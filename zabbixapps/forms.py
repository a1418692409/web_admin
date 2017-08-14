from django import forms

class AddForm(forms.Form):
    ip = forms.GenericIPAddressField()