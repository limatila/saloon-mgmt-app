from django.shortcuts import render, redirect

# Create your views here.

def redirectHome(request):
    return redirect('home')

def home(request):
    return render(request, 'pages/home.html', 
                        context={
                            
                        }
            )