from django import forms
from .zabbixtools import Zabbixtools
from pprint import pprint

class AddForm(forms.Form):
    host = Zabbixtools()
    # groupid_choices = [('2', 'Linux Server'), ('10', 'testing')]
    templateid_choices = [('10001', 'Template OS Linux'), ('10050', 'Template App Zabbix Agent')]
    groupid_choices = host.hostgroup_get()
    # pprint(groupid_choices)
    # type(groupid_choices)
    for item in groupid_choices:
        item = tuple(item)
    pprint(groupid_choices)
    ip = forms.GenericIPAddressField()
    groupids = forms.ChoiceField(groupid_choices)
    templateids = forms.ChoiceField(templateid_choices)
    # def templateid(self, templateid_choices):
    #     templateids = forms.ChoiceField(templateid_choices)
    #     return templateids