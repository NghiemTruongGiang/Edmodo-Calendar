from django.test import TestCase
from django.contrib.auth.models import User

class CalendarTest(TestCase):
    def test_register_page(self):
        data={
            'username':'admin',
            'email':'email@gmail.com',
            'password1':'123456',
            'password2':'123456',
        }
        response = self.client.post('/register/',data)
        self.assertContains(response,"Register")
    def test_login(self):
        response = self.client.post('/accounts/login/',{
            'usename' : 'admin',
            'password' : 'admin',
        })
        self.assertEqual(response.status_code, 200)
	def test_create_group(self):
        response = self.client.post('/accounts/login/',{
            'usename' : 'admin',
            'password' : 'admin',
            })
        self.assertEqual(response.status_code, 200)
        self.client.post('/create/group/',{
			'name' : 'Group name',
			'describe' : 'Group description',
			'group_email' : 'Group email address',
			})
		self.assertEqual(response.status_code, 200)
	def test_change_name_form(self):
		response = self.client.post('/accounts/login/',{
            'usename' : 'admin',
            'password' : 'admin',
            })
		self.assertEqual(response.status_code, 200)
		self.client.post('/change/form/',{
            'first_name' : 'First Name',
			'last_name' : 'Last Name',
			'email' : 'Email',
			'birthday' : 'Birthday',
            })
		self.assertEqual(response.status_code, 200)
	def test_password_change_form(self):
		response = self.client.post('/accounts/login/',{
            'usename' : 'admin',
            'password' : 'admin',
            })
		self.assertEqual(response.status_code, 200)
		self.client.post('/change/password/',{
			'old_password' : 'Old Password',
			'new_password1' : 'New Password',
			'new_password2' : 'Confirm New Password',
			})
		self.assertEqual(response.status_code, 200)
		