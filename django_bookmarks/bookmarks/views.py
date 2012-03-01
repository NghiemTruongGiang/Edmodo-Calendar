# Create your views here.
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext

def main_page(request):
    return render_to_response('main_page.html', RequestContext(request))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404('User request not found')

    bookmarks = user.bookmark_set.all()

    variables = RequestContext(request, {
        'username': username,
        'bookmarks': bookmarks
    })

    return render_to_response('user_page.html', variables)