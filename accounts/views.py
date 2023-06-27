from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import LoginForm, MPersForm, MUsuaForm
from .backends import MUsuaBackend

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = MUsuaBackend().authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Cambia 'home' por la URL de tu página principal
            else:
                form.add_error(None, 'Credenciales inválidas')  # Mensaje de error si las credenciales son inválidas
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        pers_form = MPersForm(request.POST)
        usua_form = MUsuaForm(request.POST)
        if pers_form.is_valid() and usua_form.is_valid():
            pers = pers_form.save()
            usua = usua_form.save(commit=False)
            usua.pers_f_incodper = pers
            usua.save()
            return redirect('login')
    else:
        pers_form = MPersForm()
        usua_form = MUsuaForm()

    return render(request, 'register/register.html', {'pers_form': pers_form, 'usua_form': usua_form})