from django.conf.urls.defaults import patterns, include, url
from bookmarks.views import *
import os
from django.conf.urls.defaults import *
from bookmarks.views import *

site_media = os.path.join(
    os.path.dirname(__file__),
    'site_media'
)
urlpatterns = patterns('',
    url(r'^$', main_page),
    (r'^user/(\w+)/$', user_page),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': site_media}),
)
