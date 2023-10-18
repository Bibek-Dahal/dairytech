from django.forms import CharField, ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _
import re
from my_account.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from allauth.account.forms import SignupForm,LoginForm,ChangePasswordForm,ResetPasswordKeyForm,ResetPasswordForm,SetPasswordForm,AddEmailForm
from allauth.account import app_settings

# from django.contrib.auth.forms import UserCreationForm


class MyAddEmailForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super(MyAddEmailForm, self).__init__(*args, **kwargs)
        
        # self.fields['oldpassword'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MySetPasswordForm, self).__init__(*args, **kwargs)
        
        # self.fields['oldpassword'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})
    pass



class MyPasswordResetFormKey(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordResetFormKey, self).__init__(*args, **kwargs)
        
        # self.fields['oldpassword'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})
    



class MyPasswordResetFrom(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordResetFrom, self).__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        
   

class MyPasswordChangeForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.label = _("Current Password")
        self.fields['password1'].widget.label = _("New Password")
        self.fields['password2'].widget.label = _("New Password (again)")

        self.fields['oldpassword'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})




class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        
        self.fields['password'].widget.attrs.update({'class':'form-control'})
        self.fields['login'].widget.attrs.update({'autofocous':True,'class':'form-control'}) 
        self.fields['remember'].widget.attrs.update({'class':'d-inline'})   



class MyUserCreationForm(SignupForm):
    
    # email = forms.EmailField(
    #     label= _("email"),
    #     widget=forms.TextInput(
            
    #         attrs={
    #             "type": "email",
    #             "placeholder": _("E-mail address"),
    #             "autocomplete": "email",
    #             "class":"form-control"
    #         }
    #     )
    # )
    first_name = CharField(label=_("First name"),max_length=20,min_length=2,widget=forms.TextInput(attrs={'class':'form-control','placeholder':_("First name")}))
    middle_name = CharField(label=_("Middle name"),required=False,max_length=20,min_length=2,widget=forms.HiddenInput(attrs={'class':'form-control','placeholder':_("Middle name")}))
    last_name = CharField(label=_("Last name"),max_length=20,min_length=2,widget=forms.TextInput(attrs={'class':'form-control','placeholder':_("Last name")}))
    phone_number = CharField(label=_("Phone number"),widget=forms.NumberInput(attrs={'class':'form-control','maxlength':10,'minlength':10,'placeholder':_("Phone number")}))
    field_order = ["first_name","middle_name","phone_number","password1","last_name","email","password2"]
    
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'autofocous':'autofocous','class':'form-control'}) 
        # = forms.PasswordInput(render_value=False,attrs={'class': 'form-control'})
        # self.field_order = ['email', 'first_name', 'middle_name','last_name','password1','password2'] 
        
        
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields['password2'].widget.attrs.update({'class':'form-control'}) 
            
            # PasswordField(
            #     label=_("Password (again)"), autocomplete="new-password"
            # )
        
        



    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False,attrs={'class':'form-control','maxlength':100}))
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput(render_value=False,attrs={'class':'form-control','maxlength':100})
    )
    
    # phone_number = forms.IntegerField(validators=[RegexValidator('^\d{10}$',message=_("please enter a valid phone number"))])
    

    # class Meta:
    #     model = User
    #     fields = [_("email"),_("first_name"),_("middle_name"),_("last_name"),_("phone_number"),]

    #     widgets = {
    #         'first_name':forms.TextInput(attrs={'class':'form-control','maxlength':50,'minlenght':2}),
    #         'middle_name':forms.TextInput(attrs={'class':'form-control','maxlength':50,'minlenght':2}),
    #         'last_name':forms.TextInput(attrs={'class':'form-control','maxlength':50,'minlenght':2}),
    #         'phone_number':forms.NumberInput(attrs={'class':'form-control','maxlength':10,'minlength':10}),
    #         'email':forms.EmailInput(attrs={'class':'form-control','maxlength':100,})
    #     }

    # def clean_password2(self):
        
    #     cleaned_data = super(MyUserCreationForm, self).clean()
    #     print("cleanded data",cleaned_data)
    #     # Check that the two password entries match
        
    #     password2 = cleaned_data.get("password2")   
    #     # if password1 and password2 and password1 != password2:
    #     #     raise ValidationError("Passwords don't match")
    #     if len(password2) >= 8:
    #         reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    #         # pat = re.compile(reg)
    #         match = re.match(reg, password2)
    #         if not match:
    #             raise ValidationError('Password must contain at least one digit, special characrers and uppercase letter')
        
        

        # return password2
    
    def clean_phone_number(self):
        
        print("===========")
        # print(cleaned_data)
        phone_number = self.cleaned_data['phone_number']
        print("phone_number",phone_number)
        
            # Validate the phone number using the regex pattern
        if not re.search("^\d{10}$", str(phone_number)):
            raise ValidationError(_("Please enter a valid 10-digit phone number."))
        
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError(_("User with phone numbre already exists"))
        return phone_number
    
    def clean_email(self):
        email =  super().clean_email()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('User with email address already exists.'))
        return email
        


    # def save(self,commit=True):
    #     # Save the provided password in hashed format
    #     # user = super().save(commit=False)
    #     print("+++++++++++++++++++")
    #     print(self.cleaned_data["first_name"])
    #     # user = User.objects.create_user(
    #     #     phone_number=int(self.cleaned_data["phone_number"]),
    #     #     first_name=self.cleaned_data["first_name"],
    #     #     last_name=self.cleaned_data["last_name"],
    #     #     password=self.cleaned_data["password1"],
    #     #     middle_name = self.cleaned_data["middle_name"],
    #     #     address = self.cleaned_data["address"],
    #     #     email = self.cleaned_data["email"]

    #     # )

    #     # Call the parent class's save() method first
    #     user = super().save(commit=False)
    #     user.is_active = False
    #     user.set_password(self.cleaned_data["password1"])
    #     user.save()

    #     # if commit:
    #     #     user.save()
    #     return user

class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = "__all__"

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Validate the phone number using the regex pattern
            if not re.search("^\d{10}$", str(phone_number)):
                raise ValidationError(_("Please enter a valid 10-digit phone number."))

        return phone_number
        