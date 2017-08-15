from django import forms

class AddForm(forms.Form):
    ip = forms.GenericIPAddressField()
    groupid = forms.ChoiceField(choices=[('2','Linux Server'),('10','testing')])
    templateid = forms.ChoiceField(choices=[('10001','Template OS Linux'),('10050','Template App Zabbix Agent')])