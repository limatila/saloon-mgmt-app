#Django Forms models for data entrys
from django import forms
from datetime import datetime

from .models import Appointment, Client, Worker
from django.contrib.auth import get_user_model
User = get_user_model() #TODO create form
from validate_docbr import CPF
from saloon.utils.extra_validations import verify_active_existant_client_with_phone_has_same_name

class BasePersonForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'CPF']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-field', 'placeholder': "name of name"}),
            'CPF': forms.TextInput(attrs={'class': 'form-field', 'placeholder': "XXX.XXX.XXX-xx"}),
        }
    
    #Validation
    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        if cpf:
            validator = CPF()
            charsToRemove = [' ', '.', '-']
            for char in charsToRemove:
                cpf = cpf.replace(char, '')   
            if not validator.validate(cpf):
                raise forms.ValidationError("CPF is not valid.")
        return cpf

class ClientForm(BasePersonForm):
    class Meta:
        model = Client
        fields = BasePersonForm.Meta.fields + ['phone_number']
        widgets = {
            **BasePersonForm.Meta.widgets,
            'phone_number': forms.TextInput(attrs={'class': 'form-field', 'placeholder': "+55 85 ...."}),
        }

    def clean_phone_number(self):
        number: str = self.cleaned_data.get('phone_number')
        if number:
            charsToRemove = [' ', '(', ')']
            if not number.startswith('+'):
                raise forms.ValidationError('Phone number must start with \'+\'')
            for char in charsToRemove:
                number = number.replace(char, '')
            if verify_active_existant_client_with_phone_has_same_name(number, self.cleaned_data.get('name')):
                raise forms.ValidationError('An existant & active phone number was already registered.')
        return number
    
    def clean(self): #custom all-fields cleaner
        cleaned_data = super().clean()

        cpf = cleaned_data.get('CPF')
        number = cleaned_data.get('phone_number')
        #check if both fields are not empty
        if not cpf and not number:
            raise forms.ValidationError("Either \'CPF\' or \'phone number\' must be provided. At least 1 needs to be inserted.")

        return cleaned_data

class WorkerForm(BasePersonForm):
    class Meta:
        model = Worker
        fields = BasePersonForm.Meta.fields + ['active', 'image']
        widgets = {
            **BasePersonForm.Meta.widgets,
            'image': forms.FileInput(attrs={'class': 'rounded p-2'}),
        }

class AppointmentForm(forms.ModelForm):
    date_scheduled = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local', #for widget use, only HTML / ISO format
                'class': 'form-field',
            },
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Appointment
        fields = ['service', 'worker', 'date_scheduled', 'status']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-field'}),
            'worker': forms.Select(attrs={'class': 'form-field'}),
            'status': forms.Select(attrs={'class': 'form-field'}),
        }

    #Validation
    def clean_date_scheduled(self):
        schedule = self.cleaned_data.get('date_scheduled')
        if schedule and schedule < datetime.now():
            raise forms.ValidationError("Scheduled time must be in the future.")
        return schedule


#TODO: User form, User confirmation form, User login