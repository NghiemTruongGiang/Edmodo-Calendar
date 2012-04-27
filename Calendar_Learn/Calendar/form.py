import re
from django import forms
from Calendar.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length = 30)
    first_name = forms.CharField(label = 'First Name', max_length = 30)
    last_name = forms.CharField(label = 'Last Name', max_length = 30)
    email = forms.EmailField(label = 'Email')
    password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput())
    password2 = forms.CharField(label = 'Password (Again)', widget = forms.PasswordInput())

    def clean_password2(self):
        if 'password1'in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']

            if password1 == password2:
                return password2

        raise forms.ValidationError('Password do not match!')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError(
                'Username can only contain alphanumeric characters and underscore.'
            )
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username

        raise forms.ValidationError('Username is already taken')

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.search(r'^\w+$', first_name):
            raise forms.ValidationError(
                'First Name can only contain alphanumeric characters and underscore.'
            )

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.search(r'^\w+$', last_name):
            raise forms.ValidationError(
                'Last name can only contain alphanumeric characters and underscore.'
            )
#    def clean_email(self):
#        email = self.cleaned_data['email']
#        try:
#            User.objects.get(email = email)
#        except ObjectDoesNotExist:
#            return email
#
#        raise forms.ValidationError('Email is already taken')

class CreateGroupForm(forms.Form):
	name=forms.CharField(label='Group name', max_length=40)
	describe=forms.CharField(
		label='Group description', 
		max_length=10000,
		widget=forms.Textarea()
	)
	group_email=forms.EmailField(label='Group email address')
	is_public=forms.BooleanField(label='Public', required=False)
	
	def clean_group_email(self):
		group_email=self.cleaned_data['group_email']
		try:
			GroupCalendar.objects.get(group_email=group_email)
		except ObjectDoesNotExist:
			return group_email
			
		raise forms.ValidationError('This email group is already taken')
	
	def clean_name(self):
		name=self.cleaned_data['name']
		try:
			GroupCalendar.objects.get(name=name)
		except ObjectDoesNotExist:
			return name
		
		raise forms.ValidationError('This name group is already taken')

class AddPhotoForm(forms.Form):
	title=forms.CharField(label="Title", max_length=40)
	is_use=forms.BooleanField(required=False)
	photo=forms.ImageField(label="Add photo")