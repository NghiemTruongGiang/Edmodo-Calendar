import time
import calendar
#import datetime
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
#from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

from django.http import Http404, HttpResponseRedirect
#from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.template import RequestContext
from Calendar.form import *
#from django.views.decorators.csrf import csrf_exempt


from Calendar_Learn.Calendar.models import *

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()

def test(request):
	return render_to_response('test.html')
def test_main(request):
	return render_to_response('test_main.html')

def test_calendar(request):
	return render_to_response('test_calendar.html')

def test_profile(request):
	return render_to_response('test_profile.html')

def _show_users(request):
	"""Return show_users setting; if it does not exist, initialize it."""
	s = request.session
	if not "show_users" in s:
		s["show_users"] = True
	return s["show_users"]

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

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
	groups = GroupCalendar.objects.filter(creator_group=request.user)
	try:
		image=Image.objects.get(user=request.user, is_use=True)
	except:
		image=None
	# create a list of months for each year, indicating ones that contain entries and current
	for y in [year, year+1, year+2]:
		mlst = []
		for n, month in enumerate(mnames):
			# are there entry(s) for this month; current month?
			entry = current = False
			entries = Entry.objects.filter(
				date_start__year=y, 
				date_start__month=n+1
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
	listYear = range(year - 5,year + 5)
	return render_to_response("main.html", dict(
		years=lst,
		image = image,
		groups = groups,
		user=request.user, 
		year=year,
		listYear = listYear,
		reminders=reminders(request)
	))

@login_required(login_url='/login/')
def user_page(request, username):
	user = get_object_or_404(User, username=username)
	#username1=username
	try:
		info=UserProfile.objects.get(username=user)
	except:
		info=None

	try:
		image=Image.objects.get(user=user, is_use=True)
	except:
		image=None

	#image=get_object_or_404(Image, user=request.user, is_use=True)
	if request.user.is_authenticated():
		is_friend = FriendShip.objects.filter(
			from_friend = request.user,
			to_friend = user,
		)
	else:
		is_friend = False

	variables = RequestContext(request, {
		'user2': user,
		'username': user.username,
		'is_friend': is_friend,
		'info': info,
		'image': image,
	})

	return render_to_response('user/user_page.html', variables)

@login_required(login_url='/login/')
def image_profile(request, username):
	user = get_object_or_404(User, username=username)
	try:
		info=UserProfile.objects.get(username=user)
	except:
		info=None
	try:
		imageprofile=Image.objects.filter(user=user)
	except:
		imageprofile=None

	try:
		image=Image.objects.get(user=user, is_use=True)
	except:
		image=None

	if request.user.is_authenticated():
		is_friend = FriendShip.objects.filter(
				from_friend = request.user,
				to_friend = user,
		)
	else:
		is_friend = False

	variables = RequestContext(request, {
		'user2': user,
		'username': username,
		'is_friend': is_friend,
		'imageprofile': imageprofile,
		'image': image,
	})

	return render_to_response('user/image_profile.html', variables)

@login_required(login_url='/login/')
def user_group(request, username):
	user=get_object_or_404(User, username=username)
	try:
		has_group=GroupCalendar.objects.filter(creator_group=user)
	except:
		has_group=None
	try:
		accept_join=GroupMem.objects.filter(user_mem=user).filter(is_accept=True)
	except:
		accept_join=None

	try:
		not_accept_join=GroupMem.objects.filter(user_mem=user).filter(is_accept=False)
	except:
		not_accept_join=None

	try:
		image=Image.objects.get(user=user, is_use=True)
	except:
		image=None

	if request.user.is_authenticated():
		is_friend = FriendShip.objects.filter(
				from_friend = request.user,
				to_friend = user,
		)
	else:
		is_friend = False

	variables=RequestContext(request, {
	'username': username,
	'is_friend': is_friend,
	'has_group': has_group,
	'user2': user,
	'image': image,
	'accept_join': accept_join,
	'not_accept_join': not_accept_join,
	})

	return render_to_response('user/user_group.html', variables)

@login_required(login_url='/login/')
def user_friend(request, username):	
	user=get_object_or_404(User, username=username)
	friends = [friendship.to_friend for friendship in user.friend_set.all()]
	try:
		image=Image.objects.get(user=user, is_use=True)
	except:
		image=None

	if request.user.is_authenticated():
		is_friend = FriendShip.objects.filter(
			from_friend = request.user,
			to_friend = user,
		)
	else:
		is_friend = False

	friend_pic_profile = Image.objects.filter(
		user__in = friends,
		is_use=True,
	).order_by('-id')

	variables=RequestContext(request, {
		'username': username,
		'is_friend': is_friend,
		'user2': user,
		'image': image,
		'friend': friend_pic_profile,
	})

	return render_to_response('user/user_friend.html', variables)

@login_required(login_url = '/login/')
def friend_add(request):
	if 'username' in request.GET:
		friend = get_object_or_404(
			User, username = request.GET['username']
		)
		try:
			checkfriend=FriendShip.objects.get(
				from_friend = request.user,
				to_friend = friend,
			)
		except:
			checkfriend=False

		if checkfriend:
			return HttpResponseRedirect(
			'/user/%s/friend' % request.user.username
			)
		friendship = FriendShip(	
			from_friend = request.user,
			to_friend = friend,
			is_accept=True,
		)
		friendship1 = FriendShip(	
			from_friend = friend,
			to_friend = request.user,
		)
		try:
			friendship.save()
			friendship1.save()
			request.user.message_set.create(
				message = u'%s was added to your friend list.' % friend.username
			)
		except:
			request.user.message_set.create(
				message = u'%s is already a friend of yours' % friend.username
			)
		return HttpResponseRedirect(
			'/user/%s/friend' % request.user.username
		)
	else:
		raise Http404

@login_required(login_url='/login/')		
def add_photo(request):
	if request.method == 'POST':
		form=AddPhotoForm(request.POST, request.FILES)
		if form.is_valid():
			s_is_use=form.cleaned_data['is_use']
			if s_is_use:
				try:
					photopro=Image.objects.get(user=request.user, is_use=True)
					photopro.is_use=False
					photopro.save()
				except:
					pass
			image=Image.objects.create(
				user=request.user,
				title=form.cleaned_data['title'],
				is_use=s_is_use,
				photo=form.cleaned_data['photo'],
			)
			image.save()

		return HttpResponseRedirect('/user/%s/photo' % request.user.username)
	else:
		form = AddPhotoForm()

	variables = RequestContext(request,{
		'form':form,
	})
	return render_to_response('add_photo.html',variables)


def caltime(timedel):
	s_time = str(timedel)
	s_time = s_time.split(' ')
	sum = 0
	if s_time[0][0] == '0':
		sum = 0
	else:
		sum = int(s_time[0])
	if s_time[0][0] == '-':
		sum -= 1
	else:
		sum += 1
	return sum

@login_required(login_url='/login/')
def month(request, year, month, change=None):
	#Get user
	user=get_object_or_404(User, username=request.user.username)
	#Get calendar of friend
	try:
                image=Image.objects.get(user=request.user, is_use=True)
        except:
                image=None
	try:
		listFriendCal=FriendShip.objects.filter(
			from_friend=user,
			import_friend=True,
			accept_import=True,
		)
	except:
		listFriendCal=None
	#Get calendar of group
	try:
		groups=GroupMem.objects.filter(user_mem=user)
	except:
		listGroupCal=None

	#Listing of days in `month`.
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
	#tinh tong so ngay trong month dates
	month_lst=list(month_day)
	total_s=month_lst[-1]-month_lst[0]
	total = caltime(total_s)
	month_day = cal.itermonthdates(year, month)
	#lay ngay thang nam hien tai
	nyear, nmonth, nday = time.localtime()[:3]

	lst = []#luu tru du lieu ve ngay thang va event
	lst.append([[], []])
	els=[]#luu tru cac event keo dai
	linenum=[]#so event tren mot hang (mot tuan)
	linenum.append([])
	week = 0
	k = 0#dem so hang entry
	usercal1=None
	manyday2 = []
	# make month lists containing list of days for each week
	# each day tuple will contain list of entries and 'current' indicator
	if 'username' in request.GET:
		try:
			usercal=User.objects.get(username = request.GET['username'])
		except:
			usercal=user
	else:
		usercal=user
	if usercal != None:
		#lay cac su kien dien ra trong khoang thoi gian dai
		manydays=Entry.objects.filter(
			creator=usercal,
			is_days=True,
		)
		for oneday in manydays:
			datest=date(oneday.date_start.year, oneday.date_start.month, oneday.date_start.day)
			dateen=date(oneday.date_end.year, oneday.date_end.month, oneday.date_end.day)
			delta_s_ss=datest-month_lst[0]
			delta_s_se=datest-month_lst[-1]
			delta_s_es=dateen-month_lst[0]
			delta_s_ee=dateen-month_lst[-1]
			# su kien bat dau sau nmonth hoac ket thuc truoc nmonth
			if (delta_s_es < timedelta(0)) or (delta_s_se > timedelta(0)):
				continue
			#su kien bat dau truoc nmonth va ket thuc sau nmonth
			elif (delta_s_ss < timedelta(0)) and (delta_s_ee > timedelta(0)):
				els.append([oneday, total, month_lst[0], 2])
				continue
			#su kien bat dau truoc nmonth va ket thuc o giua nmonth
			elif (delta_s_ss < timedelta(0)) and (delta_s_ee <= timedelta(0)) and (delta_s_ee >= -total_s):
				delta_es=caltime(delta_s_es)
				els.append([oneday, delta_es, month_lst[0], delta_es])
				continue
			#su kien bat dau o giua nmonth va ket thuc sau nmonth
			elif (delta_s_ss >= timedelta(0)) and (delta_s_ss <= total_s) and (delta_s_ee > timedelta(0)):
				delta_es=caltime(delta_s_es)
				els.append([oneday, delta_es+1, datest, 4])
				continue
			#su kien bat dau va ket thuc trong nmonth
			else:
				delta=caltime(oneday.date_end-oneday.date_start)
				els.append([oneday, delta, datest, 5])
				continue
		#Nap su kien de in ra du lieu
		for day in month_day:
			entries = current = False   # are there entries for this day; current day?
			if day.day:
				entries = Entry.objects.filter(
					date_start__year=day.year,
					date_start__month=day.month,
					date_start__day=day.day,
					creator=usercal,
					is_days=False
				)
				j = 0#dem so long events da duoc them vao
				#add entry into week row
				for i in range(len(els)):
					if els[i][2] == day and els[i][1] > 0:
						j+=1
						if k == 0 or k <= j:#neu so hang entry it hon so entry
							k+=1
							lst[week][1].append([])#tao hang moi rong
							linenum[week].append(0)#them mot bien quan li so event trong 1 tuan
						check = False
						#duyet qua tat cac cac dong event trong tuan
						for iter in range(k):
							if linenum[week][iter] > len(lst[week][0]):
								continue
							elif (linenum[week][iter]+1) == len(lst[week][0]):
								m = 0
								if (7-linenum[week][iter]) >= els[i][1]:
									m = els[i][1]
								else:
									m = 7-linenum[week][iter]
								lst[week][1][iter].append((els[i][0], m))
								#giam so ngay con lai cua event
								els[i][1] -= m
								#tang them thoi gian dien ra event
								els[i][2] += timedelta(m)
								linenum[week][iter] += (m)
								check=True
								break
							else:
								for i2 in range(len(lst[week][0]) - linenum[week][iter]):
									lst[week][1][iter].append([])
									linenum[week][iter] += 1
								m = 0
								if (7-linenum[week][iter]) >= els[i][1]:
									m = els[i][1]
								else:
									m = 7-linenum[week][iter]
								lst[week][1][iter].append((els[i][0], m))
								#giam so ngay con lai cua event
								els[i][1] -= m
								#tang them thoi gian dien ra event
								els[i][2] += timedelta(m)
								linenum[week][iter] += m
								check=True
								break
						if not check:
							k+= 1
							lst[week][1].append([])
							linenum[week].append(0)
							for i2 in range(len(lst[week][0]) - linenum[week][k-1]):
								lst[week][1][k-1].append([])
								linenum[week][k-1] += 1
							m = 0
							if (7-linenum[week][k-1]) >= els[i][1]:
								m = els[i][1]
							else:
								m = 7-linenum[week][k-1]
							lst[week][1][k-1].append((els[i][0], m))
							#giam so ngay con lai cua event
							els[i][1] -= m
							#tang them thoi gian dien ra event
							els[i][2] += timedelta(m)
							linenum[week][k-1] += m
				for entry in entries:
					j+= 1
					if k <= j or k == 0:#neu so hang entry it hon so entry thi them hang entry
						k+=1
						lst[week][1].append([])#tao hang moi rong
						linenum[week].append([0])
					check=False
					for iter in range(k):
						if linenum[week][iter] > len(lst[week][0]):
							continue
						elif linenum[week][iter] == len(lst[week][0]):
							lst[week][1][iter].append((entry, 0))
							linenum[week][iter] += 1
							check = True
							break
						else:
							for i2 in range(len(lst[week][0]) - linenum[week][iter]):
								lst[week][1][iter].append([])
								linenum[week][iter] += 1
							lst[week][1][iter].append((entry, 0))
							linenum[week][iter] += 1
							check=True
							break
					if not check:
						k+=1
						lst[week][1].append([])
						linenum[week].append(0)
						for i2 in range(len(lst[week][0])-linenum[week][k-1]):
							lst[week][1][k-1].append([])
							linenum[week][k-1]+=1
						lst[week][1][k-1].append((entry, 0))
						linenum[week][k-1] += 1

				if not _show_users(request):
					entries = entries.filter(creator=request.user)
				if day.day == nday and day.year == nyear and day.month == nmonth:
					current = True
				lst[week][0].append((day.day, day.month, current))
			if len(lst[week][0]) == 7:
				for i in range(len(lst[week][1])):
					if linenum[week][i] < 7:
						for j in range(7-linenum[week][i]):
							lst[week][1][i].append([])
				lst.append([[], []])
				linenum.append([])
				week += 1
				k = 0

	return render_to_response("month.html", dict(
		year=year,
		month=month,
		user=request.user,
		month_days=lst[:week],
		mname=mnames[month-1],
		listfriend=listFriendCal,
		els1=els,
		groups=groups,
                image = image,
		reminders=reminders(request)
	))

def calmi(hour, minute):
	mi = hour*60 + minute
	return mi

def week(request, year, month, day, change=None	):
	user = get_object_or_404(User, username = request.user.username)
	nameday = "Mon Tue Wed Thu Fri Sat Sun"
	nameday=nameday.split()

	year, month, day = int(year), int(month), int(day)
	try:
		lfc = FriendShip.objects.filter(
			from_friend=user,
			import_friend=True,
			accept_import=True,
		)
	except:
		lfc = None

	try:
		lgc = GroupMem.objects.filter(user_mem=user)
	except:
		lgc = None

	els = [] #luu tru event keo dai hoac su kien dac biet
	linenum = []#luu tru so hang cua moi dong event dai hoac dac biet
	linenum.append([])
	els.append([])
	weeklist = [] #luu tru event trong tuan do
	weekday = [] #luu tru ngay thang trong tuan
	b_day = date(2012, 12, 4)
	e_day = date(2012, 12, 3)
	GMT_time = range(24)
	weeklist.append([])
	count = 1 #dem so ngay trong tuan
	nday = calendar.weekday(year, month, day)
	now_day = date(year, month, day)
	#lay cac su kien keo dai
	eventlongs = Entry.objects.filter(
		creator = request.user,
		is_days = True
	).order_by('date_start')
	for i in range(7):
		this_day = now_day + timedelta(i - nday)
		weekday.append((this_day, nameday[i]))
		if i == 0:
			b_day = this_day
		if i == 6:
			e_day = this_day
		entries = Entry.objects.filter(
			date_start__year=this_day.year,
			date_start__month=this_day.month,
			date_start__day=this_day.day,
			creator=user,
			is_days=False
		).order_by('date_start')
		for entry in entries:
			top = calmi(entry.date_start.hour, entry.date_start.minute)
			hour_h = entry.date_end.hour - entry.date_start.hour
			minute_h = entry.date_end.minute - entry.date_start.minute
			height = calmi(hour_h, minute_h)
			width = 100
			relav = 0
			weeklist[i].append([entry, top, height, width, relav])
		weeklist.append([])
		count += 1
	i = 0
	for event in eventlongs:
		dates = date(event.date_start.year, event.date_start.month, event.date_start.day)
		datee = date(event.date_end.year, event.date_end.month, event.date_end.day)
		dateeb = datee - b_day# ngay ket thuc su kien tru ngay dau tuan
		datese = dates - e_day# ngay bat dau su kien tru ngay cuoi tuan
		datesb = dates - b_day# ngay bat dau su kien tru ngay dau tuan
		dateee = datee - e_day# ngay ket thuc su kien tru ngay cuoi tuan
		#khong nam trong tuan day
		if dateeb < timedelta(0) or datese > timedelta(0):
			continue
		#su kien keo dai qua ca tuan
		elif datesb < timedelta(0) and dateee > timedelta(0):
			els[i].append([0, event, 7, 0])
			els.append([])
			linenum[i].append(7)
			linenum.append([])
			i += 1
			continue
		#su kien bat dau truoc tuan va ket thuc trong tuan
		elif datesb < timedelta(0) and dateee <= timedelta(0):
			dateeb = datee - b_day
			dateeb_n = caltime(dateeb)
			els[i].append([0, event, dateeb_n, 7 - dateeb_n])
			linenum[i][0] += dateeb
			continue
		#su kien bat dau trong tuan va ket thuc sau tuan
		elif datesb >= timedelta(0) and dateee > timedelta(0):
			pass
		#su kien bat dau trong tuan va ket thuc trong tuan
		else:
			pass


	var = RequestContext(request, {
		"listfc": lfc,
		"listhour": GMT_time,
		"listgc": lgc,
		"weeks": weeklist[:count-1],
		"weekdays": weekday,
		"user": request.user,
		"year": year,
		"month": month,
		"day": day,
		"reminders":reminders(request)
	})

	return render_to_response("week.html", var)

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
				entry.date_start = datetime(int(year), int(month), int(day), 12, 50)
				entry.date_end = date(int(year), int(month), int(day), 15, 30)
				entry.save()
			return HttpResponseRedirect(reverse(
				'Calendar_Learn.Calendar.views.month',
				args = (year, month)
			))
	else:
		#display formset for existing entries and one extra form
		formset = EntriesFormset(
			queryset = Entry.objects.filter(
				date_start__year = year,
				date_start__month = month,
				date_start__day = day,
				creator = request.user
			)
		)
	other_entries = []
	if _show_users(request) :
		other_entries = Entry.objects.filter(
			date_start__year = year,
			date_start__month = month,
			date_start__day = day,
		).exclude(creator = request.user)
	return render_to_response('day.html', add_csrf(
		request,
		entries = formset, 
		year = year,
		month = month,
		day = day,
		reminders=reminders(request)
	))

"""def create_event(request, year, month):
	user = get_object_or_404(User, username = request.user.username)

	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid:


	if "id" in request.GET:
"""		
def add_csrf(request, **kwargs):
	"""Add csrf adn use to dictionary."""
	d = dict(user = request.user, **kwargs)
	d.update(csrf(request))
	return d

def register_page(request):
	if request.method=='POST':
		form=RegistrationForm(request.POST)
		if form.is_valid():
			user=User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password2'],
				email=form.cleaned_data['email']
			)
			#user_profile=UserProfile.objects.create(
			#	username=form.cleaned_data['username'],
			#	first_name=form.cleaned_data['first_name'],
			#	last_name=form.cleaned_data['last_name'],
			#	birthday=form.cleaned_data['birthday']
			#	
			#)
			#user_profile.save()"""
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
		date_start__year = year,
		date_start__month = month,
		date_start__day = day,
		creator = request.user,
		remind = True
	)
	tomorrow = datetime.now() + timedelta(days = 1)
	year, month, day = tomorrow.timetuple()[:3]

	return list(reminders) + list(Entry.objects.filter(
		date_start__year = year,
		date_start__month = month,
		date_start__day = day,
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

@login_required(login_url='/login/')
def create_group(request):
	if request.method == 'POST':
		form=CreateGroupForm(request.POST)
		if form.is_valid():
			groupcalendar=GroupCalendar.objects.create(
				name=form.cleaned_data['name'],
				creator_group=request.user,
				describe=form.cleaned_data['describe'],
				group_email=form.cleaned_data['group_email'],
				is_public=form.cleaned_data['is_public'],
			)
			groupcalendar.save()

			return HttpResponseRedirect('/Group/group.html/')
	else:
		form=CreateGroupForm()
	variables=RequestContext(request, { 'form':form})

	return render_to_response('Group/create_group.html', variables)

def group_view(request, groupname):
	group=get_object_or_404(GroupCalendar, name=groupname)

	if request.user.is_authenticated():
		is_mem = GroupMem.objects.filter(
			user_mem = request.user,
			group_name = group,
		)
	else:
		is_mem = False

	try:
		mems=GroupMem.objects.filter(group_name=group)
	except:
		mems=None

	listmem=[]
	n = 0
	for mem in mems:
		try:
			pic_profile_mem=Image.objects.get(user=mem.user_mem, is_use=True)
		except:
			pic_profile_mem=None
		listmem.append((n, mem, pic_profile_mem))
		n=n+1

	variables=RequestContext(request, {
		'group': group,
		'listmem': listmem,
		'is_mem': is_mem,
		'down': n,
	})

	return render_to_response('Group/group.html', variables)

@login_required(login_url = '/login/')
def join_group(request):
	if 'group_name' in request.GET:
		group = get_object_or_404(
			GroupCalendar, name = request.GET['group_name']
		)

		joinmem, newmem = GroupMem.objects.get_or_create(	
			user_mem = request.user,
			group_name = group
		)
		try:
			newmem.save()
			request.user.message_set.create(
				message = u'You was added to group %s.' % group.name 
			)
		except:
			request.user.message_set.create(
				message = u'You is already a member of group: %s' % group.name 
			)
		return HttpResponseRedirect(
			'/group/%s/' % group.name
		)
	else:
		raise Http404

@login_required(login_url='/login/')
def group_month(request, groupname, year, month, change=None):
	"""Listing of days in `month`."""
	group=get_object_or_404(GroupCalendar, name=groupname)
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
			entries = GroupEntry.objects.filter(
				date_start__year=day.year, 
				date_start__month=day.month, 
				date_start__day=day.day,
				group_name=group,
			)
			if not _show_users(request):
				entries = entries.filter(creator=request.user)
			if day.day == nday and day.year == nyear and day.month == nmonth:
				current = True
		lst[week].append((day.day, day.month, entries, current))
		if len(lst[week]) == 7:
			lst.append([])
			week += 1

	return render_to_response("Group/group_month.html", dict(
		year=year, 
		month=month, 
		user=request.user,
		group_name=groupname,
		month_days=lst[:week],
		mname=mnames[month-1], 
		reminders=reminders(request)
	))

@login_required(login_url = '/login/')
def group_day(request, groupname, year, month, day):
	"""Entries for day"""
	group=get_object_or_404(GroupCalendar, name=groupname)
	EntriesFormset = modelformset_factory(
		GroupEntry,
		extra = 1,
		exclude = ('group_name', 'creator', 'date_start', 'date_end'),
		can_delete = True
	)
	hour=12
	minute=50
	if request.method == 'POST':
		formset = EntriesFormset(request.POST)
		if formset.is_valid:
			#add current user and date to each entry and save
			entries = formset.save(commit = False)
			for entry in entries:
				entry.group_name=group
				entry.creator = request.user
				entry.date_start=datetime(int(year), int(month), int(day), int(hour), int(minute))
				entry.date_end=datetime(int(year), int(month), int(day), int(hour), int(minute))
				entry.save()
			return HttpResponseRedirect(reverse(
				'Calendar_Learn.Calendar.views.group_month',
				args = (groupname, year, month)
			))
	else:
		#display formset for existing entries and one extra form
		formset = EntriesFormset(
			queryset = GroupEntry.objects.filter(
				date_start__year = year,
				date_start__month = month,
				date_start__day = day,
				group_name=group,
			)
		)
	other_entries = []
	#if _show_users(request) :
	#	other_entries = Entry.objects.filter(
	#		date__year = year,
	#		date__month = month,
	#		date__day = day,
	#	).exclude(creator = request.user)
	return render_to_response('Group/group_day.html', add_csrf(
		request,
		group_name=groupname,
		entries = formset, 
		year = year,
		month = month,
		day = day,
		reminders=reminders(request)
	))

@login_required(login_url = '/login/')
def g_event_edit(request, groupname, year, month, id_e):
	group=get_object_or_404(GroupCalendar, name=groupname)
	entry=get_object_or_404(GroupEntry, pk=id_e)
	if request.method == 'POST':
		form=AddEntryGroupForm(request.POST)
		if form.is_valid():
			dele=form.cleaned_data['dele']
			if dele:
				entry.delete()
			else:
				entry.title=form.cleaned_data['title']
				entry.snippet=form.cleaned_data['snippet']
				entry.body=form.cleaned_data['body']
				entry.date_start=form.cleaned_data['date_start']
				entry.date_end=form.cleaned_data['date_end']
				entry.remind=form.cleaned_data['remind']
				entry.save()
			return HttpResponseRedirect(reverse(
				'Calendar_Learn.Calendar.views.group_month',
				args = (groupname, year, month)
			))
	else:
		form=AddEntryGroupForm({
			'title': entry.title,
			'snippet': entry.snippet,
			'body': entry.body,
			'date_start': entry.date_start,
			'date_end': entry.date_end,
			'remind': entry.remind,
			'dele': False,
		})

	variables=RequestContext(request, {
		'form': form,
		'id_e': entry.pk,
		'groupname': groupname,
		'reminders': reminders(request),
	})

	return render_to_response('Group/group_day_edit.html', variables)
"""	
@login_required(login_url='/login/')
def month(request, year, month, change=None):
	#Listing of days in `month`.
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
				date__day=day.day,
				creator=request.user
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
	))"""
