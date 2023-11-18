from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class UserModelTests(TestCase):
  def test_user_created_using_email(self):
    user = get_user_model().objects.create_user(email='user@patient.com', password='123123')

    self.assertEqual(user.email, 'user@patient.com')
  
  def test_admin_user_created(self):
    user = get_user_model().objects.create_superuser(email='admin@patient.com', password='123123')
    
    self.assertEqual(user.email, 'admin@patient.com')


class AdminTests(TestCase):
  def setUp(self):
    self.client = Client()
    self.admin_user = get_user_model().objects.create_superuser(
      email='admin@patient.com', password='123123'
    )

    self.user = get_user_model().objects.create_user(
      email='hellobondeveloper@gmail.com',
      password='test123123',
      name='Test user fullname'
    )

    self.client.force_login(self.admin_user)

  def test_users_listed(self):
    url = reverse('admin:accounts_user_changelist')
    res = self.client.get(url)

    self.assertContains(res, self.user.name)
    self.assertContains(res, self.user.email)
    self.assertContains(res, self.admin_user.email)
