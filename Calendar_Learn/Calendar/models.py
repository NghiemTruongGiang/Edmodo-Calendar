from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Entry(models.Model):
	title = models.CharField(max_length = 40)# The name of event
	snippet = models.CharField(max_length = 150, blank = True)
	body = models.TextField(max_length = 10000, blank = True)# content's event
	created = models.DateTimeField(auto_now_add = True)# Time that event was created(auto)
	date = models.DateField(blank = True)
	creator = models.ForeignKey(User, blank = True, null = True)# user create
	remind = models.BooleanField(default = False)# remind for user
	
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
		
		
###Admin
class EntryAdmin(admin.ModelAdmin):
    list_display = ["creator", "date", "title", "snippet"]
    search_fields = ["title", "snippet"]
    list_filter = ["creator"]
	
admin.site.register(Entry, EntryAdmin)