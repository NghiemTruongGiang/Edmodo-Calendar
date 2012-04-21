from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Entry(models.Model):
	title = models.CharField(max_length = 40)# The name of event
	snippet = models.CharField(max_length = 150, blank = True)
	body = models.TextField(max_length = 10000, blank = True)# content's event
	created = models.DateTimeField(auto_now_add = True)# Time that event was created(auto)
	date_start=models.DateTimeField(blank=True)#start of event
	date_end=models.DateTimeField(blank=True)#the end of event
	creator = models.ForeignKey(User, blank = True, null = True)# user create
	remind = models.BooleanField(default = False)# remind for user
	is_days=models.BooleanField(default=False)
	
	def __unicode__(self):
		if self.title:
			return unicode(self.creator) + u" - " + self.title
		else:
			return unicode(self.creator) + u" - " + self.snippet[:40]
			
	def short(self):
		if self.snippet:
			return "<i>%s</i> - %s" % (self.title, self.snippet)
		else:
			return self.title
			
	short.allow_tags = True 
	
	class Meta:
		verbose_name_plural = "entries"

class GroupCalendar(models.Model):		#Group of calendar
	name=models.CharField(max_length=40)	#the name of group
	creator_group=models.ForeignKey(User, blank=True, null=True)#creator of group
	describe=models.TextField(max_length=10000, blank=True)#the description of group
	group_email=models.EmailField()
	created=models.DateTimeField(auto_now_add=True)
	is_public=models.BooleanField(default=True)
	datecreated=models.DateTimeField(auto_now_add=True)
	
	def short(self):
		if self.name:
			return "<i>%s</i> - %s" % (self.name, self.creator_group)
		else:
			return self.creator_group
	def __unicode__(self):
		return unicode(self.creator_group) + u" - " + self.name
		
	short.allow_tags = True 
	verbose_name_plural = "Group Calendars"
	
class GroupMem(models.Model):
	group_name=models.ForeignKey(GroupCalendar, blank=True, null=True, related_name="group_set")#group
	user_mem=models.ForeignKey(User, blank=True, null=True, related_name="mem_set")#user join
	created=models.DateTimeField(auto_now_add=True)#attended time of this user
	can_modify=models.BooleanField(default=False)#can modify the exested event
	can_create=models.BooleanField(default=False)#can create new event
	is_accept=models.BooleanField(default=False)#become to a member
	
	def __unicode__(self):
		if self.group_name:
			return unicode(self.group_name)
		else:
			return unicode(self.user_mem)
			
	def short(self):
		return "<i>%s</i>" % (self.user_mem)
					
	short.allow_tags = True 
	class Meta:
		verbose_name_plural = "Group Members"
		
class GroupEntry(models.Model):
	title=models.CharField(max_length=40)#title of this event
	snippet=models.CharField(max_length=150, blank=True)#brief
	body=models.TextField(max_length=10000, blank=True)#content
	created=models.DateTimeField(auto_now_add=True)# created time
	date_start=models.DateTimeField(blank=True)#start of event
	date_end=models.DateTimeField(blank=True)#the end of event
	creator=models.ForeignKey(User, blank = True, null = True)#who created
	group_name=models.ForeignKey(GroupCalendar, blank=True, null=True)#where store this event
	remind=models.BooleanField(default=False)#warning user
	is_days=models.BooleanField(default=False)
	
	def __unicode__(self):
		if self.title:
			return unicode(self.group_name) + u" - " + self.title
		else:
			return unicode(self.group_name) + u" - " + self.snippet[:40]
			
	def short(self):
		if self.snippet:
			return "<i>%s</i> - %s" % (self.title, self.snippet)
		else:
			return self.title
			
	short.allow_tags = True 
	
	class Meta:
		verbose_name_plural = "Group Entries"  

class FriendShip(models.Model):
	from_friend=models.ForeignKey(
		User, 
		blank=True, 
		null=True,
		related_name = 'friend_set'
	)#friend request
	to_friend=models.ForeignKey(
		User, 
		blank=True, 
		null=True,
		related_name = 'to_friend_set'
	)#friend accept
	created=models.DateTimeField(auto_now_add=True)#thoi diem tro thanh ban be
	can_create=models.BooleanField(default=False)#to_friend can create new event for ...
	can_modify=models.BooleanField(default=False)#to_friend can modify existed event for ...
	import_friend=models.BooleanField(default=False)#get calendar event from to_friend
	accept_import=models.BooleanField(default=False)#accept for export
	is_accept=models.BooleanField(default=False)#accept to become friend
	
	def __unicode__(self):
		return u'%s, %s' % (
			self.from_friend.username,
			self.to_friend.username
		)
			
	def short(self):
		return "<i>%s</i> - %s" % (self.from_friend, self.to_friend)
					
	short.allow_tags = True 
	
	class Meta:
		unique_together = (('to_friend', 'from_friend'), )
	
	class Meta:
		verbose_name_plural = "Friendship"

class Image(models.Model):
	user=models.ForeignKey(User)
	title=models.CharField('Title', max_length = 40)
	photo=models.ImageField(upload_to = 'file/photo')
	created=models.DateTimeField(auto_now_add=True)# created time
	is_use=models.BooleanField(default=True)
	def __unicode__(self):
		return self.title
		
class UserProfile(models.Model):
	username=models.ForeignKey(User, blank=True, null=True)
	is_public=models.BooleanField(default=True)
	birthday=models.DateField(blank=True)
	first_name=models.CharField(max_length=30)
	last_name=models.CharField(max_length=30)
	image_profile=models.ManyToManyField(Image, blank=True, null=True)
	
	def __unicode__(self):
		return unicode(self.username)
			
	def short(self):
		return "<i>%s</i>" % (self.username)
					
	short.allow_tags = True 
	
	class Meta:
		verbose_name_plural = "User Profile"

class NotificationModel(models.Model):
	user=models.ForeignKey(User, blank=True, null=True)
	content=models.CharField('Content', max_length=100)
	link=models.CharField('Link', max_length=200)
	remind=models.BooleanField(default=True)