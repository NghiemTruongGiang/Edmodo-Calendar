from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from Calendar.views import *
from django.views.generic.simple import direct_to_template
import os

media = os.path.join(
    os.path.dirname(__file__), 'media'
)

site_media = os.path.join(
	os.path.dirname(__file__), 'site_media'
)
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#Calendar_Learn.Calendar.views
urlpatterns = patterns('',
    (r"^month/(\d+)/(\d+)/(prev|next)/$", month),
    (r"^month/(\d+)/(\d+)/$", month),
    (r"^month/$", month),
    (r"^day/(\d+)/(\d+)/(\d+)/$", day),
    (r"^settings/$", settings),
	(r"^main/$", main),
	(r'^add_photo/$', add_photo),
	(r'^friend/add/$', friend_add),
	(r'^user/(\w+)/friend/$', user_friend),
	(r'^user/(\w+)/group/$', user_group),
	(r'^user/(\w+)/photo/$', image_profile),
    (r'^user/(\w+)/$', user_page),
    (r"^(\d+)/$", main),
    (r"^$", main),
    (r'^register/$', register_page),
	(r'^admin/', include(admin.site.urls)),
    (r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),
	#Group management
	(r'^group/join/$', join_group),
	(r'^group/(\w+)/(\d+)/(\d+)/(\d+)/$', g_event_edit),
	(r'^create_group/$', create_group),
	(r'^group/(\w+)/$', group_view),
	(r"^(\w+)/month/(\d+)/(\d+)/(prev|next)/$", group_month),
    (r"^(\w+)/month/(\d+)/(\d+)/$", group_month),
    (r"^(\w+)/month/$", group_month),
	(r"^(\w+)/day/(\d+)/(\d+)/(\d+)/$", group_day),
	#Session management
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', logout_page),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
		{'document_root': site_media}),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': ''}),
)
