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
  province = models.CharField(max_length=255)
  postal_code = models.IntegerField()


class MedicalStaff(models.Model):
  POSITION_CHOICES = [
    ("doctor", "Doctor"),
    ("nurse", "Nurse"),
    ("director", "Director")
  ]
  user = models.ForeignKey(
    get_user_model(),
    on_delete=models.DO_NOTHING
  )
  phone = models.CharField(max_length=40)
  position = models.CharField(
    max_length=20,
    choices=POSITION_CHOICES
  )
  street = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  province = models.CharField(max_length=255)
  postal_code = models.IntegerField()
