from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django import forms

from acceso.models import Usuario
from core.models import Wish

import re


class WishForm(forms.ModelForm):

    def clean_item(self):
        item = self.cleaned_data['item']
        if len(item) < 1:
            raise forms.ValidationError(
                'Tu deseo debe tener minimo 3 caracteres ')
        return item

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 1:
            raise forms.ValidationError(
                'Debe agregar una descripcion ')
        return description

    class Meta:
        model = Wish
        fields = ['item', 'description']

        labels = {
            'item': 'Título: ',
            'description': 'Descripción: '
        }

        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# def add_wish(request):

#     if request.method == 'GET':
#         return render(request, 'core/wishes.html', {'formModel'  : WishForm()})
    
#     if request.method == "POST":
#         print(request.POST)

#         form = WishForm(request.POST)

#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Wish creado correctamente')
#             return redirect(reverse('wishes:agregar'))
#         else:
#             messages.error(request, 'Con errores, solucionar.')
#             return render(request, 'core/wishes.html', {'formModel'  : form})    

