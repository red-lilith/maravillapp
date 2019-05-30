from django import forms
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from .models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','cantidad','tipo','ingredientes','precio','imagen','estado']

        widgets={
        'ingredientes': ModelSelect2MultipleWidget(
        model = Ingrediente,
        search_fields=['nombre__icontains'],
        required = False,
        )}


class ComboForm(forms.Form):
    class Meta:
        model = Combo
        fields = '__all__'

        widgets = {
        'productos': ModelSelect2MultipleWidget(
        model = Ingrediente,
        search_fields=['nombre__icontains'],
        )
        }
