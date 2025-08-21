from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect

from saloon.views.querys import dataQuerys, formQuerys

# Create your views here.

#* Redirections
def REDIRECT_HOME(request):
    return redirect('home')
def REDIRECT_ADMIN(request):
    return HttpResponseRedirect('/admin/')
def BASE(request):
    return HOME(request, True)

#* Renders
def HOME(request, base: bool = False):
    title: str = "Home"
    if base: title = "Base"
    return render(request, 'pages/home.html', 
                    context={
                        'baseRender': base,
                        'childRender': (not base),
                        'title': title,
                        'workers': dataQuerys.load_data_range('workers', range=8, offset=0),
                        
                        'appointments': dataQuerys.load_all_appointments_today(),
                        'qtt_ongoing_hour': dataQuerys.load_ongoing_appointments_next_hour(),
                        'qtt_finished_today': dataQuerys.load_finished_appointments_today(),
                        'value_revenue_today': dataQuerys.load_revenue_today(),
                    }
            )

def DYNAMIC_RENDER(request):
    title: str = None
    for modelName in dataQuerys.MODEL_CHOICES:
        if modelName in request.path.lower():
            title: str = modelName
            break;
    if not title:
        raise Http404('The model for the view was not found.')

    return render(request, f'pages/{title}.html', 
                    context={
                        'childRender': True,
                        'title': title.capitalize(),
                        str(title): dataQuerys.load_data_range(title, range=0)
                    }
            )

#* Forms
def REGISTRATION_APPOINTMENTS(request): 
    title: str = "Schedule an Appointment"
    formResult = formQuerys.register_client_and_appointment(request)
    if formResult is True: 
        return REDIRECT_HOME(request)
    elif isinstance(formResult, dict): 
        return render(request, "pages/clients/schedule-appointments.html",
                    context={
                        'childRender': True,
                        'title': title,
                        'client_form': formResult['client_form'],
                        'appointment_form': formResult['appointment_form'],
                    }
            )
    else:
        raise Exception("formResult did not returned a sufficient value")