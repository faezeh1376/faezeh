from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15,label='شماره تلفن')
    address = forms.CharField(max_length=200,label='ادرس')
    code_posti = forms.CharField(max_length=15,label='کد پستی')

    first_name = forms.CharField(max_length=100,label='نام')
    last_name = forms.CharField(max_length=100,label='نام خانوادگی')
    
    password1 = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    class Meta:
        model = User
        fields = ('username',  'password1', 'password2','first_name', 'last_name' ,'email','phone_number','address','code_posti')
        labels = {

            'username':'نام کاربری',
            'email':"پست الکترونیکی"
            
        }
        error_messages = {
            'username': {
                'max_length': _("طول زیاد است"),
            },
        }