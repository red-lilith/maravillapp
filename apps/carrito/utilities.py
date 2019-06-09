import io

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Table, Paragraph
from reportlab.platypus import TableStyle
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



def generar_pdf_factura(orden, usuario, tenant):
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename="Factura de Compra - Orden No. "' + str(orden.cod_ref) + '".pdf"'\
        .format(title="Factura de Compra - Orden No." + str(orden.cod_ref))

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.setTitle("Factura de Compra - Orden No. " + str(orden.cod_ref))

    # Configuracion de pagina
    p.setPageSize((200, 350))

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    p.setFont("Helvetica", 10)
    p.drawCentredString(100, 330, "****Franquicias Maravilla****")
    p.setFont("Helvetica", 10)
    p.drawCentredString(100, 320, str(tenant.nombre))
    p.setFont("Helvetica", 8)
    p.drawCentredString(100, 310, "Dirección: " + str(tenant.direccion))
    p.drawCentredString(100, 302, "Teléfono: " + str(tenant.telefono))

    p.setFillColor(colors.black)
    p.rect(20, 280, 150, 10, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 8)
    p.drawString(20, 280, "Factura # " + str(orden.cod_ref))
    p.setFillColor(colors.black)
    p.drawString(20, 270, "Fecha de Compra: " + str(orden.date_ordered))
    if usuario.is_authenticated:
        p.drawString(20, 262, "Nombre del Cliente: " + str(usuario.first_name + " " + usuario.last_name))
        p.drawString(20, 254, "CC.: " + str(usuario.documento))
    else:
        p.drawString(20, 262, "Nombre del Cliente: ")
        p.drawString(20, 254, "CC.: ")
    p.drawString(20, 240, "==================================")

    styles = getSampleStyleSheet()
    stylesBH = ParagraphStyle('Parrafos',
                              alignment=TA_LEFT,
                              fontSize=8,
                              fontName='Helvetica-Bold')

    numero = Paragraph('''#''', stylesBH)
    producto = Paragraph('''Producto''', stylesBH)
    cantidad = Paragraph('''Cant.''', stylesBH)
    total = Paragraph('''Total''', stylesBH)

    data = []
    data.append([numero, producto, cantidad, total])

    # Table
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 8

    high = 210

    for index, item in enumerate(orden.items.all(), start=1):
        this_item = [index, item.producto, 1, item.producto.precio]
        data.append(this_item)
        high = high - 18

    # table size
    width, height = 0,0
    table = Table(data, colWidths=[0.5 * cm, 3 * cm, 1.5 * cm, 1.5 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.white)
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 0, high)

    # valor total
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 10)
    p.drawString(70, high-18, "Total a Pagar: $"+str(orden.get_carrito_total()))

    p.setFont("Helvetica", 8)
    p.drawString(20, high-50, "==================================")
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(100, high-100, "¡Gracias por su compra!")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response