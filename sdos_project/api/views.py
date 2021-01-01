import json
from datetime import datetime
from django.http import JsonResponse
from django.utils.timezone import make_aware # Naive to native
from django.contrib.auth.decorators import login_required

from users.models import *
from users.decorators import mentee_required, mentor_required


def __get_choices(s: str, ChoiceClass):
	res = [{
		'key': -1,
		'value': 'Any ' + s
	}]

	for i, r in enumerate(ChoiceClass.choices):
		res.append({
			'key': i,
			'value': str(r[-1])
		})

	return res


@login_required
@mentee_required
def get_mentor_roles(request):
	response = {
		'success': True,
		'roles': __get_choices('role', MentorRoles)
	}

	return JsonResponse(response, safe=False)


@login_required
@mentee_required
def get_mentor_fields(request):
	response = {
		'success': True,
		'fields': __get_choices('field', Fields)
	}

	return JsonResponse(response, safe=False)


@login_required
@mentee_required
def get_mentor_areas(request):
	response = {
		'success': True,
		'areas': __get_choices('area', Areas)
	}

	return JsonResponse(response, safe=False)


def get_role_id(role: str, Roles):
	return next(filter(lambda x: x[-1] == role, Roles.choices))[0] if role else None


def get_field_id(field: str):
	return next(filter(lambda x: x[-1] == field, Fields.choices))[0] if field else None


def get_area_id(area: str):
	return next(filter(lambda x: x[-1] == area, Areas.choices))[0] if area else None


def filter_mentors(role: str, field: str, area: str):
	role = get_role_id(role, MentorRoles)
	field = get_field_id(field)
	area = get_area_id(area)

	options = dict()
	if role:
		options['role'] = role

	if field:
		options['field'] = field

	shortlist = [m.mentor for m in MentorRoleField.objects.filter(**options)]
	if not area:
		return shortlist

	return [m for m in shortlist if m.mentorarea.area == area]


# TODO: Filters
@login_required
@mentee_required
def search_users(request):
	user = request.user
	role = request.GET.get('role')
	field = request.GET.get('field')
	area = request.GET.get('area')

	role = None if (role == 'Any role') else role
	field = None if (field == 'Any field') else field
	area = None if (area == 'Any area') else area

	mentors = filter_mentors(role, field, area)

	# Status codes
	REQUEST_MENTORSHIP = 0
	PENDING_REQUEST = 1
	MY_MENTOR = 2

	shortlist = []
	for mentor in mentors:
		if MyMentor.objects.filter(mentor=mentor, mentee=user.account.mentee).exists():
			status = MY_MENTOR
		elif MenteeSentRequest.objects.filter(mentor=mentor, mentee=user.account.mentee).exists():
			status = PENDING_REQUEST
		else:
			status = REQUEST_MENTORSHIP

		shortlist.append({
			'id': mentor.account.id,
			'username': mentor.account.user.username,
			'is_mentor': mentor.account.is_mentor,
			'status': status
		})

	return JsonResponse(shortlist, safe=False)


@login_required
@mentee_required
def send_mentorship_request(request):
	user = request.user
	requestee = request.GET.get('requestee')
	requestee = User.objects.get(username=requestee)
	sop = request.GET.get('sop')
	expectations = request.GET.get('expectations')
	commitment = request.GET.get('commitment')
	
	status = False
	
	if MenteeSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestee.account.mentor).exists():
		# Checks if mentee has already sent a request to the mentor
		pass
	elif MyMentor.objects.filter(mentee=user.account.mentee, mentor=requestee.account.mentor).exists():
		# Checks if the user is already a mentee of the requestee
		pass
	elif len(MenteeSentRequest.objects.filter(mentee=user.account.mentee)) + len(MyMentor.objects.filter(mentee=user.account.mentee)) == 3:
		# If mentee has already sent 3 requests
		pass
	else:
		status = True
		MentorshipRequestMessage.objects.create(mentee=user.account.mentee, mentor=requestee.account.mentor, 
			sop=sop, expectations=expectations, commitment=commitment
		)
		MenteeSentRequest.objects.create(mentee=user.account.mentee, mentor=requestee.account.mentor)

	return JsonResponse({"success" : status})


@login_required
@mentor_required
def get_user_requests(request):
	user = request.user
	user_requests = []
	
	for user_request in MenteeSentRequest.objects.filter(mentor=user.account.mentor):

		mrm = MentorshipRequestMessage.objects.filter(mentor=user.account.mentor, mentee=user_request.mentee)
		assert(len(mrm) == 1)
		mrm = mrm.first()
		
		user_requests.append({
			'id': user_request.id,
			'username': user_request.mentee.account.user.username,
			'sop': mrm.sop,
			'expectations': mrm.expectations,
			'commitment': mrm.commitment,
		})
	
	return JsonResponse(user_requests, safe=False)


