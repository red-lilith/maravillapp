## README
**SQL para Tenants**

`INSERT INTO "tenants_tenant" ("schema_name", "nombre", "administrador", "paquete", "direccion", "telefono","estado") VALUES
('public', 'public', 'admin','none','Cll 100 #12-03','5555555','True');`

`INSERT INTO "tenants_dominio" ("domain", "is_primary", "tenant_id") VALUES
('127.0.0.1', true, 1);`


**IMPORTAR cities a cada Tenant**
`python manage.py tenant_command loaddata cities_light_city.json --schema="schema_name"`


[settings.py](https://drive.google.com/open?id=1MXGMcfsgTpbDG_mCMkJy4S4tpjnyNqaF)

[Template Bootstrap4](https://themewagon.com/themes/free-bootstrap-4-html5-coffee-website-template-coffee-blend/)


[Guía de django-bootstrap4](https://buildmedia.readthedocs.org/media/pdf/django-bootstrap4/latest/django-bootstrap4.pdf)

