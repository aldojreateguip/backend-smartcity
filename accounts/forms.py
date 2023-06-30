from django import forms
from .models import MPers, MUsua, SDire
# from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent',}),)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            try:
                user = MUsua.objects.get(usua_chlogusu=username)
                if not user.check_password(password):
                    self.add_error('password', 'Contraseña incorrecta')
            except MUsua.DoesNotExist:
                self.add_error('username', 'El nombre de usuario no existe')

        return cleaned_data

class MPersForm(forms.ModelForm):
    pers_chnomper = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    pers_chapeper = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    pers_chdocide = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    pers_chcelper = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    pers_chemaper = forms.CharField(
        max_length=300,
        widget=forms.EmailInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent', 'placeholder':'correo@dominio.com'}),
    )
    class Meta:
        model = MPers
        fields = ['pers_chnomper', 'pers_chapeper', 'pers_chdocide', 'pers_chemaper','pers_chcelper']

class MUsuaForm(forms.ModelForm):

    usua_chlogusu = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    usua_chpasusu = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    class Meta:
        model = MUsua
        fields = ['usua_chlogusu', 'usua_chpasusu']


class SDireForm(forms.ModelForm):
    dire_chnomdir = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    class Meta:
        model = SDire
        fields = ['dire_chnomdir']

class Step1Form(forms.Form):
    pers_chnomper = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    pers_chapeper = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    pers_chdocide = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    pers_chemaper = forms.CharField(
        max_length=300,
        widget=forms.EmailInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent', 'placeholder':'correo@dominio.com'}),
    )

class Step2Form(forms.Form):
    pers_chcelper = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    dire_chnomdir = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    usua_chlogusu = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )
    usua_chpasusu = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border-2 rounded-lg text-md border-gray-500 focus:ring-0 focus:border-2 focus:border-blue-500 focus:outline-none focus:placeholder-transparent'}),
    )


