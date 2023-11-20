from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Appointment, Patient

class AppointmentCreationForm(forms.ModelForm):

  class Meta:
    model = Appointment
    fields = ["date", "time", "patient"]

  
  def __init__(self, *args, **kwaargs):
    super().__init__(*args, **kwaargs)
    self.fields['patient'].queryset = Patient.objects.none()