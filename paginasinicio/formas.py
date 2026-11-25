from django import forms
from django.forms import ModelForm
from .models import Tarea

class TareaForm(ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'importante']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Ingrese el título de la tarea'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Ingrese la descripción de la tarea'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                     'placeholder': 'Marque si es importante'}),
        }