# TODO : 1. avoid duplicate requests, 
# TODO : 2. check if the request already exists
# TODO : 3. check if the user and the requestor are of different type (mentor / mentee)
@login_required
@mentor_required
def accept_mentorship_request(request):
	user = request.user
	requestor = request.GET.get('requestor')
	requestor = User.objects.get(username=requestor)

	status = False
	if MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).exists():
		# executes only if, requestor is not already a mentee of the user and it is the requestor that sent the 
		# mentorship request to the user
		MyMentee.objects.create(mentor=user.account.mentor, mentee=requestor.account.mentee)
		MyMentor.objects.create(mentor=user.account.mentor, mentee=requestor.account.mentee)
		MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).delete()
		MentorshipRequestMessage.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).delete()
		status = True
	
	return JsonResponse({"success" : status})


# TODO : 1. avoid duplicate requests, 
# TODO : 2. check if the request already exists
# TODO : 3. check if the user and the requestor are of different type (mentor / mentee)
@login_required
@mentor_required
def reject_mentorship_request(request):
	user = request.user
	to_reject = request.GET.get('requestor')
	to_reject = User.objects.get(username=to_reject)

	status = False
	if MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=to_reject.account.mentee).exists():
		# delete a request only if the request exists
		MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=to_reject.account.mentee).delete()
		MentorshipRequestMessage.objects.filter(mentor=user.account.mentor, mentee=to_reject.account.mentee).delete()
		status = True

	return JsonResponse({"success" : status})
	

@login_required
@mentee_required
def get_mentors(request):
	user = request.user
	# TODO: get a list of mentors only and not a list of mentor / mentee
	# SUGGESTED EDIT: mentors = map(lambda x: x.mentor, mentors)
	mentors = MyMentor.objects.filter(mentee=user.account.mentee)

	mentor_ids = []
	for mentor in mentors:
		mentor_ids.append({
			'id': mentor.id,
			'username': mentor.mentor.account.user.username
		})
	
	response = {
		'mentors': mentor_ids,
		'success': True
	}

	return JsonResponse(response, safe=False)


@login_required
@mentor_required
def get_mentees(request):
	user = request.user
	mentees = MyMentee.objects.filter(mentor=user.account.mentor)

	mentee_ids = []
	for mentee in mentees:
		mentee_ids.append({
			'id': mentee.id,
			'username': mentee.mentee.account.user.username
		})

	response = {
		'mentees': mentee_ids,
		'success': True
	}

	return JsonResponse(response, safe=False)


@login_required
def get_chatters(request):
	user = request.user
	chatters = []

	if user.account.is_mentor:
		mentees = MyMentee.objects.filter(mentor=user.account.mentor)
		for mentee in mentees:
			chatters.append({
				'id': mentee.id,
				'username': mentee.mentee.account.user.username,
				"first_name": mentee.mentee.account.user.first_name,
				"last_name": mentee.mentee.account.user.last_name,
				"gender": mentee.mentee.account.gender,
			})
	else:
		mentors = MyMentor.objects.filter(mentee=user.account.mentee)
		for mentor in mentors:
			chatters.append({
				'id': mentor.id,
				'username': mentor.mentor.account.user.username,
				'first_name': mentor.mentor.account.user.first_name,
				'last_name': mentor.mentor.account.user.last_name,
				'gender': mentor.mentor.account.gender,
			})

	print(chatters)

	response = {
		'chatters': chatters,
		'success': True
	}
	return JsonResponse(response, safe=False)


@login_required
@mentee_required
def get_recommendations(request):
	mentors = []
	for mentor in Mentor.objects.all():
		mentors.append(
			{
				"id": mentor.id,
				"username": mentor.account.user.username,
			}
		)
	response = {
		'recommendations': mentors,
		'success': True
	}

	return JsonResponse(response, safe=False)


