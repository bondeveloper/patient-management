from django.test import TestCase
from patient.models import Patient

def create_patient() -> Patient:
  return Patient.objects.create_patient(
      first_name='jane',
      last_name='doe' ,
      date_of_birth='0000/10/05',
      email='jane.doe@none.com',
      gender='female',
      street='1 purm street',
      city='cape town',
      province='western cape',
      postal_code=7800,
      occupation='surgeon',
      phone='0112345675'
    )

class PatientTests(TestCase):
  def test_patient_created(self):
    patient = create_patient()
    self.assertEquals(patient.email,'jane.doe@none.com')
    self.assertEquals(patient.street,'1 purm street')
    self.assertEquals(patient.date_of_birth,'0000/10/05')
    self.assertEquals(patient.phone,'0112345675')

    
