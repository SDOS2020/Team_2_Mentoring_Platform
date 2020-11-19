from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
from django.utils.timezone import make_aware # Naive to native
from users.models import (
	User,
	Account, 
	Mentor, 
	Mentee, 
	MenteeSentRequest, 
	MentorSentRequest, 
	MyMentee, 
	MyMentor,
	Roles,
	Fields,
	MentorRoleField,
	MenteeRoleField,
	MentorExpectedRoleField,
	MenteeExpectedRoleField,
	Message,
	Meeting,
)


@login_required
def get_tags(request):
	tags = []

	i = 0
	# Add (role, NULL)
	for role in Roles.choices:
		r = str(role[-1])
		tags.append({
			'key': i,
			'role': r,
			'field': None,
			'value': r
		})

		i += 1

	# Add (NULL, field)
	for field in Fields.choices:
		f = str(field[-1])
		tags.append({
			'key': i,
			'role': None,
			'field': f,
			'value': f
		})

		i += 1

	# Add (role, field)
	for role in Roles.choices:
		r = str(role[-1])
		for field in Fields.choices:
			f = str(field[-1])
			tags.append({
				'key': i,
				'role': r,
				'field': f,
				'value': r + ' ' + f
			})

			i += 1

	response = {
		'success': True,
		'tags': tags
	}

	return JsonResponse(response, safe=False)


@login_required
def get_my_tags(request):
	my_tags = []

	if request.user.account.is_mentor:
		my_tags = MentorExpectedRoleField.objects.filter(mentor=request.user.account.mentor)
	else:
		my_tags = MenteeExpectedRoleField.objects.filter(mentee=request.user.account.mentee)

	my_tags = [{
		'role': my_tag.get_role_display(), 
		'field': my_tag.get_field_display(),
		'value': my_tag.get_role_display() + ' ' + my_tag.get_field_display(),
	} for my_tag in my_tags]
	
	response = {
		'success': True,
		'my_tags': my_tags
	}

	return JsonResponse(response, safe=False)


def get_role_id(role: str):
	return next(filter(lambda x: x[-1] == role, Roles.choices))[0] if role else None


def get_field_id(field: str):
	return next(filter(lambda x: x[-1] == field, Fields.choices))[0] if field else None


def filter_mentor(mentor, filters):
	if not filters:  # If no filter is applied
		return True

	for f in filters:
		role, field = get_role_id(f['role']), get_field_id(f['field'])
		options = dict()

		if role:
			options['role'] = role

		if field:
			options['field'] = field

		if MentorRoleField.objects.filter(mentor=mentor, **options).exists():
			return True

	return False


def filter_mentee(mentee, filters):
	if not filters:  # If no filter is applied
		return True

	for f in filters:
		role, field = get_role_id(f['role']), get_field_id(f['field'])
		options = dict()

		if role:
			options['role'] = role

		if field:
			options['field'] = field

		if MenteeRoleField.objects.filter(mentee=mentee, **options).exists():
			return True

	return False


# TODO: Filters
@login_required
def search_users(request):
	user = request.user
	pattern = request.GET.get('pattern')
	filters = json.loads(request.GET.get('filters'))
	mentors_allowed = request.GET.get('mentors_allowed') == 'true'
	mentees_allowed = request.GET.get('mentees_allowed') == 'true'

	print(Mentor.objects.all())
	print(Mentee.objects.all())
	print(filters)
	print(pattern)
	print(mentors_allowed)
	print(mentees_allowed)

	shortlist = []

	# Status codes
	NOT_ALLOWED = 0
	REQUEST_MENTORSHIP = 1
	REQUEST_MENTEESHIP = 2
	PENDING_REQUEST = 3
	REQUEST_RECEIVED = 4
	MY_MENTEE = 5
	MY_MENTOR = 6

	if user.account.is_mentor:
		# current user is mentor
		for account in Account.objects.all():
			status = NOT_ALLOWED

			if account.is_mentor != user.account.is_mentor:
				# current user is a mentor, other user is a mentee
				if not mentees_allowed:
					continue

				if not filter_mentee(account.mentee, filters):
					continue

				if MyMentee.objects.filter(mentor=user.account.mentor, mentee=account.mentee).exists():
					status = MY_MENTEE
				elif MentorSentRequest.objects.filter(mentor=user.account.mentor, mentee=account.mentee).exists():
					status = PENDING_REQUEST
				elif MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=account.mentee).exists():
					status = REQUEST_RECEIVED
				else:
					status = REQUEST_MENTEESHIP
			else:
				if not mentors_allowed:
					continue

				if not filter_mentor(account.mentor, filters):
					continue

			if pattern.lower() in account.user.username.lower():
				shortlist.append({
					'id': account.id,
					'username': account.user.username,
					'is_mentor': account.is_mentor,
					'status': status
				})
	else:
		# current user is mentee
		for account in Account.objects.all():
			status = NOT_ALLOWED
			if account.is_mentor != user.account.is_mentor:
				# current user is a mentee, other user is a mentor
				if not mentors_allowed:
					continue

				if not filter_mentor(account.mentor, filters):
					continue

				if MyMentor.objects.filter(mentor=account.mentor, mentee=user.account.mentee).exists():
					status = MY_MENTOR
				elif MenteeSentRequest.objects.filter(mentor=account.mentor, mentee=user.account.mentee).exists():
					status = PENDING_REQUEST
				elif MentorSentRequest.objects.filter(mentor=account.mentor, mentee=user.account.mentee).exists():
					status = REQUEST_RECEIVED
				else:
					status = REQUEST_MENTORSHIP
			else:
				if not mentees_allowed:
					continue

				if not filter_mentee(account.mentee, filters):
					continue

			if pattern.lower() in account.user.username.lower():
				shortlist.append({
					'id': account.id,
					'username': account.user.username,
					'is_mentor': account.is_mentor,
					'status': status
				})

	return JsonResponse(shortlist, safe=False)


