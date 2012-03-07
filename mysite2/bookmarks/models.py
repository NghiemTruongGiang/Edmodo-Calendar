from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

# Create your models here.
class Link(models.Model):
	url = models.URLField(unique = True)
	def __str__(self):
		return self.url

class Bookmark(models.Model):
	title = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	link = models.ForeignKey(Link)
	def __str__(self):
		return '%s, %s' %(self.user.username, self.link.url)
	def get_absolute_url(self):
		return self.link.url
	
class Tag(models.Model):
	name = models.CharField(max_length = 64, unique = True)
	bookmarks = models.ManyToManyField(Bookmark)
	def __str__(self):
		return self.name
		
class SharedBookmark(models.Model):
	bookmark = models.ForeignKey(Bookmark, unique = True)
	date = models.DateTimeField(auto_now_add = True)
	votes = models.IntegerField(default = 1)
	users_voted = models.ManyToManyField(User)
	
	def __unicode__(self):
		return u'%s, %s' % (self.bookmark, self.votes)
		
class Friendship(models.Model):
	from_friend = models.ForeignKey(
		User, related_name = 'friend_set'
	)
	to_friend = models.ForeignKey(
		User, related_name = 'to_friend_set'
	)
	def __unicode__(self):
		return u'%s, %s' % (
			self.from_friend.username,
			self.to_friend.username
		)
		
	class Meta:
		unique_together = (('to_friend', 'from_friend'), )
	
	class Meta: 
		permissions = (
				('can_list_friend_bookmarks',
				'can list friend bookmarks'),
		)

class Invitation(models.Model):
	name = models.CharField(max_length = 50)
	email = models.EmailField()
	code = models.CharField(max_length = 20)
	sender = models.ForeignKey(User)
	
	def __unicode__(self):
		return u'%s %s' % (self.sender.username, self.email)
		
	def send(self):
		subject = u'Invitation to join Django Bookmarks.'
		link = 'http://%s/friend/accept/%s/' % (settings.SITE_HOST, self.code)
		template = get_template('invitation_email.txt')
		context = Context({
			'name': self.name,
			'link': link,
			'sender': self.sender.username,
		})
		message = template.render(context)
		send_mail(
			subject, message, settings.DEFAULT_FROM_EMAIL, [self.email]
		)