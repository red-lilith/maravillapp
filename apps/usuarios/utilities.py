import io

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
import locale
from django.core import signing
from django.urls import reverse


def generar_pdf_usuarios(usuarios, tipo):
    response = HttpResponse(content_type='application/force-download')

    if tipo:
        response['Content-Disposition'] = 'inline; filename="Listado_Digitadores.pdf"' \
            .format(title="Listado Digitadores")

    else:
        response['Content-Disposition'] = 'inline; filename="Listado_Clientes.pdf"' \
            .format(title="Listado Clientes")

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Configuracion de pagina
    #p.setPageSize((200, 350))

    # Signature data

    # Path
    # TODO Cambiar dependiendo de dominio
    path = 'https://cinemapp-uv.herokuapp.com'

    # signer = Signer()
    # value = signer.sign(str(boleta.id))
    # url = reverse('boletas:validar_boleta', args=[value])

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # titulo
    p.setFont("Helvetica", 14)
    p.drawCentredString(100, 320, "MARAVILLA")

    p.setFillColor(colors.black)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response