# TODO : 1. avoid duplicate requests, 
# TODO : 2. check if the person is already a mentor / mentee
# TODO : 3. Assumption that the user and the requestee are different types of users
# user is a mentee, requestee is a mentor
def send_mentorship_request(user, requestee):
	status = False
	
	if MenteeSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestee.account.mentor).exists():
		# Checks if mentee has already sent a request to the mentor
		pass
	elif MentorSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestee.account.mentor).exists():
		# Checks if the mentor has already sent a request to the mentee
		pass
	elif MyMentor.objects.filter(mentee=user.account.mentee, mentor=requestee.account.mentor).exists():
		# checks if the user is already a mentee of the requestee
		pass
	else:
		status = True
		MenteeSentRequest.objects.create(mentee=user.account.mentee, mentor=requestee.account.mentor)
	
	return JsonResponse({"success" : status})


# TODO : 1. avoid duplicate requests, 
# TODO : 2. check if the person is already a mentor / mentee
# TODO : 3. Assumption that the user and the requestee are different types of users
# user is a mentor, requestee is a mentee
def send_menteeship_request(user, requestee):
	status = False

	if MentorSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestee.account.mentee).exists():
		# Checks if mentor has already sent a request to the mentee
		pass
	elif MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestee.account.mentee).exists():
		# Checks if mentee has already sent a request to the mentor
		pass
	elif MyMentee.objects.filter(mentor=user.account.mentor, mentee=requestee.account.mentee).exists():
		# checks if the user is already a mentor of the requestee
		pass
	else:
		status = True
		MentorSentRequest.objects.create(mentor=user.account.mentor, mentee=requestee.account.mentee)
	
	return JsonResponse({"success" : status})


@login_required
def send_request(request):
	user = request.user
	requestee = request.GET.get('requestee')
	requestee = User.objects.get(username=requestee)

	if user.account.is_mentor and requestee.account.is_mentee:
		return send_menteeship_request(user, requestee)
	
	if user.account.is_mentee and requestee.account.is_mentor:
		return send_mentorship_request(user, requestee)
	
	return JsonResponse({"success" : False})


@login_required
def get_user_requests(request):
	user = request.user
	print(user)

	user_requests = []
	
	if user.account.is_mentor:
		for user_request in MenteeSentRequest.objects.filter(mentor=user.account.mentor):
			user_requests.append({
				'id': user_request.id,
				'username': user_request.mentee.account.user.username
			})
	else:
		for user_request in MentorSentRequest.objects.filter(mentee=user.account.mentee):
			user_requests.append({
				'id': user_request.id,
				'username': user_request.mentor.account.user.username
			})
	
	return JsonResponse(user_requests, safe=False)


# user is a mentor, requestor is a mentee
def accept_mentorship_request(user, requestor):
	status = False

	if MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).exists():
		# executes only if, requestor is not already a mentee of the user and it is the requestor that sent the 
		# mentorship request to the user
		MyMentee.objects.create(mentor=user.account.mentor, mentee=requestor.account.mentee)
		MyMentor.objects.create(mentor=user.account.mentor, mentee=requestor.account.mentee)
		MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).delete()
		status = True

	return JsonResponse({"success" : status})


