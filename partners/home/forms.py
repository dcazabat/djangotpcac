from django import forms
from django.forms import ValidationError
import re

def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El nombre no puede contener números. %(valor)s',
                            code='Invalid',
                            params={'valor':value})

def validate_email(value):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError('Correo electrónico inválido')
    return value
 
class ContactoForm(forms.Form):
    TIPO_CONSULTA = (
        ('','-Seleccione-'),
        (1,'General'),
        (2,'Eventos'),
        (3,'Novedades'),
        (4,'Cobros de Cuotas')
    )

    # Style CSS string's
    __formLabelControl = 'block mb-2 text-sm font-medium text-gray-900'
    __formControl = 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5'
    __formButton = 'py-3 px-5 text-sm font-medium text-center text-white rounded-lg bg-primary-700 sm:w-fit hover:bg-primary-800 focus:ring-4 focus:outline-none focus:ring-primary-300'
    __formCheckBox = 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
    nombre = forms.CharField(
            label='Nombre', 
            max_length=50,
            validators=(solo_caracteres,),
            widget=forms.TextInput(attrs={'class': __formControl,'placeholder':'Solo letras'}
                    )
        )
    email = forms.EmailField(
            label='Email',
            max_length=100,
            required=False,
            validators=(validate_email,),
            error_messages={
                    'required': 'Por favor completa el campo'
                },
            widget=forms.TextInput(attrs={'class':__formControl,'type':'email'})
        )
    asunto = forms.CharField(
        label='Asunto',
        max_length=100,
        widget=forms.TextInput(attrs={'class':__formControl})
    )
    mensaje = forms.CharField(
        label='Mensaje',
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 5,'class':__formControl})
    )
    tipo_consulta = forms.ChoiceField(
        label='Tipo de consulta',
        choices=TIPO_CONSULTA,
        widget=forms.Select(attrs={'class':__formControl})
    )
    suscripcion = forms.BooleanField(
        label='Deseo suscribirme a las novedades !!!',
        required=False,
        widget=forms.CheckboxInput(attrs={'class':__formCheckBox,'value':1})
    )

    def clean_mensaje(self):
        data = self.cleaned_data['mensaje']
        if len(data) < 10:
            raise ValidationError("Debes especificar mejor el mensaje que nos envias")
        return data

    def clean(self):
        cleaned_data = super().clean()
        asunto = cleaned_data.get("asunto")
        suscripcion = cleaned_data.get("suscripcion")

        if suscripcion and asunto and "suscripcion" not in asunto:
            msg = "Debe agregar la palabara 'suscripcion' al asunto."
            self.add_error('asunto', msg)