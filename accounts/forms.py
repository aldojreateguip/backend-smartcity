from django import forms
from .models import MPers, MUsua
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent',}),)

class MPersForm(forms.ModelForm):
    pers_chnomper = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    pers_chapeper = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    pers_chdocide = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    pers_chcelper = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    pers_chemaper = forms.CharField(
        max_length=300,
        widget=forms.Textarea(attrs={'class': 'form-textarea'}),
    )
    class Meta:
        model = MPers
        fields = ['pers_chnomper', 'pers_chapeper', 'pers_chdocide', 'pers_chcelper', 'pers_chemaper']

class MUsuaForm(forms.ModelForm):
    usua_chlogusu = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    usua_chpasusu = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    class Meta:
        model = MUsua
        fields = ['usua_chlogusu', 'usua_chpasusu']