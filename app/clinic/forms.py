from collections.abc import Mapping
from django import forms
from .models import Appointment, Patient

class AppointmentCreationForm(forms.ModelForm):

  class Meta:
    model = Appointment
    fields = ["date", "time", "patient"]

  
  def __init__(self, *args, **kwaargs):
    super().__init__(*args, **kwaargs)
    self.fields['patient'].queryset = Patient.objects.none()