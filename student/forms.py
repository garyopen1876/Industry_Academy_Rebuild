from django import forms
from django.core.validators import MinLengthValidator
from .models import Resume, Student
from Industry_Academy.dictionaries import MESSAGE_DICT


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('user',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'class_name': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'phone': forms.TextInput(attrs={'class': 'form-control can_edit'}),
            'email': forms.EmailInput(attrs={'class': 'form-control can_edit'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].validators.append(MinLengthValidator(8, MESSAGE_DICT.get('phone_length_error')))


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = "__all__"
