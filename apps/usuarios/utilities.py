import io

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Table, Paragraph
from reportlab.platypus import TableStyle
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Times New Roman', 'times.ttf'))
pdfmetrics.registerFont(TTFont('Times New Roman Bold', 'timesbd.ttf'))
pdfmetrics.registerFont(TTFont('Times New Roman Italic', 'timesi.ttf'))


def generar_pdf_usuarios(usuarios, tipo):
    response = HttpResponse(content_type='application/force-download')

    if tipo == 0:
        response['Content-Disposition'] = 'inline; filename="Listado_Digitadores.pdf"' \
            .format(title="Listado Digitadores")

    else:
        response['Content-Disposition'] = 'inline; filename="Listado_Clientes.pdf"' \
            .format(title="Listado Clientes")

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)

    if tipo:
        p.setTitle("Listado_Digitadores_Maravilla")

    else:
        p.setTitle("Listado_Clientes_Maravilla")

    #Header
    p.setLineWidth(.3)
    p.setFont('Times New Roman', 22)
    p.drawString(30, 750, 'Franquicias Maravilla')
    p.setFont('Times New Roman', 16)
    if tipo:
        p.drawString(30, 735, 'Listado de Digitadores')
    else:
        p.drawString(30, 735, 'Listado de Clientes')

    p.setFont('Times New Roman Bold', 12)
    p.drawString(470, 750, datetime.now().strftime("%Y-%m-%d %H:%M"))
    p.line(460, 747, 560, 747)


    #Table Header
    styles = getSampleStyleSheet()
    stylesBH = ParagraphStyle('Parrafos',
                              alignment=TA_CENTER,
                              fontSize=14,
                              fontName='Times-Bold')

    documento = Paragraph('''Documento''', stylesBH)
    nombres = Paragraph('''Nombres y Apellidos''', stylesBH)
    correo = Paragraph('''Correo Electrónico''', stylesBH)
    telefono = Paragraph('''Teléfono''', stylesBH)
    estado = Paragraph('''Activo''', stylesBH)

    data = []
    data.append([documento, nombres, correo, telefono, estado])

    #Table
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 14

    high = 650

    for usuario in usuarios:
        this_user = [usuario.documento, usuario.first_name + " " + usuario.last_name, usuario.email, usuario.telefono, usuario.is_active]
        data.append(this_user)
        high = high - 18

    #table size
    width, height = A4
    table = Table(data, colWidths=[3 * cm, 7 * cm, 4.5 * cm, 2.5 * cm, 1.9 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 30, high)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response