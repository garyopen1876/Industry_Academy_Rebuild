from django import forms
from .models import Company


# 公司
class CompanyForm(forms.Form):
    class Meta:
        model = Company
        fields = "__all__"
