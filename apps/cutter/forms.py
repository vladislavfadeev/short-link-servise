from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password



class RedirectPasswordForm(forms.Form):
    password = forms.CharField()
    encoded_pwd = forms.CharField()
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        encoded_pwd= cleaned_data.get('encoded_pwd')
        if not check_password(password, encoded_pwd):
            self.add_error('password', ValidationError('Password is not correct! Try again.'))
        return cleaned_data
        
        