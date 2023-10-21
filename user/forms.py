from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.utils.translation import gettext_lazy as _

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic"]

        def clean_image(self):
            image = self.cleaned_data.get('profile_pic')
            if image:
                if image.size > 5*1024 * 1024:  # 1 MB as an example size limit
                    raise forms.ValidationError("Image size must be less than 1 MB.")
            return image

        # widgets = {
        #     "profile_pic":forms.FileInput(attrs={'class':'form-control'})
        # }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name','middle_name','last_name','address']

        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':_('First name')}),
            'middle_name':forms.TextInput(attrs={'class':'form-control','placeholder':_('Mirst name')}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':_('Lirst name')}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':_('Address')})
        }

