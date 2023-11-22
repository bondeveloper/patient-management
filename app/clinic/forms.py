from collections.abc import Mapping
from django import forms
from .models import Appointment, Patient, Doctor

class AppointmentCreationForm(forms.ModelForm):

  class Meta:
    model = Appointment
    fields = ["date", "time", "patient"]

  
  def __init__(self, *args, **kwaargs):
    super().__init__(*args, **kwaargs)
    self.fields['patient'].queryset = Patient.objects.none()


class BaseDoctorModelForm(forms.ModelForm):

  class Meta:
    model = Doctor
    fields = ('user', 'phone', 'department', 'street', 'city', 'postal_code')

    widgets = {
      'phone': forms.TextInput(attrs={'class': 'form-control'}),
      'street': forms.TextInput(attrs={'class': 'form-control'}),
      'city': forms.TextInput(attrs={'class': 'form-control'}),
      'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
      'department': forms.TextInput(attrs={'class': 'form-control'})
    }

  
class CreateDoctorModelForm(BaseDoctorModelForm):

  class Meta(BaseDoctorModelForm.Meta):
    fields = ('user', 'phone', 'department', 'street', 'city', 'postal_code')


class UpdateDoctorModelForm(BaseDoctorModelForm):

  class Meta(BaseDoctorModelForm.Meta):
    fields = ('phone', 'department', 'street', 'city', 'postal_code')