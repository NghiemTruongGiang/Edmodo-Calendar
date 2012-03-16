import time
import calendar
#import datetime
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
#from django.http import HttpResponseRedirect, HttpResponse
#from django.shortcuts import get_object_or_404, render_to_response

from django.http import Http404
#from django.contrib.auth.models import User
from django.shortcuts import render_to_response
#from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from Calendar.form import *
#from django.views.decorators.csrf import csrf_exempt
#from Calendar.models import *


from Calendar_Learn.Calendar.models import *

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()

def _show_users(request):
    """Return show_users setting; if it does not exist, initialize it."""
    s = request.session
    if not "show_users" in s:
        s["show_users"] = True
    return s["show_users"]

@login_required(login_url = '/login/')
def main(request, year=None):
    """Main listing, years and months; three years per page."""
    # prev / next years
    if year: 
		year = int(year)
    else:    
		year = time.localtime()[0]

    nowy, nowm = time.localtime()[:2]
    lst = []

    # create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1, year+2]:
        mlst = []
        for n, month in enumerate(mnames):
			# are there entry(s) for this month; current month?
            entry = current = False   
            entries = Entry.objects.filter(
				date__year=y, 
				date__month=n+1
			)
            if not _show_users(request):
                entries = entries.filter(creator=request.user)

            if entries:
                entry = True
            if y == nowy and n+1 == nowm:
                current = True
            mlst.append(dict(
				n=n+1, 
				name=month, 
				entry=entry, 
				current=current
			))
        lst.append((y, mlst))

    return render_to_response("main.html", dict(
		years=lst, 
		user=request.user, 
		year=year,
        reminders=reminders(request)
	))

def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404('User request not found')

    variables = RequestContext(request, {
        'username': username,
    })

    return render_to_response('user_page.html', variables)

@login_required(login_url='/login/')
def month(request, year, month, change=None):
    """Listing of days in `month`."""
    year, month = int(year), int(month)

    # apply next / previous change
    if change in ("next", "prev"):
        now, mdelta = date(year, month, 15), timedelta(days=31)
        if change == "next":   
			mod = mdelta
        elif change == "prev": 
			mod = -mdelta

        year, month = (now+mod).timetuple()[:2]

    # init variables
    cal = calendar.Calendar()
    month_day = cal.itermonthdates(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0
    # make month lists containing list of days for each week
    # each day tuple will contain list of entries and 'current' indicator
    for day in month_day:
        entries = current = False   # are there entries for this day; current day?
        if day.day:
            entries = Entry.objects.filter(
				date__year=day.year, 
				date__month=day.month, 
				date__day=day.day
			)
            if not _show_users(request):
                entries = entries.filter(creator=request.user)
            if day.day == nday and day.year == nyear and day.month == nmonth:
                current = True
        lst[week].append((day.day, day.month, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1
			
    return render_to_response("month.html", dict(
		year=year, 
		month=month, 
		user=request.user,
        month_days=lst[:week], 
		mname=mnames[month-1], 
		reminders=reminders(request)
	))
	
@login_required(login_url = '/login/')
def day(request, year, month, day):
	"""Entries for day"""
	EntriesFormset = modelformset_factory(
		Entry,
		extra = 1,
		exclude = ('creator', 'date'),
		can_delete = True
	)
	
	if request.method == 'POST':
		formset = EntriesFormset(request.POST)
		if formset.is_valid:
			#add current user and date to each entry and save
			entries = formset.save(commit = False)
			for entry in entries:
				entry.creator = request.user
				entry.date = date(int(year), int(month), int(day))
				entry.save()
			return HttpResponseRedirect(reverse(
				'Calendar_Learn.Calendar.views.month',
				args = (year, month)
			))
	else:
		#display formset for existing entries and one extra form
		formset = EntriesFormset(
			queryset = Entry.objects.filter(
				date__year = year,
				date__month = month,
				date__day = day,
				creator = request.user
			)
		)
	other_entries = []
	if _show_users(request) :
		other_entries = Entry.objects.filter(
			date__year = year,
			date__month = month,
			date__day = day,
		).exclude(creator = request.user)
	return render_to_response('day.html', add_csrf(
		request,
		entries = formset, 
		year = year,
		month = month,
		day = day
	))

def add_csrf(request, **kwargs):
	"""Add csrf adn use to dictionary."""
	d = dict(user = request.user, **kwargs)
	d.update(csrf(request))
	return d

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password2'],
                email=form.cleaned_data['email']
            )
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'registration/register.html',
        variables
    )

def reminders(request):
	"""Return the list of reminders for today and tomorrow."""
	year, month, day = time.localtime()[:3]
	reminders = Entry.objects.filter(
		date__year = year,
		date__month = month,
		date__day = day,
		creator = request.user,
		remind = True
	)
	tomorrow = datetime.now() + timedelta(days = 1)
	year, month, day = tomorrow.timetuple()[:3]
	
	return list(reminders) + list(Entry.objects.filter(
		date__year = year,
		date__month = month,
		date__day = day,
		creator = request.user,
		remind = True
	))
	
@login_required(login_url= '/login/')
def settings(request):
	"""Setting screen"""
	s = request.session
	_show_users(request)
	if request.method == 'POST':
		s['show_users'] = (True if 'show_users' in request.POST else False)
		
	return render_to_response(
		'settings.html', 
		add_csrf(request, show_users = s['show_users']) 
	)