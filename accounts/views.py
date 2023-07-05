from django.shortcuts import redirect, render
from django.contrib.auth import login, logout as django_logout
from django.contrib.auth.models import AnonymousUser
from .forms import LoginForm,MPersForm,MUsuaForm,Step1Form,Step2Form,SDireForm
from .backends import MUsuaBackend
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)
            user = MUsuaBackend().authenticate(request, username=username, password=password)

            if user is not None:
                user.backend = f"{MUsuaBackend.__module__}.{MUsuaBackend.__name__}"
                login(request, user, backend=f"{MUsuaBackend.__module__}.{MUsuaBackend.__name__}")
                return redirect('dashboard')  
            else:
                return JsonResponse({'success': False, 'errorslog': 'Credenciales Incorrectas'})
        else:
            return JsonResponse({'success': False, 'errorslog': 'credenciales Incorrectas'})
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    # Realiza aquí las acciones personalizadas de cierre de sesión
    # Por ejemplo, puedes agregar registro de actividad, limpiar datos de la sesión personalizados, etc.
    
    # Llama a la función de cierre de sesión de Django
    django_logout(request)
    
    # Restablece el usuario a AnonymousUser
    request.user = AnonymousUser()
    
    # Redirige a la página de inicio de sesión u otra página de tu elección
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = Step1Form(request.POST)
        if form.is_valid():
            request.session['step1_data'] = form.cleaned_data
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errorsw': form.errors})
    else:
        form = Step1Form()
        form2 = Step2Form()

    return render(request, 'register/register.html', {'form': form, 'form2': form2})


def register_step2_view(request):
    step1_data = request.session.get('step1_data', {})
    if step1_data is not None:
        if request.method == 'POST':
            form = Step2Form(request.POST)
            step1_data['pers_chcelper'] = request.POST.get('pers_chcelper', '')
            if form.is_valid():
                pers_form = MPersForm(data=step1_data)
                usua_form = MUsuaForm(request.POST)
                dire_form = SDireForm(request.POST)
                if pers_form.is_valid() and usua_form.is_valid() and dire_form.is_valid():
                    dire = dire_form.save(commit=False)
                    dire.esta_f_incodest = 1
                    dire.save()
                    dire_pk = dire.dire_p_incodper
                    pers = pers_form.save(commit=False)
                    pers.dire_f_incodper = dire_pk
                    pers.tipo_f_incodper = 2
                    pers.save()

                    pers_pk = pers.pers_p_incodper

                    usua = usua_form.save(commit=False)
                    usua.pers_f_incodper = pers_pk
                    usua.tipo_f_incodusu = 1
                    usua.save()

                    del request.session['step1_data']
                    return redirect('login')
                else:
                    return JsonResponse({'success': False, 'errors': pers_form.errors})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            form = Step2Form()
    else:
        return JsonResponse({'success': False})
    return render(request, 'register/register.html', {'form': form})
