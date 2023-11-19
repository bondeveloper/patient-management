from django.test import TestCase
from clinic.models import Doctor
from django.contrib.auth import get_user_model


class DoctorsTest(TestCase):
  def setUp(self) -> None:
    self.user = get_user_model().objects.create_user(
      email="jane@123.com",
      password="123123"
    )
    self.doctor = Doctor(
      user=self.user,
      phone='192392734',
      street='3 tres road',
      city='cape town',
      postal_code=7800,
      department='neuro-surgery'
    )

    self.doctor.save()
  
  def test_doctor_created(self):
    doctor = Doctor.objects.get(pk=self.doctor.id)
    self.assertEquals(doctor.department, 'neuro-surgery')

  def test_doctor_updated(self):
    self.assertEquals(self.doctor.department, 'neuro-surgery')
    self.doctor.department = 'general-surgery'
    self.doctor.save()
    self.assertEquals(self.doctor.department, 'general-surgery')

  def test_doctor_deleted(self):
    self.assertTrue(len(Doctor.objects.all()) == 1)
    self.doctor.delete()
    self.assertTrue(len(Doctor.objects.all()) == 0)