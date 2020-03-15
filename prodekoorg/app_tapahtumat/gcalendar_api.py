import os
from datetime import datetime, timedelta, time, date
from io import BytesIO
from re import match

from apiclient.discovery import build
from apiclient.http import MediaIoBaseDownload
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from google.oauth2 import service_account
from PyPDF2 import PdfFileMerger, PdfFileReader
from urllib.error import HTTPError

from .constants import TEAM_DRIVE_ID
from .models import Tapahtuma


def initialize_service():
    """Initializes a Google Calendar API instance.

    Returns:
        Google Calendar API service object.
    """

    SERVICE_ACCOUNT_FILE = os.path.join(
        settings.BASE_DIR, "prodekoorg/service_account.json"
    )
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    credentials = credentials.with_subject("mediakeisari@prodeko.org")
    service = build("calendar", "v3", credentials=credentials)
    return service


def generate_desc(event):
    ret = ""
    if event.short_desc:
        ret += event.short_desc + "\n\n"
    if event.t_what:
        ret += "MITÄ: " + event.t_what + "\n"
    if event.t_where:
        ret += "MISSÄ: " + event.t_where + "\n"
    if event.t_when:
        ret += "MILLOIN: " + event.t_when + "\n"
    else:
        start_datetime = event.start_date.strftime("%d.%m.%Y")
        if event.start_time:
            start_datetime += " " + event.start_time.strftime("%H:%M")
        ret += "MILLOIN: " + start_datetime + "\n"
    if event.t_why:
        ret += "MIKSI: " + event.t_why + "\n"
    if event.t_cost:
        ret += "MITÄ MAKSAA: " + event.t_cost + "\n"
    if event.t_dc:
        ret += "DC: " + event.t_dc + "\n"
    if event.t_for_who:
        ret += "KENELLE: " + event.t_for_who + "\n"
    if len(ret) > 0:
        ret += "\n\n"
    ret += event.desc
    return ret


def generate_event(event):
    """Generoi tapahtuma google calendar APIa varten
    
    Arguments:
        event {Tapahtuma} -- Tapahtuma
    """
    ret_event = {"summary": event.name, "id": event.uuid.hex}

    if event.start_time:
        ret_event["start"] = {
            "dateTime": datetime.combine(
                event.start_date, event.start_time
            ).isoformat(),
            "timeZone": "Europe/Helsinki",
        }
    else:
        ret_event["start"] = {
            "date": event.start_date.isoformat(),
            "timeZone": "Europe/Helsinki",
        }

    if event.end_date:
        if event.end_time:
            ret_event["end"] = {
                "dateTime": datetime.combine(
                    event.end_date, event.end_time
                ).isoformat(),
                "timeZone": "Europe/Helsinki",
            }
        else:
            if event.start_time:
                ret_event["end"] = {
                    "dateTime": (
                        datetime.combine(event.end_date, event.start_time)
                        + timedelta(hours=1)
                    ).isoformat(),
                    "timeZone": "Europe/Helsinki",
                }
            else:
                ret_event["end"] = {
                    "date": event.end_date.isoformat(),
                    "timeZone": "Europe/Helsinki",
                }
    else:
        if event.start_time:
            if event.end_time:
                ret_event["end"] = {
                    "dateTime": datetime.combine(
                        event.start_date, event.end_time
                    ).isoformat(),
                    "timeZone": "Europe/Helsinki",
                }
            else:
                ret_event["end"] = {
                    "dateTime": (
                        datetime.combine(event.start_date, event.start_time)
                        + timedelta(hours=1)
                    ).isoformat(),
                    "timeZone": "Europe/Helsinki",
                }
        else:
            ret_event["end"] = {
                "date": event.start_date.isoformat(),
                "timeZone": "Europe/Helsinki",
            }

    desc = generate_desc(event)

    if desc:
        ret_event["description"] = desc

    print(ret_event)

    return ret_event


def update_event(event):
    """[summary]
    
    Arguments:
        event {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    print(event)
    try:
        service = initialize_service()
    except Exception as e:
        print(e)
        return False

    new_event = generate_event(event)

    try:
        old_event = Tapahtuma.objects.get(uuid=event.uuid)
        cal_event = (
            service.events()
            .get(
                calendarId="prodeko.org_br7j1nk202p8r7840h0be18d9o@group.calendar.google.com",
                eventId=new_event["id"],
            )
            .execute()
        )

        service.events().update(
            calendarId="prodeko.org_br7j1nk202p8r7840h0be18d9o@group.calendar.google.com",
            eventId=new_event["id"],
            body=new_event,
        ).execute()
        return True
    except Exception as e:
        print(e)

    try:
        service.events().insert(
            calendarId="prodeko.org_br7j1nk202p8r7840h0be18d9o@group.calendar.google.com",
            body=new_event,
        ).execute()
        return True
    except Exception as e:
        print(e)
        return False

