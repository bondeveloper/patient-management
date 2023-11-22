from django.test import TestCase
from clinic.models import Patient
from django.urls import reverse


class PatientTests(TestCase):
  def setUp(self) -> None:
    self.patient = Patient(
      first_name='jane',
      last_name='doe' ,
      date_of_birth='1975-10-05',
      email='jane.doe@none.com',
      gender='female',
      street='1 purm street',
      city='cape town',
      postal_code=7800,
      occupation='surgeon',
      phone='0112345675',
      allergies='coffee,garlic'
    )
    self.patient.save()

  def test_patient_created(self):
    patient = Patient(
      first_name='john',
      last_name='doe' ,
      date_of_birth='1975-10-05',
      email='jane.doe@none.com',
      gender='female',
      street='1 purm street',
      city='cape town',
      postal_code=7800,
      occupation='surgeon',
      phone='0112345675'
    )

    patient.save()
    self.assertEquals(patient.first_name,'john')

    self.assertTrue(len(Patient.objects.all()) == 2)
  
  def test_patient_updated(self):
    self.assertEquals(self.patient.first_name, 'jane')
    self.patient.first_name = 'janet'
    self.patient.save(update_fields=['first_name'])

    self.assertEquals(self.patient.first_name, 'janet')

  def test_patient_deleted(self):
    self.patient.delete()
    self.assertTrue(len(Patient.objects.all()) == 0)
