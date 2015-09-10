from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from core.models import UserProfile

from rest_framework import status


# Create your tests here.
class ViewTest(TestCase):
	fixtures = ['test_users']

	def setUp(self):
		self.client = Client()
		
	def test_valid_user_register(self):
		response = self.client.post('/register/', {'username': 'john.smith1', 'password': '123456', 
			'title' : 'developer', 'office_phone' : '1234567890', 'email' : 'john.smith1@cfpb.gov', 
			'first_name' : 'John', 'last_name' : 'Smith'})
		self.assertEqual(response.status_code, status.HTTP_302_FOUND)
		user = User.objects.get(username='john.smith1')
		self.assertEqual(user.email, 'john.smith1@cfpb.gov')
		user_profile = UserProfile.objects.get(user = user)
		self.assertEqual(user_profile.title, 'developer')

	def test_password_missing_user_register(self):
		response = self.client.post('/register/', {'username': 'john.smith', 
			'title' : 'developer', 'office_phone' : '1234567890', 'email' : 'john.smith@cfpb.gov', 
			'first_name' : 'John', 'last_name' : 'Smith'})
		self.assertContains(response, 'This field is required.')

	def test_invalid_email_user_register(self):
		response = self.client.post('/register/', {'username': 'john.smith', 'password': '123456', 
			'title' : 'developer', 'office_phone' : '1234567890', 'email' : 'john.smith@test.gov', 
			'first_name' : 'John', 'last_name' : 'Smith'})
		self.assertContains(response, 'Please enter an authorized email address.')

	def test_user_login_successful(self):
		response = self.client.post('/login/', {'username': 'john.smith', 'password': '123456'})
		self.assertEqual(response.status_code, status.HTTP_302_FOUND)

	def test_user_login_failure(self):
		response = self.client.post('/login/', {'username': 'john.smith1', 'password': '123456'})	
		self.assertEqual(response.content, 'Invalid login details supplied.')