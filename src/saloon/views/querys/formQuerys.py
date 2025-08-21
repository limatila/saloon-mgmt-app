# for usage in forms
from datetime import datetime, timedelta

from saloon.forms import *
from saloon.utils.extra_validations import verify_client_is_active


def register_client_and_appointment(request) -> dict[str, ClientForm | AppointmentForm] | bool:
    match(request.method):
        case 'POST':
            #form submitted
            client_form = ClientForm(request.POST)
            appointment_form = AppointmentForm(request.POST)
            if client_form.is_valid() and appointment_form.is_valid():
                clientData = client_form.cleaned_data
                cpf, number = clientData.get('CPF'), clientData.get('phone_number')
                client_cpf = Client.objects.filter(CPF=cpf).first()
                client_phone = Client.objects.filter(phone_number=number).first()
                if client_cpf:
                    client = client_cpf
                elif client_phone:
                    if not verify_client_is_active(client_phone):
                        client_phone.delete()
                        client = client_form.save()
                    else:
                        client = client_phone
                else:
                    client = client_form.save()
                appointment = appointment_form.save(commit=False)
                appointment.client = client
                appointment.save()
                return True
            else:
                forms = {
                    'client_form': client_form,
                    'appointment_form': appointment_form
                }
        case "GET":
            # if client loading in form / client inserted invalid values
            initial_dt = (
                datetime.now().replace(second=0, minute=0) + timedelta(hours=1)
                ).strftime('%Y-%m-%dT%H:%M')
            forms = {
                'client_form': ClientForm(),
                'appointment_form': AppointmentForm(initial={'date_scheduled': initial_dt}),
            }

    return forms

#TODO worker form query