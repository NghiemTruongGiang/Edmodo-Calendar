from django.contrib import admin
from Calendar.models import *

#Group calendar
class GroupCalendarAdmin(admin.ModelAdmin):
	list_display=["name", "creator_group", "group_email", "datecreated", "is_public"]
	ordering=["name"]
	search_fields=["name"]
	list_filter=["name"]
admin.site.register(GroupCalendar, GroupCalendarAdmin)

#Group Entry calendar
class GroupEntryAdmin(admin.ModelAdmin):
	list_display=["group_name", "creator", "date_start", "date_end", "title", "snippet"]
	ordering=["group_name"]
	search_fields=["title", "snippet"]
	list_filter=["creator","group_name"]
	
admin.site.register(GroupEntry, GroupEntryAdmin)

#Group Memeber
class GroupMemAdmin(admin.ModelAdmin):
	list_display=["group_name", "user_mem", "created", "can_modify", "can_create", "is_accept"]
	ordering=["group_name"]
	search_field=["group_name", "user_mem"]
	list_filter=["group_name"]
	
admin.site.register(GroupMem, GroupMemAdmin)

#FriendShip
class FriendShipAdmin(admin.ModelAdmin):
	list_display=["from_friend", "to_friend", "created", "is_accept"]
	ordering=["from_friend"]
	search_field=["from_friend", "to_friend"]
	list_filter=["from_friend", "to_friend"]

admin.site.register(FriendShip, FriendShipAdmin)

#Image Admin
class ImageAdmin(admin.ModelAdmin):
	list_display=["user", "title", "created", "is_use", "photo"]
	ordering=["user"]
	search_field=["user", "title"]

admin.site.register(Image, ImageAdmin)

#User Profile
class UserProfileAdmin(admin.ModelAdmin):
	list_display=["username", "birthday", "first_name", "last_name", "is_public"]
	ordering=["username"]
	search_field=["username"]
	
admin.site.register(UserProfile, UserProfileAdmin)

###Admin
class EntryAdmin(admin.ModelAdmin):
    list_display = ["creator", "date_start", "date_end", "title", "snippet"]
    search_fields = ["title", "snippet"]
    list_filter = ["creator"]
	
admin.site.register(Entry, EntryAdmin)