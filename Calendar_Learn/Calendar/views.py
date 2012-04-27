import time
import calendar
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.template import RequestContext
from Calendar.form import *
from Calendar_Learn.Calendar.models import *

#from django.core.files.base import File
#from django.views.decorators.csrf import csrf_exempt
#import datetime
#from django.http import HttpResponseRedirect, HttpResponse
#from django.contrib.auth.models import User

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()

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

    nowy, nowm, nowd = time.localtime()[:3]
    lst = []
    # create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1, year+2]:
        mlst = []
        for n, month in enumerate(mnames):
			# are there entry(s) for this month; current month?
            entry = current = False   
            entries = Entry.objects.filter(
				date__year=y, 
				date__month=n+1,
                creator=request.user
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
				current=current,

			))
        lst.append((y, mlst))
    currnentDate = []
    for n, month in enumerate(mnames):
        if( n+1 == nowm):
            currnentDate.append((nowd,nowm,month,nowy))
    listYear = range(year-10,year+10)
#    cal = calendar.TextCalendar()
#    for i in range(7):
#        listDate = cal.formatweekday(i-1,3)
    cal = calendar.Calendar()
    listDate = cal.itermonthdates(nowy,nowm)
    return render_to_response("main.html", dict(
		years=lst, 
		user=request.user, 
		year=year,
        reminders=reminders(request),
        listYear = listYear,
        currnentDate = currnentDate,
        listDate = listDate,
        oneRow = range(7),
        oneCol = range(6),
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
        'username': username,
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
            image=Image.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                photo=form.cleaned_data['photo'],
                is_use=form.cleaned_data['is_use']
            )
            image.save()
            return HttpResponseRedirect('/user/%s/photo' % request.user.username)
            
    else:
        form = AddPhotoForm()

    variables = RequestContext(request,{'form':form})
    return render_to_response('add_photo.html',variables)
	
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
    currentDate = []
    for numberM, nameM in enumerate(mnames):
        if( (numberM + 1) == nmonth):
            currentDate.append((nday,nmonth,nameM,nyear))
    listYear = range(year-10,year+10)
    listMonth=[]
    for num, nameM in enumerate(mnames):
        listMonth.append((num+1, nameM))
    return render_to_response("month.html", dict(
		year=year, 
		month=month, 
		user=request.user,
        month_days=lst[:week], 
<<<<<<< HEAD
        mname=mnames[month-1], 
        listfriend=listFriendCal,
        els1=els,
        listgroup=listGroupCal,
        reminders=reminders(request)
    ))

def calmi(hour, minute):
	mi = hour*60 + minute
	return mi
	
def week(request, year, month, day, change=None	):
	user = get_object_or_404(User, username = request.user.username)
	
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
	weeklist = [] #luu tru event trong tuan do
	weekday = [] #luu tru ngay thang trong tuan
	weeklist.append([])
	count = 1 #dem so ngay trong tuan
	nday = calendar.weekday(year, month, day)
	now_day = date(year, month, day)
	
	for i in range(7):
		this_day = now_day + timedelta(i - nday)
		weekday.append(this_day)
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
	
	var = RequestContext(request, {
		"listfc": lfc,
		"listgc": lgc,
		"weeks": weeklist[:count],
		"weekdays": weekday,
		"user": request.user,
		"year": year,
		"month": month,
		"day": day
	})
	
	return render_to_response("week.html", var)
		
=======
		mname=mnames[month-1], 
		reminders=reminders(request),
        listYear = listYear,
        listMonth = listMonth[:12],
        currentDate = currentDate,
	))
	
>>>>>>> f7b1b68ff0362506bed244cd2d02520460f78c1b
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
		day = day,
		reminders=reminders(request)
	))

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
			
			return HttpResponseRedirect('/Group/')
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
		joinmem = GroupMem(	
			user_mem = request.user,
			group_name = group
		)
		try:
			joinmem.save()
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
    currentDate = []
    for numberM, nameM in enumerate(mnames):
        if( (numberM + 1) == nmonth):
            currentDate.append((nday,nmonth,nameM,nyear))
    listYear = range(year-10,year+10)
    listMonth=[]
    for num, nameM in enumerate(mnames):
        listMonth.append((num+1, nameM))
    return render_to_response("Group/group_month.html", dict(
		year=year, 
		month=month, 
		user=request.user,
		group_name=groupname,
        month_days=lst[:week], 
		mname=mnames[month-1], 
		reminders=reminders(request),
        listYear = listYear,
        listMonth = listMonth[:12],
        currentDate = currentDate,
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
