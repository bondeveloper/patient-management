from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTests(TestCase):
  def test_user_created_using_email(self):
    user = get_user_model().objects.create_user(email='user@patient.com', password='123123')

    self.assertEqual(user.email, 'user@patient.com')
  
  def test_admin_user_created(self):
    user = get_user_model().objects.create_superuser(email='admin@patient.com', password='123123')
    
    self.assertEqual(user.email, 'admin@patient.com')