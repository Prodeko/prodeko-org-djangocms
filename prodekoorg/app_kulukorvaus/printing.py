from io import BytesIO

from django.conf import settings
from django.utils import timezone
from django.utils.dateformat import format
from django.utils.translation import ugettext as _
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import HRFlowable


class KulukorvausPDF:
    """PDF generation from KulukorvausPerustiedot and Kulukorvaus objects.

    This class abstracts away the pdf generation process utilising the
    reportlab library (https://www.reportlab.com/opensource/).

    Attributes:
        model_perustiedot: Timestamp of object creation.
        buffer: A BytesIO buffer.
        models_kulukorvaukset: One or more Kulukorvaus objects
    """

    def __init__(self, model_perustiedot, models_kulukorvaukset):
        """Initialize class attributes."""
        self.register_fonts()
        self.model_perustiedot = model_perustiedot
        self.buffer = BytesIO()
        self.models_kulukorvaukset = models_kulukorvaukset

    def register_fonts(self):
        """Register fonts so reportlab can use them."""
        pdfmetrics.registerFont(
            TTFont("Raleway Bold", settings.STATIC_ROOT + "/fonts/Raleway-Bold.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("Raleway Medium", settings.STATIC_ROOT + "/fonts/Raleway-Medium.ttf")
        )

    def handle_receipt(self, img_receipt):
        """Read receipt into reportlab compatible Image format and make it smaller."""
        img = Image(BytesIO(img_receipt))
        img._restrictSize(12 * cm, 15 * cm)
        return img

    def get_image(self, path, width):
        """Return image with a specified width and the original aspect ratio."""
        img = ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect))

    def print_kulukorvaukset(self):
        """Generates a pdf file from submitted form data."""
        buffer = self.buffer
        doc = SimpleDocTemplate(
            buffer, rightMargin=72, leftMargin=72, topMargin=18, bottomMargin=18
        )

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name="Center", alignment=TA_CENTER))

        # General data
        formatted_time = format(timezone.now(), "D, j M Y H:i:s")
        model_perustiedot = self.model_perustiedot

        # Extract data from model
        created_by = model_perustiedot.created_by
        email = model_perustiedot.email
        phone_number = model_perustiedot.phone_number
        bank_number = model_perustiedot.bank_number
        bic = model_perustiedot.get_bic_display()
        additional_info = model_perustiedot.additional_info

        # Container to hold table elements
        elements = []

        # Setup table data
        t_basic_info = [
            [_("Name"), created_by],
            [_("Email"), email],
            [_("Phone number"), phone_number],
            [_("Account number (IBAN)"), bank_number],
            ["BIC", bic],
            [_("Additional info"), additional_info],
        ]

        t_kulu = []
        # Loop Kulukorvaus models and append to t_kulu
        for model in self.models_kulukorvaukset:
            fields = model._meta.get_fields()
            for field in fields:
                if (
                    field.name != "id"
                    and field.name != "created_at"
                    and field.name != "info"
                ):
                    verbose_name = field.verbose_name
                    value = getattr(model, field.name)
                    if field.name == "receipt":
                        receipt = self.handle_receipt(value.file.read())
                        value = receipt
                    t_kulu.append([verbose_name, value])

        # Styling for the table
        t_style = [
            ("GRID", (0, 0), (-1, -1), 0.01 * cm, (0, 0, 0)),
            ("FONT", (0, 0), (-1, -1), "Raleway Medium"),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.gray),
            ("VALIGN", (0, 0), (0, -1), "TOP"),
        ]

        Img = self.get_image(
            settings.STATIC_ROOT + "/images/logos/prodeko-logo-text-blue.png",
            width=10 * cm,
        )
        s05cm = Spacer(width=0, height=0.5 * cm)
        ptime = f"<font name='Raleway Medium' size=8>{formatted_time}</font>"
        PTIME = Paragraph(ptime, styles["Center"])

        text_info = _(
            "Your reimbursement claim has been received. The claim will be processed in the next Prodeko board meeting."
        )
        text_errors = _(
            "If you notice any errors in the information below, contact Prodeko's treasurer immediately at rahastonhoitaja@prodeko.org."
        )

        ptext = f"""<font name='Raleway Medium' size=10>{text_info}
        <br />
        <br />
        {text_errors}
        </font>
        """

        # Setup paragraph of text before the table as well as the table
        P1 = Paragraph(ptext, styles["Normal"])
        T_basic = Table(t_basic_info)
        T_kulu = Table(t_kulu)
        T_basic.setStyle(TableStyle(t_style))
        T_kulu.setStyle(TableStyle(t_style))

        # Append pdf elements (time, image, spacers, paragraph, table)
        # to the container
        elements.append(PTIME)
        elements.append(Img)
        elements.append(s05cm)
        elements.append(HRFlowable(width=20 * cm))
        elements.append(s05cm)
        elements.append(P1)
        elements.append(s05cm)
        elements.append(T_basic)
        elements.append(s05cm)
        elements.append(T_kulu)

        doc.build(elements)

        # Get the value of the BytesIO buffer
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
