## README

**SQL para Tenants**

`INSERT INTO "tenants_tenant" ("schema_name", "nombre", "paquete", "direccion", "telefono","pagado_hasta","estado") VALUES
('public', 'public','none','Cll 100 #12-03','5555555', '2099-01-01','True');`

`INSERT INTO "tenants_dominio" ("domain", "is_primary", "tenant_id") VALUES
('127.0.0.1', true, 1);`


**NOTA:** Debe crearse un superuser para cada tenant el cual será su administrador

**IMPORTAR cities a cada Tenant**
`python manage.py tenant_command loaddata cities_light_country.json --schema="t1"`

`python manage.py tenant_command loaddata cities_light_region.json --schema="t1"`

`python manage.py tenant_command loaddata cities_light_city.json --schema="t1"`


[settings.py](https://drive.google.com/open?id=1MXGMcfsgTpbDG_mCMkJy4S4tpjnyNqaF)

[Template Bootstrap4](https://themewagon.com/themes/free-bootstrap-4-html5-coffee-website-template-coffee-blend/)


[Guía de django-bootstrap4](https://buildmedia.readthedocs.org/media/pdf/django-bootstrap4/latest/django-bootstrap4.pdf)


