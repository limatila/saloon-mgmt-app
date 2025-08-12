from django.shortcuts import render, redirect

from saloon.views.querys import dataQuerys, formQuerys

# Create your views here.

#Rediractions
def REDIRECT_HOME(request):
    return redirect('home')
def REDIRECT_ADMIN(request):
    return redirect('admin')
def BASE(request):
    return HOME(request, True)

#Render
def HOME(request, base: bool = False):
    title: str = "Home"
    if base: title = "Base"
    return render(request, 'pages/home.html', 
                    context={
                        'baseRender': base,
                        'childRender': (not base),
                        'title': title,
                        'workers': dataQuerys.load_data_range('worker', range=8, offset=0),
                        
                        'appointments': dataQuerys.load_all_appointments_today(),
                        'qtt_ongoing_hour': dataQuerys.load_ongoing_appointments_next_hour(),
                        'qtt_finished_today': dataQuerys.load_finished_appointments_today(),
                        'value_revenue_today': dataQuerys.load_revenue_today(),
                    }
            )

def APPOINTMENTS(request):
    title: str = "Appointments"
    return render(request, 'pages/appointments.html', 
                    context={
                        'childRender': True,
                        'title': title,
                        'appointments': dataQuerys.load_data_range('appointment', range=0),
                    }
            )

def WORKERS(request):
    title: str = "Workers"
    return render(request, 'pages/workers.html', 
                    context={
                        'childRender': True,
                        'title': title,
                        'workers': dataQuerys.load_data_range('worker', range=0),
                    }
            )

def REGISTRATION_APPOINTMENTS(request): 
    return render(request, "pages/clients/schedule-appointments.html")