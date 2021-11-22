from django import forms
from django.core import validators


# 聯絡
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    from_email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    subject = forms.CharField(required=True)


# 修改密碼
class ChangePasswordForm(forms.Form):
    old = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control can_edit'}))
    new = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control can_edit'}),
                          validators=[validators.MinLengthValidator(limit_value=8)])
    check = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control can_edit'}))