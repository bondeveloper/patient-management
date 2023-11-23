from django.test import TestCase
from django.contrib.auth import get_user_model
from clinic.models import Appointment, Patient, Doctor


class ModelTests(TestCase):
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
      phone='0112345675'
    )
    self.patient.save()

    self.user = get_user_model().objects.create_user(
      email="janet@123.com",
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

    self.appointment = Appointment(
      patient=self.patient,
      doctor=self.doctor,
      symptoms='headache, fever, vomiting',
      illness='food poisoning',
      notes='went abroad for holidays and suspect might have had bed food.',
      patient_type='out',
      date='2023-11-22',
      time='16:17',
    )
    self.appointment.save()

  def test_appointment_created(self):
    self.assertTrue(len(Appointment.objects.all()) > 0)
  
  def test_appointment_updated(self):
    self.assertEquals(self.appointment.patient_type, 'out')
    self.appointment.patient_type = 'in'
    self.appointment.save(update_fields=['patient_type'])
    self.assertEquals(self.appointment.patient_type, 'in')

  def test_appointment_deleted(self):
    self.appointment.delete()
    self.assertTrue(len(Appointment.objects.all()) == 0)

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

  def test_patient_updated(self):
    self.assertEquals(self.patient.first_name, 'jane')
    self.patient.first_name = 'janet'
    self.patient.save(update_fields=['first_name'])

    self.assertEquals(self.patient.first_name, 'janet')

  def test_patient_deleted(self):
    self.patient.delete()
    self.assertTrue(len(Patient.objects.all()) == 0)