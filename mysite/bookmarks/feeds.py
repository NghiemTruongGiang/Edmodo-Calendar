from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from bookmarks.models import Bookmark

class RecentBookmarks(Feed):
	title = u'Django Bookmarks | Recent Bookmarks'
	link = '/feeds/recent/'
	description = u'Recent bookmarks posted to Django Bookmarks'
	
	def items(self):
		return Bookmark.objects.order_by('-id')[:10]

class UserBookmark(Feed):
	def get_object(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
		return User.objects.get(username = bits[0])
	
	def title(self, user):
		return(
			u'Django Bookmarks | Bookmarks for %s' %user.username
		)
	
	def link(self, user):
		return '/feeds/user/%s' %user.username
	
	def description(self, user):
		return u'Recent bookmarks posted by %s' % user.username
	
	def items(self, user):
		return user.bookmark_set.order_by('-id')[:10]
		