# user is a mentee, requestor is a mentor
def accept_menteeship_request(user, requestor):
	status = False

	if MentorSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestor.account.mentor).exists():
		# executes if mentor is not already the mentor of the mentee
		# and if mentor actually sent a mentorship request to the mentee
		MyMentor.objects.create(mentee=user.account.mentee, mentor=requestor.account.mentor)
		MyMentee.objects.create(mentee=user.account.mentee, mentor=requestor.account.mentor)
		MentorSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestor.account.mentor).delete()
		status = True

	return JsonResponse({"success": status})


# TODO : 1. avoid duplicate requests, 
# TODO : 2. check if the request already exists
# TODO : 3. check if the user and the requestor are of different type (mentor / mentee)
@login_required
def accept_request(request):
	user = request.user
	requestor = request.GET.get('requestor')
	requestor = User.objects.get(username=requestor)
	print('Got requestor:', requestor)

	if user.account.is_mentor and requestor.account.is_mentee:
		return accept_mentorship_request(user, requestor)
	
	if user.account.is_mentee and requestor.account.is_mentor:
		return accept_menteeship_request(user, requestor)
	
	return JsonResponse({"success" : False})


# user is a mentor, requestor is a mentee
def reject_mentorship_request(user, requestor):
	status = False

	if MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).exists():
		# delete a request only if the request exists
		MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).delete()
		status = True

	return JsonResponse({"success" : status})


# user is a mentee, requestor is a mentor
def reject_menteeship_request(user, requestor):
	status = False

	if MentorSentRequest.objects.filter(mentor=requestor.account.mentor, mentee=user.account.mentee).exists():
		# delete a request only if the request exists
		MentorSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestor.account.mentor).delete()
		status = True

	return JsonResponse({"success" : status})


# TODO : 1. avoid duplicate requests, 
# TODO : 2. check if the request already exists
# TODO : 3. check if the user and the requestor are of different type (mentor / mentee)
@login_required
def reject_request(request):
	user = request.user
	requestor = request.GET.get('requestor')
	requestor = User.objects.get(username=requestor)
	print('Got requestor:', requestor)

	if user.account.is_mentor and requestor.account.is_mentee:
		return reject_menteeship_request(user, requestor)
	
	if user.account.is_mentee and requestor.account.is_mentor:
		return reject_mentorship_request(user, requestor)
	
	return JsonResponse({"success" : False})
	

@login_required
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
def get_recommendations(request):
	mentors = []
	for mentor in Mentor.objects.all():
		mentors.append(
			{
				"id": mentor.id,
				"username": mentor.account.user.username
			}
		)
	response = {
		'recommendations': mentors,
		'success': True
	}

	return JsonResponse(response, safe=False)


@login_required
def update_my_tags(request):
	updated_tags = json.loads(request.body.decode('utf-8'))['updated_tags']

	if request.user.account.is_mentor:
		MentorExpectedRoleField.objects.filter(mentor=request.user.account.mentor).delete()
		for tag in updated_tags:
			MentorExpectedRoleField.objects.create(mentor=request.user.account.mentor, role=get_role_id(tag['role']), field=get_field_id(tag['field']))

	else:
		MenteeExpectedRoleField.objects.filter(mentee=request.user.account.mentee).delete()
		for tag in updated_tags:
			MenteeExpectedRoleField.objects.create(mentee=request.user.account.mentee, role=get_role_id(tag['role']), field=get_field_id(tag['field']))


	return JsonResponse({'success': True})

@login_required
def update_settings(request):
	user = request.user

	if user.account.is_mentor:	
		mentorship_duration = json.loads(request.body.decode('utf-8'))['mentorship_duration']
		is_open_to_mentorship = json.loads(request.body.decode('utf-8'))['is_open_to_mentorship']

		user.account.mentor.mentorship_duration = mentorship_duration
		user.account.mentor.is_open_to_mentorship = is_open_to_mentorship
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
		mentorship_duration = user.account.mentor.mentorship_duration
		is_open_to_mentorship = user.account.mentor.is_open_to_mentorship
		
		response = {
			'success': True,
			'mentorship_duration': mentorship_duration,
			'is_open_to_mentorship': is_open_to_mentorship
		}

	else:
		needs_mentoring = user.account.mentee.needs_mentoring
		needs_urgent_mentoring = user.account.mentee.needs_urgent_mentoring

		response = {
			'success': True,
			'needs_mentoring': needs_mentoring,
			'needs_urgent_mentoring': needs_urgent_mentoring
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
		time = messages[i]['timestamp'].strftime("%H:%M")
		messages[i]['timestamp'] = time

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

	if not guest_name:
		print('[ERROR] guest_name is None')
		return JsonResponse({'success': False})

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
