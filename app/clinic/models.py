from django.db import models
from django.contrib.auth import get_user_model
    

class Patient(models.Model):

  GENDER_CHOICES = [
    ("female", "Female"),
    ("male", "Male"),
  ]
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  date_of_birth = models.CharField(max_length=255)
  email = models.EmailField()
  phone = models.CharField(max_length=40)
  gender = models.CharField(
    max_length=6,
    choices=GENDER_CHOICES,
  )
  occupation = models.CharField(max_length=255)
  street = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  postal_code = models.IntegerField()
  allergies = models.CharField(max_length=255)

  def __str__(self) -> str:
    return f"{self.first_name} {self.last_name}"
  
  @classmethod
  def get_genders(self):
    return self.GENDER_CHOICES


class Doctor(models.Model):
  
  user = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE
  )
  phone = models.CharField(max_length=40)
  street = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  postal_code = models.IntegerField()
  department = models.CharField(max_length=100)

  def __str__(self) -> str:
     return f"{self.user.first_name} {self.user.last_name}"

class Consultation(models.Model):
  PATIENT_TYPE_CHOICES = [
      ('in', 'In Patient'),
      ('out', 'Out Patient')
    ]
  patient = models.ForeignKey(
    Patient,
    on_delete=models.DO_NOTHING
  )
  doctor = models.ForeignKey(
    Doctor,
    on_delete=models.DO_NOTHING
  )
  symptoms = models.CharField(max_length=40)
  illness = models.CharField(max_length=255)
  notes = models.CharField(max_length=255)
  patient_type = models.CharField(
    choices=PATIENT_TYPE_CHOICES,
    max_length=10
  )
  datetime = models.DateTimeField()

  def __str__(self) -> str:
     return f"{self.patient} {self.doctor}"

  @classmethod
  def get_patient_types(self):
    return self.PATIENT_TYPE_CHOICES
  
class Medication(models.Model):
  consultation = models.ForeignKey(
    Consultation,
    on_delete=models.CASCADE
  )
  name = models.CharField(max_length=100)
  instructions = models.CharField(max_length=255)
  start = models.DateField()
  end = models.DateField()
  datetime = models.DateTimeField()