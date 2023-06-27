from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redireccionar a la página de inicio o a la siguiente página deseada
                return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'login/login.html', {'form': form})

def register_view(request):

    return render(request, "register/register.html")