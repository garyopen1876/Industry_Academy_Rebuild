from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Company, ContactPerson
from Industry_Academy.dictionaries import MESSAGE_DICT


# 公司
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'industry': forms.Select(attrs={'class': 'form-control can_edit'}),
            'uniform_numbers': forms.NumberInput(attrs={'class': 'form-control can_edit'}),
            'capital': forms.NumberInput(attrs={'class': 'form-control can_edit'}),
            'employee': forms.NumberInput(attrs={'class': 'form-control can_edit'}),
            'website': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'address': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'foreign': forms.Select(attrs={'class': 'form-control can_edit'}),
            'inter_ship_start': forms.DateInput(attrs={'class': 'form-control can_edit'}),
            'inter_ship_end': forms.DateInput(attrs={'class': 'form-control can_edit'}),
            'work_time': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'work_place': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'salary': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'welfare': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'explanation': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'interview': forms.Select(attrs={'class': 'form-control can_edit'}),
            'introduction': forms.ClearableFileInput(attrs={'class': 'form-control can_edit'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uniform_numbers'].validators.append(
            MinLengthValidator(8, MESSAGE_DICT.get('uniform_numbers_length_error')))
        self.fields['uniform_numbers'].validators.append(
            MaxLengthValidator(8, MESSAGE_DICT.get('uniform_numbers_length_error')))


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        exclude = ('user', 'all_email')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'email': forms.EmailInput(attrs={'class': 'form-control can_edit'}),
            'phone': forms.TextInput(attrs={'class': 'form-control can_edit'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].validators.append(MinLengthValidator(8, MESSAGE_DICT.get('phone_length_error')))