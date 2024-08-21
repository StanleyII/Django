from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password_one = forms.CharField(max_length=65, widget=forms.PasswordInput)
    password_two = forms.CharField(max_length=65, widget=forms.PasswordInput)
