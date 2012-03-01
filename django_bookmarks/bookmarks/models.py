from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    url = models.URLField(unique=True)

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)

class DateEvent(models.Model):
    date = models.DateTimeField()
    event = models.TextField(max_length=1000)
    user = models.ForeignKey(User)