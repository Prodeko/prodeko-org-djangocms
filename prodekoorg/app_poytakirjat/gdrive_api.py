import os
from datetime import datetime
from io import BytesIO
from re import match

from apiclient.discovery import build
from apiclient.http import MediaIoBaseDownload
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from google.oauth2 import service_account
from PyPDF2 import PdfFileMerger, PdfFileReader

from .models import Dokumentti

TEAM_DRIVE_ID = '0AD8EdtHhweZwUk9PVA'


def initialize_service():
    """Initializes a Google Drive API instance.

    Returns:
        Google Drive API service object.
    """

    SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'prodekoorg/app_poytakirjat/service-account.json')

    # mimeType of Google Drive folder
    SCOPES = ['https://www.googleapis.com/auth/drive']

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_credentials = credentials.with_subject('mediakeisari@prodeko.org')

    service = build('drive', 'v3', credentials=delegated_credentials)
    return service


def merge_liitteet_to_doc(pdfs):
    """Merges a list of pdf's into a single pdf file.

    Utilizes the PdfFileMerger from PyPDF2.

    Args:
        pdfs: List of pdf's to merge.

    Returns:
        BytesIO buffer contents (a pdf file).
    """

    merger = PdfFileMerger()
    for pdf in pdfs:
        if(pdf):
            merger.append(PdfFileReader(pdf))
            pdf.close()

    fh = BytesIO()
    merger.write(fh)
    ret = fh.getvalue()

    fh.close()

    return ret


# TODO compress pdf using something. Now they are ~7MB and
# can be reduced to ~500kb without visible changes
def compress_pdf(fh_pdf):
    import ghostscript

    args = [
        "ghostscript",  # actual value doesn't matter
        "-dNOPAUSE", "-dBATCH", "-dSAFER", "dQUIET",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/printer",
        "-sOutputFile=test.pdf",
        "-c", ".setpdfwrite",
        "-f", fh_pdf
    ]

    ghostscript.Ghostscript(*args)


def get_gdrive_folders_dict(service, parent_folder_id):
    """Get a dictionary of files in a Google Drive folder.

    Generates a dictionary containing folder id's whose parent
    folder's id is parent_folder_id.

    Args:
        service: Drive API service instance.
        folder_id: Id of the parent folder.

    Returns:
        Python dictionary containing folder id's that
        are children of parent_folder_id.
    """

    while True:
        folders = service.files().list(
            corpora="teamDrive",
            orderBy="createdTime",
            q="mimeType='application/vnd.google-apps.folder' and parents in '" + parent_folder_id + "'",
            supportsTeamDrives=True,
            includeTeamDriveItems=True,
            teamDriveId=TEAM_DRIVE_ID).execute()
        return folders


def filter_gdrive_folders_dict(folders_dict):
    """Filter folders_dict dictionary.

    Filter out folders names that don't match a regular expression in the
    folder name. Folder id's for which we already have documents are
    also filtered out.

    Args:
        folders_dict: Dictionary folder info that gets converted to Dokumentti models.

    Returns:
        A filtered Python dictionary containing folder id's
        whose contents are to be downloaded next.
    """

    # Use a regex match to include only folders names such as '10_31.12.2018'
    filtered_dict = {k['id']: k['name'] for k in folders_dict['files'] if match(
        '\d{2}_([0-9]|[1-3][0-9]).([1-9]|[1][0-2]).\d{4}$', k['name'])}

    existing_gdrive_ids = Dokumentti.objects.values_list('gdrive_id', flat=True)

    # Filter out documents that we already have in the database
    if existing_gdrive_ids:
        filtered_dict = {k: v for k, v in filtered_dict.items() if k not in list(existing_gdrive_ids)}
    return filtered_dict


