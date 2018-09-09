import io
import locale
import time

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)
from reportlab.platypus.flowables import HRFlowable

from .models import Kulukorvaus


class KulukorvausPDF:

    def __init__(self, model_perustiedot, models_kulukorvaukset, buffer):
        # Register fonts
        self.register_fonts()
        self.model_perustiedot = model_perustiedot
        self.buffer = buffer
        self.models_kulukorvaukset = models_kulukorvaukset

    def register_fonts(self):
        pdfmetrics.registerFont(TTFont('Raleway Bold', settings.STATIC_ROOT + '/fonts/Raleway/Raleway-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('Raleway Medium', settings.STATIC_ROOT + '/fonts/Raleway/Raleway-Medium.ttf'))

    def handle_receipt(self, img_receipt):
        img = Image(io.BytesIO(img_receipt))
        img._restrictSize(12 * cm, 15 * cm)
        return img

    def get_image(self, path, width):
        """ Return image with a specified width with original aspect ratio."""
        img = ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect))

    def print_kulukorvaukset(self):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=18,
                                bottomMargin=18,
                                title='Prodeko kulukorvaus')

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name="Center", alignment=TA_CENTER))

        # General
        formatted_time = time.ctime()
        model_perustiedot = self.model_perustiedot

        # Model
        #created_by_user = model.created_by_user
        created_by = model_perustiedot.created_by
        email = model_perustiedot.email
        position_in_guild = model_perustiedot.position_in_guild
        phone_number = model_perustiedot.phone_number
        bank_number = model_perustiedot.bank_number
        bic = model_perustiedot.bic

        elements = []

        t_data = [['Nimi', created_by],
                  ['Sähköposti', email],
                  ['Asema killassa', position_in_guild],
                  ['Puhelinnumero', phone_number],
                  ['Tilinumero (IBAN)', bank_number],
                  ['BIC', bic]]

        for model in self.models_kulukorvaukset:
            fields = model._meta.get_fields()
            for field in fields:
                if field.name != "id" and field.name != "created_at" and field.name != "info":
                    verbose_name = field.verbose_name
                    value = getattr(model, field.name)
                    if field.name == "receipt":
                        receipt = self.handle_receipt(value.file.read())
                        value = receipt
                    t_data.append([verbose_name, value])

        t_style = [('GRID', (0, 0), (-1, -1), 0.01 * cm, (0, 0, 0)),
                   ('FONT', (0, 0), (-1, -1), 'Raleway Medium'),
                   ('TEXTCOLOR', (0, 0), (0, -1), colors.gray),
                   ('VALIGN', (0, 0), (0, -1), 'TOP')]

        I = self.get_image(settings.STATIC_ROOT + '/images/prodeko-logo-text-blue.png', width=10 * cm)
        s1cm = Spacer(width=0, height=1 * cm)
        s05cm = Spacer(width=0, height=0.5 * cm)
        ptime = "<font name='Raleway Medium' size=8>{}</font>".format(formatted_time)
        PTIME = Paragraph(ptime, styles['Center'])

        ptext = """<font name='Raleway Medium' size=10>Kulukorvauksesi on vastaanotettu. Hakemus käsitellään seuraavassa hallituksen kokouksessa

        <br />
        <br />
        Jos havaitset virheitä alla olevista tiedoista, ota välittömästi yhteys rahastonhoitajaan
        rahastonhoitaja@prodeko.org.
        </font>
        """
        P1 = Paragraph(ptext, styles['Normal'])
        T = Table(t_data)
        T.setStyle(TableStyle(t_style))

        elements.append(PTIME)
        elements.append(I)
        elements.append(s05cm)
        elements.append(HRFlowable(width=20 * cm))
        elements.append(s05cm)
        elements.append(P1)
        elements.append(s05cm)
        elements.append(T)

        doc.build(elements)

        # Get the value of the BytesIO buffer
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
