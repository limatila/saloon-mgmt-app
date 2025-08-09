from django.shortcuts import render, redirect

# Create your views here.

def redirectHome(request):
    return redirect('home')

def home(request, base: bool = False):
    title: str = "Home"
    if base: title = "Base"
    return render(request, 'pages/home.html', 
                        context={
                            'baseRender': base,
                            'childRender': (not base),
                            'title': title
                        }
            )

def base(request):
    return home(request, True)