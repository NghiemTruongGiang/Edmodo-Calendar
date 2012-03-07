import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django import forms


class RegistrationForm(forms.Form):
	username = forms.CharField(label = 'Username', max_length = 30)
	firstname = forms.CharField(label = 'First name', max_length = 30)
	lastname = forms.CharField(label = 'Last name', max_length = 30)
	email = forms.EmailField(label = 'Email')
	password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput())
	password2 = forms.CharField(label = 'Password (Again)', widget = forms.PasswordInput())
	
	def clean_password2(self):
		if 'password1'in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			
			if password1 == password2:
				return password2
		
		return forms.ValidationError('Password do not match!')
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and underscore.')
		try:
			User.objects.get(username = username)
		except ObjectDoesNotExist:
			return username
		
		raise forms.ValidationError('Username is already taken')
		
	def clean_first_name(self):
		firstname = self.cleaned_data['firstname']
		if not re.search(r'^\w+$', first_name):
			raise forms.ValidationError('First name can only contain alphanumeric characters and underscore.')
	
	def clean_last_name(self):
		lastname = self.cleaned_data['lastname']
		if not re.search(r'^\w+$', last_name):
			raise forms.ValidationError('Last name can only contain alphanumeric characters and underscore.')
	
	
	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			User.objects.get(email = email)
		except ObjectDoesNotExist:
			return email
			
		raise forms.ValidationError('Email is already taken')

class BookmarkSaveForm(forms.Form):
	url = forms.URLField(
		label = 'URL',
		widget = forms.TextInput(attrs = {'size' : 64})
	)
	title = forms.CharField(
		label = 'Title',
		widget = forms.TextInput(attrs = {'size' : 64})
	)
	tags = forms.CharField(
		label = 'Tags',
		required = False,
		widget = forms.TextInput(attrs = {'size' : 64})
	)
	share = forms.BooleanField(
		label = u'Share on the main page',
		required = False
	)
	
class SearchForm(forms.Form):
  query = forms.CharField(
    label=u'Enter a keyword to search for',
    widget=forms.TextInput(attrs={'size': 32})
  )

class FriendInviteForm(forms.Form):
	name = forms.CharField(label = _("Friend's Name"))
	email = forms.EmailField(label = _("Friend's Email"))