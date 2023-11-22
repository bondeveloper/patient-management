from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from clinic.models import Appointment, Patient, Doctor
from django.urls import reverse
import json


class AppointmentTests(TestCase):
  def setUp(self) -> None:
    self.client = Client()
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
    self.client.force_login(self.user)

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

  def test_making_appointment(self):
    url = reverse('doctor_appointments_create')
    payload = {
      "id_patient": self.patient.id,
      "symptoms":'headache, fever, vomiting',
      "illness":'food poisoning',
      "notes":'went abroad for holidays and suspect might have had bed food.',
      "patient_type":'out patient',
      "date": '2023-11-22',
      "time": '12:00'
    }
    res = self.client.post(url, json.dumps(payload), content_type="application/json")
    self.assertTrue(res.json().get('success'))