@login_required
def update_settings(request):
	user = request.user

	if user.account.is_mentor:	
		mentorship_duration = json.loads(request.body.decode('utf-8'))['mentorship_duration']
		is_open_to_mentorship = json.loads(request.body.decode('utf-8'))['is_open_to_mentorship']
		
		will_mentor_faculty = json.loads(request.body.decode('utf-8'))['will_mentor_faculty']
		will_mentor_phd = json.loads(request.body.decode('utf-8'))['will_mentor_phd']
		will_mentor_mtech = json.loads(request.body.decode('utf-8'))['will_mentor_mtech']
		will_mentor_btech = json.loads(request.body.decode('utf-8'))['will_mentor_btech']
		responsibilities = json.loads(request.body.decode('utf-8'))['willing_to']
		other_responsibility = json.loads(request.body.decode('utf-8'))['other_responsibility']


		
		user.account.mentor.mentorship_duration = mentorship_duration
		user.account.mentor.is_open_to_mentorship = is_open_to_mentorship
		user.account.mentor.will_mentor_faculty = will_mentor_faculty
		user.account.mentor.will_mentor_phd = will_mentor_phd
		user.account.mentor.will_mentor_mtech = will_mentor_mtech
		user.account.mentor.will_mentor_btech = will_mentor_btech

		s = 'responsibility'
		for i in range(len(responsibilities)):
			setattr(user.account.mentor, s + str(i+1), responsibilities[i])

		user.account.mentor.other_responsibility = other_responsibility

		user.account.mentor.save()

	else:
		needs_mentoring = json.loads(request.body.decode('utf-8'))['needs_mentoring']
		needs_urgent_mentoring = json.loads(request.body.decode('utf-8'))['needs_urgent_mentoring']

		user.account.mentee.needs_mentoring = needs_mentoring
		user.account.mentee.needs_urgent_mentoring = needs_urgent_mentoring
		user.account.mentee.save()

	return JsonResponse({'success': True})


@login_required
def get_settings(request):
	user = request.user
	
	if user.account.is_mentor:

		response = {
			'success': True,
			'mentorship_duration': user.account.mentor.mentorship_duration,
			'is_open_to_mentorship': user.account.mentor.is_open_to_mentorship,
			'will_mentor_faculty': user.account.mentor.will_mentor_faculty,
			'will_mentor_phd': user.account.mentor.will_mentor_phd,
			'will_mentor_mtech': user.account.mentor.will_mentor_mtech,
			'will_mentor_btech': user.account.mentor.will_mentor_btech,
			'responsibilities': [],
			'other_responsibility': user.account.mentor.other_responsibility,
		}

		s = 'responsibility'
		for i, j in MentorResponsibility.choices:
			response['responsibilities'].append( 
				(getattr(user.account.mentor, s + str(i)), j)
			)
	else:

		response = {
			'success': True,
			'needs_mentoring': user.account.mentee.needs_mentoring,
			'needs_urgent_mentoring': user.account.mentee.needs_urgent_mentoring
		}

	return JsonResponse(response)


@login_required
def get_messages(request, chatter_username):
	chatter_user = User.objects.filter(username=chatter_username).first()
	
	messages_sent = Message.objects.filter(sender=request.user.account, receiver=chatter_user.account)
	messages_received = Message.objects.filter(receiver=request.user.account, sender=chatter_user.account)

	messages = [{'sender': msg.sender.user.username, 'content': msg.content, 'timestamp': msg.time_posted, 'by_me': True} for msg in messages_sent] + \
	[{'sender': msg.sender.user.username, 'content': msg.content, 'timestamp': msg.time_posted, 'by_me': False} for msg in messages_received]

	messages = sorted(messages, key=lambda msg: msg['timestamp'])
	
	for i in range(len(messages)):
		timestamp = messages[i]['timestamp']
		date = timestamp.strftime("%d %b")
		time = timestamp.strftime("%H:%M")
		messages[i]['timestamp'] = time
		messages[i]['date'] = date


	response = {
		'success': True,
		'messages': messages,
	}
	
	return JsonResponse(response, safe=False)


@login_required
def send_message(request):
	message = json.loads(request.body.decode('utf-8'))['message']
	receiver_user = User.objects.filter(username=message['receiver']).first()
	Message.objects.create(sender=request.user.account, 
							receiver=receiver_user.account, 
							content=message['content'])

	return JsonResponse({'success': True})


@login_required
def get_meetings(request, guest_name):
	user = request.user

	if guest_name == "undefined":
		meeting_created_by_me = Meeting.objects.filter(creator=user.account).all()
		meeting_created_for_me = Meeting.objects.filter(guest=user.account).all()

	else:
		guest = User.objects.filter(username=guest_name).first()
		meeting_created_by_me = Meeting.objects.filter(creator=user.account, guest=guest.account).all()
		meeting_created_for_me = Meeting.objects.filter(creator=guest.account, guest=user.account).all()

	fields = ('title', 'agenda', 'time', 'meeting_url')
	meetings = [dict((field, getattr(meeting, field)) for field in fields) for meeting in meeting_created_by_me] + \
		[dict((field, getattr(meeting, field)) for field in fields) for meeting in meeting_created_for_me]

	meetings.sort(key=lambda x: x['time'])

	for i in range(len(meetings)):
		meetings[i]['day'] = meetings[i]['time'].strftime('%a')
		meetings[i]['date'] = meetings[i]['time'].strftime('%d %b')
		meetings[i]['time'] = meetings[i]['time'].strftime('%H:%M')

	response = {
		'success': True,
		'meetings': meetings,
	}

	return JsonResponse(response)


