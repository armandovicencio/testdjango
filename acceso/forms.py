from datetime import date

from django import forms

from acceso.models import Usuario

import re



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(
    r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
NOMBRE_REGEX = re.compile(
    r'^([a-zA-Z ]{2,254})')


class UsuarioForm(forms.ModelForm):

    confirmar_password = forms.CharField(
        label="Confirmar Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

  


    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if len(nombre) < 2:
            raise forms.ValidationError(
                'Nombre debe tener minimo 2 caracteres ')
        if not NOMBRE_REGEX.match(nombre):
            raise forms.ValidationError('Nombre Solo debe contener letras')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if len(apellido) < 2:
            raise forms.ValidationError(
                'apellido debe tener minimo 2 caracteres')
        if not NOMBRE_REGEX.match(apellido):
            raise forms.ValidationError('apellido Solo debe contener letras')
        return apellido

    def clean_email(self):
        email = self.cleaned_data['email']
        if not EMAIL_REGEX.match(email):
            raise forms.ValidationError(
                'Ingresar formato válido de Correo Electronico')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError(
                'Contraseña debe tener mínimo 8 caracteres ')
        if not PASSWORD_REGEX.match(password):
            raise forms.ValidationError(
                'Ingresar formato valido de contraseña, letras y números')
        return password

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        if cleaned_data.get('password') != cleaned_data.get('confirmar_password'):
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
            )

    class Meta:
        model = Usuario
        # fields = ['nombre', 'apellido', 'username',
        #           'email', 'birthday', 'password']
        fields = ['nombre', 'apellido', 'username',
                  'email', 'password']

        labels = {
            'nombre': 'Nombre: ',
            'apellido': 'Apellido: ',
            'username': 'Nombre Usuario: ',
            'email': 'Correo: ',
            # 'birthday': 'Cumpleaños:',
            'password': 'Contraseña: ',
            'description': 'Descripción'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
            # 'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': date.today().strftime('%Y-%m-%d')}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

