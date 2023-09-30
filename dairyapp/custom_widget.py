from django import forms

class DateInput(forms.DateInput):
    input_type = "date"
    # format = "%m/%d/%Y"
    # format = "%Y-%m-%d"
    
