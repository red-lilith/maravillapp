from django import forms
from .models import *
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ('nombre', 'estilos')
        widgets = {
            'estilos': ModelSelect2MultipleWidget(
                model=Estilos,
                search_fields=['nombre__icontains'],
            )
        }

class TenantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        super(TenantForm, self).__init__(*args, **kwargs)
        self.fields['schema_name'].label = "Subdominio *"

    class Meta:
        model = Tenant
        fields = ('nombre', 'pagado_hasta', 'paquete', 'direccion', 'telefono', 'schema_name',)
        widgets = {
            'paquete': ModelSelect2Widget(
                model=Paquete,
                search_fields=['nombre__icontains'],
            )
        }

    def clean_schema_name(self):
        dir_tenant = self.cleaned_data["schema_name"]
        if dir_tenant.lower() == 'www':
            self.add_error("schema_name", "No es posible registrar %s como dirección en el sistema" % dir_tenant)

        return dir_tenant


class ModificarTenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ('nombre', 'paquete', 'direccion', 'telefono', 'estado',)
