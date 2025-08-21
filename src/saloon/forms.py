#Django Forms models for data entrys
from django import forms
from datetime import datetime
from .models import Appointment, Client, Worker
from django.contrib.auth import get_user_model
User = get_user_model() #TODO create form
from validate_docbr import CPF

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
        validator = CPF()
        charsToRemove = [' ', '.', '-']
        for char in charsToRemove:
            cpf = cpf.replace(char, '')   
        if not validator.validate(cpf):
            raise forms.ValidationError("CPF is not valid")
        return cpf

    def validate_unique(self):
        pass

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
        charsToRemove = [' ', '(', ')']
        if not number.startswith('+'):
            raise forms.ValidationError('Phone number must start with \'+\'')
        for char in charsToRemove:
            number = number.replace(char, '')
        return number

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

class WorkerForm(BasePersonForm):
    class Meta:
        model = Worker
        fields = BasePersonForm.Meta.fields + ['active', 'image']
        widgets = {
            **BasePersonForm.Meta.widgets,
            'image': forms.FileInput(attrs={'class': 'rounded p-2'})
        }


#TODO: User form, User confirmation form, User login