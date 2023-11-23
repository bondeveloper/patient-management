from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from clinic.models import Patient, Doctor
from django.urls import reverse
import json
import logging

logger = logging.getLogger(__name__)

class ApiTest(TestCase):
  
  def setUp(self) -> None:
    self.client = Client()

    self.user = get_user_model().objects.create_user(
      email="janet2@123.com",
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


  def test_making_appointment(self):
    logger.error(self.doctor)
    url = reverse('create_appointment')
    payload = {
      "id_patient": self.patient.id,
      "id_doctor": self.doctor.id,
      "date": '2023-11-22',
      "time": '12:00'
    }

    res = self.client.post(url, json.dumps(payload), content_type="application/json")
    self.assertTrue(res.json().get('success'))

  def test_get_users(self):
    url = reverse('get_users')
    res = self.client.get(url+'?term=jan&_type=query&q=jan', content_type="application/json")
    self.assertTrue(len(res.json()) == 1)

  def test_get_doctors(self):
    url = reverse('get_doctors')
    res = self.client.get(url+'?term=jan&_type=query&q=jan', content_type="application/json")
    self.assertTrue(len(res.json()) == 1)