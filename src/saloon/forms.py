#Django Forms models for data entrys
from django import forms
from datetime import datetime
from .models import Appointment, Client
from validate_docbr import CPF

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'CPF', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'rounded border p-2', 'placeholder': "nome de sobrenome"}),
            'CPF': forms.TextInput(attrs={'class': 'rounded border p-2', 'placeholder': "XXX.XXX.XXX-xx"}),
            'phone_number': forms.TextInput(attrs={'class': 'rounded border p-2', 'placeholder': "+55 85 ...."}),
        }
    
    #Validation
    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        validator = CPF()
        if not validator.validate(cpf):
            raise forms.ValidationError("CPF is not valid")
        return cpf

class AppointmentForm(forms.ModelForm):
    date_scheduled = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local', #for widget use, only HTML / ISO format
                'class': 'rounded border p-2',
            },
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Appointment
        fields = ['service', 'worker', 'date_scheduled', 'status']
        widgets = {
            'service': forms.Select(attrs={'class': 'rounded border p-2'}),
            'worker': forms.Select(attrs={'class': 'rounded border p-2'}),
            'status': forms.Select(attrs={'class': 'rounded border p-2'}),
        }

    #Validation
    def clean_date_scheduled(self):
        schedule = self.cleaned_data.get('date_scheduled')
        if schedule and schedule < datetime.now():
            raise forms.ValidationError("Scheduled time must be in the future.")
        return schedule
