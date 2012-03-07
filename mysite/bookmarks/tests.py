from django.test import TestCase
from django.test.client import Client



class ViewTest(TestCase):
	fixtures = ['test_data.json']
	def setUp(self):
		self.client = Client()
	
	def test_register_page(self):
		data = {
			'username': 'test_user',
			'email': 'test_user@example.com',
			'password1': 'pass12345',
			'password2': 'pass12345',
		}
		
		response = self.client.post('/register/', data)
		self.assertRedirects(response, '/register/success/')

	
	def test_bookmark_save(self):
		response = self.client.login(
			username = 'admin',
			password = '12345'
		)

		self.assertTrue(response, msg = 'Failed to login.')
		
		data = {
			'url': 'fujifilm.com',
			'title': 'Fujifilm',
			'tags': 'Camera',
		}
		
		response = self.client.post('/save/', data)
		self.assertRedirects(response, '/user/admin/')
		
		response = self.client.get('/user/admin/')
		self.assertContains(response, 'fujifilm.com')
		
		#self.assertContains(response, 'test-url')
		#self.assertContains(response, 'test-tag')