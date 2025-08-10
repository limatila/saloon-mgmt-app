from django.shortcuts import render, redirect

# Create your views here.

def REDIRECT_HOME(request):
    return redirect('home')

def HOME(request, base: bool = False):
    title: str = "Home"
    if base: title = "Base"
    return render(request, 'pages/home.html', 
                        context={
                            'baseRender': base,
                            'childRender': (not base),
                            'title': title
                        }
            )

def APPOINTMENTS(request):
    title: str = "Appointments"
    return render(request, 'pages/appointments.html', 
                        context={
                            'childRender': True,
                            'title': title
                        }
            )

def WORKERS(request):
    title: str = "Workers"
    return render(request, 'pages/workers.html', 
                        context={
                            'childRender': True,
                            'title': title
                        }
            )

def BASE(request):
    return HOME(request, True)