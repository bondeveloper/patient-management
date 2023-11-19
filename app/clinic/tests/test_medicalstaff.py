from django.test import TestCase
from clinic.models import MedicalStaff
from django.contrib.auth import get_user_model


class MedicalStaffTest(TestCase):
  def setUp(self) -> None:
    self.user = get_user_model().objects.create_user(
      email="jane@123.com",
      password="123123"
    )
    self.staff = MedicalStaff(
      user=self.user,
      phone='192392734',
      street='3 tres road',
      position='doctor',
      city='cape town',
      postal_code=7800,
      department='neuro-surgery'
    )

    self.staff.save()
  
  def test_staff_created(self):
    staff = MedicalStaff.objects.get(pk=1)
    self.assertEquals(staff.position, 'doctor')

  def test_staff_updated(self):
    self.assertEquals(self.staff.position, 'doctor')
    self.staff.position = 'nurse'
    self.staff.save()
    self.assertEquals(self.staff.position, 'nurse')

  def test_staff_deleted(self):
    self.assertTrue(len(MedicalStaff.objects.all()) == 1)
    self.staff.delete()
    self.assertTrue(len(MedicalStaff.objects.all()) == 0)