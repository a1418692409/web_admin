from django import forms
from .zabbixtools import Zabbixtools
from pprint import pprint

class AddForm(forms.Form):
    host = Zabbixtools()
    # groupid_choices = [('2', 'Linux Server'), ('10', 'testing')]
    # templateid_choices = [('10001', 'Template OS Linux'), ('10050', 'Template App Zabbix Agent')]
    groupid_choices = host.hostgroup_get()
    templateid_choices = host.template_get()
    # pprint(templateid_choices)
    # pprint(groupid_choices)
    # type(groupid_choices)
    groupid_list = []
    templateid_list = []
    for item in groupid_choices:
        item = (item['groupid'], item['name'])
        groupid_list.append(item)
    # pprint(groupid_list)
    for template in templateid_choices:
        template = (template['templateid'], template['name'])
        templateid_list.append(template)
    # pprint(templateid_list)
    ip = forms.GenericIPAddressField()
    groupids = forms.ChoiceField(groupid_list)
    templateids = forms.ChoiceField(templateid_list)
    # def templateid(self, templateid_choices):
    #     templateids = forms.ChoiceField(templateid_choices)
    #     return templateids