@login_required
def add_meeting(request):
	user = request.user
	req = json.loads(request.body)
	guest_name = req.get('guest_name')

	if not guest_name:
		print('[ERROR] guest_name is None')
		return JsonResponse({'success': False})

	guest = User.objects.filter(username=guest_name).first()
	req['time'] = make_aware(datetime.strptime(req['time'], '%Y-%m-%dT%H:%M'))

	Meeting.objects.create(creator=user.account,
							guest=guest.account,
							title=req['title'],
							agenda=req['agenda'],
							time=req['time'],
							meeting_url=req['meeting_url'])

	response = {
		'success': True
	}

	return JsonResponse(response)


@login_required
def get_meeting_summaries(request, guest_name):
	user = request.user
	guest = User.objects.get(username=guest_name)

	mentor, mentee = user, guest
	if user.account.is_mentee and guest.account.is_mentor:
		mentor, mentee = guest, user

	elif user.account.is_mentee == guest.account.is_mentee:
		print('[ERROR] Both users of same type')
		return JsonResponse({'success': False})
	
	summaries = MeetingSummary.objects.filter(mentor=mentor.account.mentor, mentee=mentee.account.mentee).all()

	fields = ('meeting_date', 'meeting_length', 'meeting_details', 'meeting_todos',
				'next_meeting_date', 'next_meeting_agenda')

	summaries = [dict((field, getattr(summary, field)) for field in fields) for summary in summaries]
	summaries.sort(key=lambda x: x['meeting_date'], reverse=True)

	for i in range(len(summaries)):
		summaries[i]['day'] = summaries[i]['meeting_date'].strftime('%a')
		summaries[i]['date'] = summaries[i]['meeting_date'].strftime('%d %b')
		summaries[i]['time'] = summaries[i]['meeting_date'].strftime('%H:%M')

	response = {
		'success': True,
		'summaries': summaries,
	}

	return JsonResponse(response)


@login_required
def add_meeting_summary(request):
	user = request.user
	req = json.loads(request.body)
	guest_name = req.get('guest_name')

	if not guest_name:
		print('[ERROR] guest_name is None')
		return JsonResponse({'success': False})

	guest = User.objects.get(username=guest_name)
	req['meeting_date'] = make_aware(datetime.strptime(req['meeting_date'], '%Y-%m-%dT%H:%M'))

	mentor, mentee = user, guest
	if user.account.is_mentee and guest.account.is_mentor:
		mentor, mentee = guest, user

	elif user.account.is_mentee == guest.account.is_mentee:
		print('[ERROR] Both users of same type')
		return JsonResponse({'success': False})

	MeetingSummary.objects.create(mentor=mentor.account.mentor,
								mentee=mentee.account.mentee,
								meeting_date=req['meeting_date'],
								meeting_length=req['meeting_length'],
								meeting_details=req['meeting_details'],
								meeting_todos=req['meeting_todos'],
								next_meeting_date=req['next_meeting_date'],
								next_meeting_agenda=req['next_meeting_agenda'])

	response = {
		'success': True
	}

	return JsonResponse(response)

@login_required
def get_milestones(request):
	mentor_name = request.GET.get('mentor')
	mentee_name = request.GET.get('mentee')
	
	mentor = User.objects.get(username=mentor_name).account.mentor
	mentee = User.objects.get(username=mentee_name).account.mentee

	milestones = Milestone.objects.filter(mentor=mentor, mentee=mentee).all()
	milestones = [milestone.content for milestone in milestones]

	response = {
		'milestones': milestones,
		'success': True
	}
	return JsonResponse(response, safe=False)

@login_required
@mentor_required
def add_milestone(request):
	req = json.loads(request.body)

	mentor_name = req.get('mentor')
	mentee_name = req.get('mentee')
	content = req.get('content')
	
	mentor = User.objects.get(username=mentor_name).account.mentor
	mentee = User.objects.get(username=mentee_name).account.mentee

	Milestone.objects.create(mentor=mentor, mentee=mentee, content=content)

	return JsonResponse({'success': True})



