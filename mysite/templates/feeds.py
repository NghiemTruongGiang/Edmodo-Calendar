from django.contrib.syndication.feeds import Feed
from bookmarks.models import Bookmark

class RecentBookmarks(Feed):
	title = u'Django Bookmarks | Recent Bookmarks'
	link = '/feeds/recent/'
	description = u'Recent bookmarks posted to Django Bookmarks'
	
	def items(self):
		return Bookmark.objects.order_by('-id')[:10]