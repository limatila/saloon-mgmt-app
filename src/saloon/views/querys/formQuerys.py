# for usage in forms
from datetime import datetime, timedelta

from saloon.forms import *

def create_client_and_appointment(request) -> dict[str, ClientForm | AppointmentForm] | bool:
    match(request.method):
        case 'POST':
            #form submitted
            client_form = ClientForm(request.POST)
            appointment_form = AppointmentForm(request.POST)

            if client_form.is_valid() and appointment_form.is_valid():
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