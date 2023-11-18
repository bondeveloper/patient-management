from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

class UserModelTests(TestCase):
  def setUp(self):
    self.user = get_user_model().objects.create_user(email='user@patient.com', password='123123')

  def test_user_created_using_email(self):
    self.assertEqual(self.user.email, 'user@patient.com')
  
  def test_admin_user_created(self):
    user = get_user_model().objects.create_superuser(email='admin@patient.com', password='123123')
    self.assertEqual(user.email, 'admin@patient.com')

  def test_user_created_existing_email_fails(self):
    self.assertRaises(IntegrityError, get_user_model().objects.create_user, email='user@patient.com')

  def test_user_updated(self):
    self.assertEquals(self.user.first_name, '')
    self.user.first_name = 'jane'
    self.user.save()

    self.assertEquals(self.user.first_name, 'jane')

  def test_user_deleted(self):
    self.assertTrue(len(get_user_model().objects.all()) == 1)
    self.user.delete()
    self.assertTrue(len(get_user_model().objects.all()) == 0)