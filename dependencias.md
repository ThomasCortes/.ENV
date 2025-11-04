#ENLACE_DEL_FRAMEWORK_DJANGO_TAILWIND
https://pypi.org/project/django-tailwind/

#COMANDOS_A_REALIZAR_PARA_DJANGO_TAILWIND
"Configurar settings.py: Agrega django_tailwind a tus INSTALLED_APPS y configura el middleware:"
  
    INSTALLED_APPS = [
        'django_tailwind',
        # ... otras apps
    ]

    MIDDLEWARE = [
        'django_tailwind.middleware.TailwindMiddleware',
        # ... otros middlewares
    ]


#PLANTILLA_PARA_HTML_CON_TAILWIND

    {% load tailwind_tags %}
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mi Proyecto</title>
        {% tailwind_css %}
    </head>
    <body>
        {% block content %}
        {% endblock %}
    </body>
    </html>


    --contraseña del correo de "nutriet.col@gmail.com"--
    ---Nutrietoficial2025*--
