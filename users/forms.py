from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms



class Account(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

    def __init__(self, *args,**kwargs):
        super(Account,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control mt-2 mb-2'})
            field.help_text = ""


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)
