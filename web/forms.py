from django import forms
from .models import Message


# 公佈欄
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"


# 聯絡
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    from_email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    subject = forms.CharField(required=True)
