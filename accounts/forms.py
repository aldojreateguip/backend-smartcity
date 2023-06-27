from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    # username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={'class:': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent',}),)
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    #Example in tailwindCSS como colocar estilo, solo reemplazar la propiedad widget en el codigo arriba
    #widget=forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),

    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent',}),)
