import django.forms as forms
from eReservation.models import Table


class AddTableForm(forms.ModelForm):
    class Meta:
        model = Table
        exclude = ["restaurant"]