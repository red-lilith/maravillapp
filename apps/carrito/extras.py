from django.conf import settings
import random
import string
from datetime import date
import datetime
import braintree
from apps.carrito.models import ItemCarrito

def generar_orden_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str

# gateway = braintree.BraintreeGateway(
#     braintree.Configuration(
#         environment=settings.BT_ENVIRONMENT,
#         merchant_id=settings.BT_MERCHANT_ID,
#         public_key=settings.BT_PUBLIC_KEY,
#         private_key=settings.BT_PRIVATE_KEY
#     )
# )

def generar_token_cliente():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def encontrar_transaccion(id):
    return gateway.transaction.find(id)
