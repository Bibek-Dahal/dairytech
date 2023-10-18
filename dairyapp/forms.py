import datetime
from django import forms
from .models import *
from my_account.models import User
from .custom_widget import DateInput
from utils.dairyapp.commonutils import getShift
from django.utils.translation import gettext_lazy as _



class CreateFatForm(forms.ModelForm):

    # fat_rate = forms.FloatField(widget=forms.NumberInput(attrs={"class": "form-control","placeholder":"enter your email"}))
    dairy = forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={"class":"form-control","maxlength":6}))
    # foo_select = forms.ModelMultipleChoiceField(queryset=None)
    bonous_amount = forms.CharField(initial=0,label=_("Bonus amount"),widget=forms.NumberInput(attrs={'class':'form-control'}))
    # created_at = forms.DateField(label=_("Created At"),widget=DateInput(attrs={"class":"form-control date-picker","placeholder":"dd-mm-yyyy"},format="%Y-%m-%d"))
    def __init__(self,request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        print("------------")
        self.fields["dairy"].queryset = Dairy.objects.filter(user=request.user)
        instance = kwargs.get('instance')
        
        # Exclude 'created_at' field when creating a new instance
        if instance is None:
            self.fields.pop('created_at')
        
    class Meta:
        model = FatRate
        fields = ["fat_rate","dairy","bonous_amount","created_at"]

        widgets ={
            # 'country':CountrySelectWidget(attrs={"class": "form-select"}),
            'created_at':forms.DateInput(attrs={"class":"form-control date-picker","placeholder":"dd-mm-yyyy"},format="%Y-%m-%d"),
            'fat_rate':forms.NumberInput(attrs={"class": "form-control","placeholder":"enter fat rate"}),
            # 'bonous_amount':forms.NumberInput(attrs={'class':'form-control'})
            # 'dairy':forms.ChoiceField(widget=forms.ModelChoiceIterator())
            # 'username':forms.TextInput(attrs={"class": "form-control","placeholder":"enter your name","minlength":3})
            #'password':forms.PasswordInput(attrs={"class": "form-control"})
        }

    def clean_fat_rate(self):
        fat_rate = self.cleaned_data['fat_rate']
        if fat_rate < 0:
            raise forms.ValidationError(_('fat rate should be positive'))
        
        return fat_rate
    

class CreateDairyForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(label=_("Members"),required=False,queryset=User.objects.filter(is_active=True),widget=forms.SelectMultiple(attrs={"class": "form-control dairy-member-select"}))
    class Meta:
        model = Dairy
        fields = ["name","location","members"]

        widgets = {
            'name':forms.TextInput(attrs={"class": "form-control","placeholder":"Enter dairy name","maxlength":200}),
            'location':forms.TextInput(attrs={"class": "form-control","placeholder":"Enter dairy location"}),
            # 'members': forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True),widget=forms.SelectMultiple(attrs={"class": "form-control"}))
        }

import datetime

class CreateMilkRecordForm(forms.ModelForm):
    shiftinfo = getShift()
    # if 
    print("shift info",shiftinfo)
    user = forms.ModelChoiceField(label=_("User"),queryset=None,initial=1,widget=forms.Select(attrs={"class":"form-select"}))
    dairy = forms.ModelChoiceField(label=_("Dairy"),queryset=None,initial=1,widget=forms.Select(attrs={"class":"form-select"}))
    date = forms.DateField(label=_("Date"),widget=forms.DateInput(attrs={"class":"form-control date-picker","placeholder":"dd-mm-yyyy","data-single":'true'},format="%Y-%m-%d"))
    shift = forms.ChoiceField(label=_("Shift"),widget=forms.Select(attrs={"class":"form-select"}),initial=shiftinfo,choices=MilkRecord.shift_choices)
    # input_formats=['%Y%m%d']
    class Meta:
        model = MilkRecord
        fields = ["shift","dairy","user","milk_weight","milk_fat","date"]

        widgets = {
            # 'shift':forms.Select(attrs={"class":"form-select"}),
            # 'date':forms.DateInput()
            'milk_weight':forms.NumberInput(attrs={"class":"form-control"}),
            'milk_fat':forms.NumberInput(attrs={"class":"form-control","min":"0"}),
        }
    def __init__(self,dairy,user,*args, **kwargs):
        super().__init__(*args, **kwargs)
        print("------------")
        self.fields["user"].queryset = dairy.members.all().filter(id=user.id)
        self.fields["dairy"].queryset = Dairy.objects.filter(id=dairy.id)
        print("last of init")
    
    

    def clean_milk_fat(self):
        value = float(self.cleaned_data['milk_fat'])
        lower_bound = 0
        upper_bound = 20
        
        if  (lower_bound <= value <=upper_bound):
            return self.cleaned_data['milk_fat']
        
        raise forms.ValidationError(_("Milk fat should be between %(low_range)d and %(high_range)d") % {'low_range':0,'high_range':20})


class UpdateMilkRecord(forms.ModelForm):
    
    # user = forms.ModelChoiceField(queryset=None,initial=1,widget=forms.Select(attrs={"class":"form-select"}))
    # dairy = forms.ModelChoiceField(queryset=None,initial=1,widget=forms.Select(attrs={"class":"form-select"}))
    # date = forms.DateField(initial=datetime.datetime.now(),widget=DateInput(attrs={"class":"form-control date-picker","placeholder":"dd-mm-yyyy"},format="%Y-%m-%d"))
    # shift = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select"}),choices=MilkRecord.shift_choices)
    # input_formats=['%Y%m%d']
    date = forms.DateField(label=_("Date"),widget=forms.DateInput(attrs={"class":"form-control date-picker","placeholder":"dd-mm-yyyy","data-single":'true'},format="%Y-%m-%d"))
    class Meta:
        model = MilkRecord
        fields = ["shift","dairy","user","milk_weight","milk_fat","date"]

        widgets = {
            'date':DateInput(attrs={"class":"form-control date-picker","placeholder":"dd-mm-yyyy"},format="%Y-%m-%d"),
            'user':forms.Select(attrs={"class":"form-select"}),
            'dairy':forms.Select(attrs={"class":"form-select"}),
            'shift':forms.Select(attrs={"class":"form-select"}),
            'milk_weight':forms.NumberInput(attrs={"class":"form-control"}),
            'milk_fat':forms.NumberInput(attrs={"class":"form-control","min":"0"}),
        }
    
    
    

    def clean_milk_fat(self):
        value = float(self.cleaned_data['milk_fat'])
        lower_bound = 0
        upper_bound = 20
        
        if  (lower_bound <= value <=upper_bound):
            return self.cleaned_data['milk_fat']
        
        raise forms.ValidationError(_("Milk fat should be between %(low_range)d and %(high_range)d") % {'low_range':0,'high_range':20})

# class CreateMilkRecordFormSet(forms.BaseFormSet):
#     def __init__(self, dairy, *args, **kwargs):
#         self.dairy = dairy
#         super().__init__(*args, **kwargs)

#     def get_form_kwargs(self, index):
#         kwargs = super().get_form_kwargs(index)
#         kwargs['dairy'] = self.dairy  # Pass 'dairy' as a keyword argument to the form constructor
#         return kwargs