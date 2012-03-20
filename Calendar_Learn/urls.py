from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from Calendar.views import *
from django.views.generic.simple import direct_to_template
import os

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
    (r'^user/(\w+)/$', user_page),
    (r"^(\d+)/$", main),
    (r"^$", main),
    (r'^register/$', register_page),
	(r'^admin/', include(admin.site.urls)),
    (r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),
	#Group management
	(r'^create_group/$', create_group),
	#Session management
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', logout_page),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
		{'document_root': site_media}),
)
