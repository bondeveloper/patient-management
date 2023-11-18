from django.db import models

class PatientManager(models.Manager):
  def create_patient(self, **kwargs):
    return self.create(**kwargs)
    

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


  objects = PatientManager()