def create_models_from_folders(service, request, folders_dict):
    """Create Django objects from folders_dict

    Args:
        service: Drive API service instance.
        folders_dict: Python dictionary containing
            containing info that gets converted to Dokumentti models.

    Returns:
        Integer count of successfully downloaded documents.
    """

    # Filter out unwanted folders inside the 'Kokoukset' folder
    filtered_dict = filter_gdrive_folders_dict(folders_dict)
    success_count = 0
    for parent_id, name in filtered_dict.items():

        # Get ordinal number from folder name
        number_string = name[:2]
        try:
            number = int(number_string)
        except ValueError:
            number = 999
        name = name

        # Get date from folder name
        date = datetime.strptime(name[3:], "%d.%m.%Y").date()

        # Downloaded files as BytesIO objects
        poytakirja, liitteet = download_files_as_pdf(service, parent_id)

        pdf_file = merge_liitteet_to_doc([poytakirja] + liitteet)
        final_pdf = ContentFile(pdf_file)

        # Create the new Dokumentti object and save 'final_pdf'
        doc = Dokumentti.objects.create(gdrive_id=parent_id, name=name, number=number, date=date)
        doc.doc_file.save('{}.pdf'.format(name), final_pdf)
        success_count += 1
    return success_count


def download_files_as_pdf(service, parent_id):
    """Download files beginning 'Pöytäkirja' and 'LIITE' in a Drive
    folder specified by parent_id.

    Args:
        service: Drive API service instance.
        parent_id: Id of the parent folder.

    Returns:
        Tuple consisting of 1. a pdf file and 2. the attachments to that pdf file.
    """

    poytakirja = service.files().list(
        corpora="teamDrive",
        q="mimeType='application/vnd.google-apps.document' and name contains 'Pöytäkirja' and parents in '{}'".format(parent_id),
        supportsTeamDrives=True,
        includeTeamDriveItems=True,
        pageSize=1,  # Only return one file at max
        teamDriveId=TEAM_DRIVE_ID).execute()

    pdf_file = download_gdoc_as_pdf(poytakirja['files'], service)

    liitteet = service.files().list(
        corpora="teamDrive",
        q="mimeType='application/pdf' and name contains 'LIITE' and parents in '{}'".format(parent_id),
        supportsTeamDrives=True,
        includeTeamDriveItems=True,
        teamDriveId=TEAM_DRIVE_ID).execute()

    liitteet = download_liitteet(liitteet['files'], service)

    return pdf_file, liitteet


def download_gdoc_as_pdf(files, service):
    """Downloades the Google Doc document as a pdf using the Drive API.

    Args:
        files: List of .gdocs files in a Drive folder.
        service: Drive API service instance.

    Returns:
        PDF file that was generated from a Google Docs file.
    """

    pdf_file = None
    if files:
        # 'files' parameter should only contain one file
        f = files[0]
        request = service.files().export_media(fileId=f['id'],
                                               mimeType='application/pdf')
        fh = BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        pdf_file = fh

    # Not closing the BytesIO here is deliberate
    # It gets closed in 'merge_liitteet_to_doc'
    return pdf_file


def download_liitteet(files, service):
    """Downloades the attachments in a folder as PDF files.

    There may be 0 or more attachments in a folder.

    Args:
        files: List of attachment files in a Drive folder.
        service: Drive API service instance.

    Returns:
        List of attachment pdf files.
    """

    pdf_files = []

    # Sort liitteet by name so that liite named 'LIITE1' gets
    # merged to the final pdf before 'LIITE2' and so on
    files = sorted(files, key=lambda k: k['name'])
    if files:
        for f in files:
            request = service.files().get_media(fileId=f['id'])
            fh = BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            pdf_files.append(fh)

    # Not closing the BytesIO here is deliberate
    # It gets closed in 'merge_liitteet_to_doc'
    return pdf_files


@staff_member_required
def run_app_poytakirjat(request):
    """Main routine of this file that gets called from Django admin view.

    It works as follows:

    1. Obtain folderID from POST
    2. Get a dictionary of children folders of folderID
    3. Create Django models from the folder dict
    4. Redirect to the dokumentti admin page and display either
        an error message or the number of successfully downloaded
        documents

    Args:
        request: HttpRequest object.

    Returns:
        Redirects to the main admin dokumentti page.

        A user must be a staff member to access this function.
    """

    # Id of the 'Kokoukset' folder iside 'Hallituksen sisäinen Team Drive
    folder_id = request.POST['folderID']
    try:
        service = initialize_service()
        # Returns a dict of folders inside the folder_id above
        folders_dict = get_gdrive_folders_dict(service, folder_id)
        success_count = create_models_from_folders(service, request, folders_dict)
        messages.add_message(request, messages.INFO, 'Ladattu {} pöytäkirjaa G Drivestä.'.format(success_count))
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Virhe pöytäkirjoja ladattaessa: {}'.format(e))
    return redirect('/admin/app_poytakirjat/dokumentti/')
