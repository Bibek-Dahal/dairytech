from allauth.account.adapter import DefaultAccountAdapter
import re
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from my_account.models import User

class MyAccountAdapter(DefaultAccountAdapter):
    # def clean_email(self, email):
    #     email =  super().clean_email(email)
    #     print("self",self)
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError(_('User with email address already exists.'))
    #     return email

    def reset_password(self, request, user):
        # Override the reset_password method to skip the email check
        return super().reset_password(request, user)

    def clean_password(self, password, user=None):
        password =  super().clean_password(password, user)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            # pat = re.compile(reg)
        match = re.match(reg, password)
        if not match:
            raise ValidationError(_('Password must contain at least one digit, special characrers and uppercase letter'))
        
        return password
    
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        print("form data",data)
        user =  super().save_user(request, user, form, False)
        user.first_name = data['first_name']
        user.middle_name = data['middle_name']
        user.last_name = data['last_name']
        user.phone_number = data['phone_number']
        return super().save_user(request, user, form, commit)
