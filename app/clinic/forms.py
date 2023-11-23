from django import forms
from .models import Appointment, Patient, Doctor


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


class CreatePatientModelForm(forms.ModelForm):


    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
          'first_name': forms.TextInput(attrs={'class': 'form-control'}),
          'last_name': forms.TextInput(attrs={'class': 'form-control'}),
          'date_of_birth': forms.DateInput(format=('%Y-%m-%d'),
                  attrs={'class': 'form-control',
                   'placeholder': 'Select a date',
                   'type': 'date'
                  }),
          'email': forms.EmailInput(attrs={'class': 'form-control'}),
          'phone': forms.TextInput(attrs={'class': 'form-control'}),
          'gender': forms.Select(attrs={'class': 'form-control'}),
          'occupation': forms.TextInput(attrs={'class': 'form-control'}),
          'allergies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma separated list'}),
          'street': forms.TextInput(attrs={'class': 'form-control'}),
          'city': forms.TextInput(attrs={'class': 'form-control'}),
          'postal_code': forms.NumberInput(attrs={'class': 'form-control'})
        }

class UpdateAppointmentModelForm(forms.ModelForm):


    class Meta:
        model = Appointment
        fields = ('patient_type', 'symptoms', 'illness', 'notes')
        widgets = {
          'patient_type': forms.TextInput(attrs={'class': 'form-control'}),
          'symptoms': forms.TextInput(attrs={'class': 'form-control'}),
          'illness': forms.TextInput(attrs={'class': 'form-control'}),
          'notes': forms.Textarea(attrs={'class': 'form-control'})
        }
