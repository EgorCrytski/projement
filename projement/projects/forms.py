from django.forms.models import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from projects.models import Project, Log
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class LogForm(forms.Form):
    actual_design = forms.DecimalField(decimal_places=2)
    actual_development = forms.DecimalField(decimal_places=2)
    actual_testing = forms.DecimalField(decimal_places=2)

    def clean_actual_design(self):
        data = self.cleaned_data['actual_design']
        if data < 0 or data > 9999.9:
            raise ValidationError(_('Invalid value'))
        return data

    def clean_actual_development(self):
        data = self.cleaned_data['actual_development']
        if data < 0 or data > 9999.9:
            raise ValidationError(_('Invalid value'))
        return data

    def clean_actual_testing(self):
        data = self.cleaned_data['actual_testing']
        if data < 0 or data > 9999.9:
            raise ValidationError(_('Invalid value'))
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'UPDATE'))


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['actual_design', 'actual_development', 'actual_testing']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'UPDATE'))
