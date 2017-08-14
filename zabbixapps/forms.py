from django import forms

class AddForm(forms.Form):
    a = forms.GenericIPAddressField()