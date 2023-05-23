from django.shortcuts import render, redirect
from home.forms import ContactoForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from partners.settings import SITE_NAME, USER_NAME
# Create your views here.

data = {
    'data': {},
    'title': SITE_NAME,
    'position': ''
}

def index(request):
    return render(request, 'home/index.html', context=data)


def about(request):
    data['position'] = 'En que consiste PARTNERs !!!'
    return render(request, 'home/about.html', context=data)


def calendar(request, year=0, month=0):
    import calendar as cl
    import datetime as dt

    if year == 0:
        year = dt.datetime.now().year
    if month == 0:
        month = dt.datetime.now().month
    listEvent = [(2023, 5, 5), (2023, 5, 25)]
    data['data'] = cl.monthcalendar(year, month)
    data['position'] = 'Aca veremos los Vencimientos !!!'
    data['tyear'] = year
    data['tmonth'] = month
    data['monthName'] = cl.month_name[month]
    data['events'] = listEvent
    return render(request, 'home/calendar.html', context=data)


def contact(request):
    data['data'] = {}
    data['position'] = 'Contactate con Nosotros'
    if (request.method == 'POST'):
        contacto_form = ContactoForm(request.POST)
        if (contacto_form.is_valid()):
            mensaje = f"De: {contacto_form.cleaned_data['nombre']} <{contacto_form.cleaned_data['email']}>\n Asunto: {contacto_form.cleaned_data['asunto']}\n Mensaje: {contacto_form.cleaned_data['mensaje']}"
            mensaje_html = f"""
                <p>De: {contacto_form.cleaned_data['nombre']} <a href="mailto:{contacto_form.cleaned_data['email']}">{contacto_form.cleaned_data['email']}</a></p>
                <p>Asunto:  {contacto_form.cleaned_data['asunto']}</p>
                <p>Mensaje: {contacto_form.cleaned_data['mensaje']}</p>
            """
            asunto = "CONSULTA DESDE LA PAGINA - " + \
                contacto_form.cleaned_data['asunto']
            try:
                send_mail(
                    asunto,
                    mensaje,
                    settings.EMAIL_HOST_USER,
                    [settings.RECIPIENT_ADDRESS],
                    fail_silently=False,
                    html_message=mensaje_html
                )
            except BadHeaderError:
                messages.warning(request, 'Peligro de Inyeccion de Datos por mail')
                return render(request, '404.html',context=data)

            messages.success(request, 'Hemos recibido tus datos')
            contacto_form = ContactoForm()
        else:
            messages.warning(request, 'Por favor los datos ingresados en el formulario')
    else:
        contacto_form = ContactoForm()
    data['contacto_form'] = contacto_form
    return render(request, 'home/contact.html', context=data)

