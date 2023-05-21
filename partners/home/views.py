from django.shortcuts import render
from home.forms import ContactoForm

from datetime import datetime
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
import requests
from partners.settings import SITE_NAME
import calendar as cl
import datetime as dt
# Create your views here.


def index(request):
    data = {
        'data': {},
        'title': SITE_NAME,
        'position': 'Dashboard'
    }
    return render(request, 'home/index.html', context=data)


def about(request):
    data = {
        'data': {},
        'title': SITE_NAME,
        'position': 'ABOUT - Que te ofrecemos !!!'
    }
    print(data)
    return render(request, 'home/about.html', context=data)


def calendar(request, year=0, month=0):
    if year == 0:
        year = dt.datetime.now().year
    if month == 0:
        month = dt.datetime.now().month
    dataCalendar = cl.monthcalendar(year, month)
    listEvent = [(2023, 5, 5), (2023, 5, 25)]
    data = {
        'data': dataCalendar,
        'title': SITE_NAME,
        'tyear': year,
        'tmonth': month,
        'monthName': cl.month_name[month],
        'events': listEvent,
        'position': 'CALENDAR - Vencimientos !!!'
    }
    print(data)
    return render(request, 'home/calendar.html', context=data)


def contact(request):
    if (request.method == 'POST'):
        contacto_form = ContactoForm(request.POST)
        if (contacto_form.is_valid()):
            messages.success(request, 'Hemos recibido tus datos')
            mensaje = f"De: {contacto_form.cleaned_data['nombre']} <{contacto_form.cleaned_data['email']}>\n Asunto: {contacto_form.cleaned_data['asunto']}\n Mensaje: {contacto_form.cleaned_data['mensaje']}"
            mensaje_html = f"""
                <p>De: {contacto_form.cleaned_data['nombre']} <a href="mailto:{contacto_form.cleaned_data['email']}">{contacto_form.cleaned_data['email']}</a></p>
                <p>Asunto:  {contacto_form.cleaned_data['asunto']}</p>
                <p>Mensaje: {contacto_form.cleaned_data['mensaje']}</p>
            """
            asunto = "CONSULTA DESDE LA PAGINA - " + \
                contacto_form.cleaned_data['asunto']
            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [settings.RECIPIENT_ADDRESS],
                fail_silently=False,
                html_message=mensaje_html
            )
        # acción para tomar los datos del formulario
        else:
            messages.warning(
                request, 'Por favor revisa los errores en el formulario')
    else:
        contacto_form = ContactoForm()
    context = {
        # 'cursos':listado_cursos,
        'contacto_form': contacto_form
    }
    return render(request, 'home/contact.html', context=context)
