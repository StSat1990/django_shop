from django import forms

from products.models import FormModel


class FormModelForm(forms.ModelForm):
    class Meta:
        model = FormModel
        fields = ['username', 'city', 'comment']
