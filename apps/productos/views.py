from django.shortcuts import render

# Create your views here.
def tienda(request):
    #usuario = request.user
    return render(request, 'tienda.html')

#def mi_item(slug):
#    return Producto.get_producto(slug)

def item(request): #slug
    #usuario = request.user
    return render(request, 'item.html') #{'peli': mi_item(slug)}
