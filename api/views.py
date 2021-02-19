import json
from datetime import datetime

from mentor_mentee.methods import send_email_custom
from users.forms import EditAreasForm
from django.http import JsonResponse
from django.core.mail import send_mail
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

def get_responsibilities(mentor):
	responsibilities = []
	s = 'responsibility'
	for i, j in MentorResponsibility.choices:
		if getattr(mentor, s + str(i)):
			responsibilities.append(j)
	return responsibilities


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

		mentor_details = {
			'id': mentor.account.id,
			'username': mentor.account.user.username,
			'is_mentor': mentor.account.is_mentor,
			'status': status,

			'mentorship_duration': mentor.mentorship_duration,
			'is_open_to_mentorship': mentor.is_open_to_mentorship,
			
			'will_mentor_faculty': mentor.will_mentor_faculty,
			'will_mentor_phd': mentor.will_mentor_phd,
			'will_mentor_mtech': mentor.will_mentor_mtech,
			'will_mentor_btech': mentor.will_mentor_btech,
			
			'responsibilities': get_responsibilities(mentor),
			'other_responsibility': mentor.other_responsibility,
		}

		shortlist.append(mentor_details)

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
	status_code = 0
	
	if MenteeSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestee.account.mentor).exists():
		# Checks if mentee has already sent a request to the mentor
		status_code = 1
	
	elif MyMentor.objects.filter(mentee=user.account.mentee, mentor=requestee.account.mentor).exists():
		# Checks if the user is already a mentee of the requestee
		status_code = 2
	
	elif len(MenteeSentRequest.objects.filter(mentee=user.account.mentee)) + len(MyMentor.objects.filter(mentee=user.account.mentee)) == 3:
		# If mentee has already sent 3 requests
		status_code = 3
	
	elif len(MyMentee.objects.filter(mentor=requestee.account.mentor)) + len(MenteeSentRequest.objects.filter(mentor=requestee.account.mentor)) == 5:
		# If mentor already has 5 mentees (or has received 5 requests)
		status_code = 4
	
	else: # Everything is fine
		status = True
		MentorshipRequestMessage.objects.create(mentee=user.account.mentee, mentor=requestee.account.mentor, 
			sop=sop, expectations=expectations, commitment=commitment
		)
		MenteeSentRequest.objects.create(mentee=user.account.mentee, mentor=requestee.account.mentor)
		send_email_custom(to=[user.email], subject="Request submitted", body=f"Your request to {requestee.first_name} "
																			f"has been created!")
		send_email_custom(to=[requestee.email], subject="Request received", body=f"Request from {user.first_name} "
																			   f"received.")

	return JsonResponse({"success": status, "status_code": status_code})


@login_required
@mentee_required
def cancel_mentorship_request(request):
	user = request.user
	request_to = request.GET.get('request_to')
	request_to = User.objects.get(username=request_to)

	if request_to.account.is_mentee:
		print('Invalid request! Cannot send request to mentees in the first place')
		return JsonResponse({'success': False})

	status = False
	if MenteeSentRequest.objects.filter(mentor=request_to.account.mentor, mentee=user.account.mentee).exists():
		# Delete a request only if the request exists
		MenteeSentRequest.objects.filter(mentor=request_to.account.mentor, mentee=user.account.mentee).delete()
		MentorshipRequestMessage.objects.filter(mentor=request_to.account.mentor, mentee=user.account.mentee).delete()
		status = True

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

		mentee_account = user_request.mentee.account
		_educations = AccountEducation.objects.filter(account=mentee_account).all()
		_educations = sorted(_educations, key=lambda x: x.start_date, reverse=True)

		fields = ["qualification", "start_date", "end_date", "organization", "detail"]
		educations = [dict((f, getattr(edu, f)) for f in fields) for edu in _educations]

		user_requests.append({
			'id': user_request.id,
			'name': '{} {}'.format(mentee_account.user.first_name, mentee_account.user.last_name),
			'username': mentee_account.user.username,
			'sop': mrm.sop,
			'expectations': mrm.expectations,
			'commitment': mrm.commitment,
			'educations': educations
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
		# Delete a request only if the request exists
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
		# TODO remove needs_urgent_mentoring
		# needs_urgent_mentoring = json.loads(request.body.decode('utf-8'))['needs_urgent_mentoring']

		user.account.mentee.needs_mentoring = needs_mentoring
		# TODO remove needs_urgent_mentoring
		# user.account.mentee.needs_urgent_mentoring = needs_urgent_mentoring
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
			# TODO remove needs_urgent_mentoring
			# 'needs_urgent_mentoring': user.account.mentee.needs_urgent_mentoring
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
	Message.objects.create(
		sender=request.user.account, 
		receiver=receiver_user.account, 
		content=message['content']
	)

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

	Meeting.objects.create(
		creator=user.account,
		guest=guest.account,
		title=req['title'],
		agenda=req['agenda'],
		time=req['time'],
		meeting_url=req['meeting_url']
	)

	response = {
		'success': True
	}

	email_subject = "Meeting created"
	email_body = f"Meeting details:\n" \
				 f"Creator: {user.username}" \
				 f"Guest:   {guest.username}"
	send_email_custom(to=[user.email, guest.email], subject=email_subject, body=email_body)

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

	send_mail(
		subject='Meeting Summary - {}'.format(req['meeting_date'].strftime('%x')),
		message='Following is the summary of the meeting',
		html_message='''
			<i>This is a system generated mail. Please do not reply to this.</i>

			<br/>
			<table>
				<thead>
					<tr colspan="2">
						<th>
							<center>
								<h2> MEETING DETAILS </h2>
							</center>
						</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<th> DATE </th>
						<td> {} </td>
					</tr>
					<tr>
						<th> DURATION </th>
						<td> {} hours </td>
					</tr>
					<tr>
						<th> DETAILS </th>
						<td> {} </td>
					</tr>
					<tr>
						<th> TODOS </th>
						<td> {} </td>
					</tr>
				</tbody>
			</table>

			<br/><br/>

			<table>
				<thead>
					<tr colspan="2">
						<th>
							<center>
								<h2> NEXT MEETING </h2>
							</center>
						</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<th> TENTATIVE DATE </th>
						<td> {} </td>
					</tr>
					<tr>
						<th> AGENDA </th>
						<td> {} </td>
					</tr>
				</tbody>
			</table>
			<br/>
		'''.format(
			req['meeting_date'],
			req['meeting_length'],
			req['meeting_details'],
			req['meeting_todos'],
			req['next_meeting_date'],
			req['next_meeting_agenda']
		),
		from_email='mailbotfcs@gmail.com',
		recipient_list=[mentor.account.user.email, mentee.account.user.email]
	)

	MeetingSummary.objects.create(
		mentor=mentor.account.mentor,
		mentee=mentee.account.mentee,
		meeting_date=req['meeting_date'],
		meeting_length=req['meeting_length'],
		meeting_details=req['meeting_details'],
		meeting_todos=req['meeting_todos'],
		next_meeting_date=req['next_meeting_date'],
		next_meeting_agenda=req['next_meeting_agenda']
	)

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


@login_required
def end_relationship(request):
	user = request.user
	other = User.objects.get(username=request.GET.get('username'))

	if user.account.is_mentor == other.account.is_mentor:
		return JsonResponse({'success': False})

	mentor, mentee = other, user
	if user.account.is_mentor:
		mentor, mentee = user, other

	mentor, mentee = mentor.account.mentor, mentee.account.mentee

	MyMentee.objects.filter(mentor=mentor, mentee=mentee).delete()
	MyMentor.objects.filter(mentor=mentor, mentee=mentee).delete()

	DeletedMentorMenteeRelation.objects.create(
		mentor=mentor,
		mentee=mentee,
		end_reason=request.GET.get('end_reason'),
	)

	send_mail(
		subject='Mentor Mentee Relation Ended',
		message='Mentor mentee relationship has been ended. Details are as follows',
		html_message='''
			<i>This is a system generated mail. Please do not reply to this.</i>
			<br/>

			{} ended the mentor-mentee relationship with {}.
			<br/>
			<b>REASON:</b> {}
		'''.format(
			user.username,
			other.username,
			request.GET.get('end_reason')
		),
		from_email='mailbotfcs@gmail.com',
		recipient_list=[user.email, other.email]
	)

	return JsonResponse({'success': True})


@login_required
def get_education(request):
	account = request.user.account
	
	response = {
		'qualifications': [edu.qualification for edu in AccountEducation.objects.filter(account=account)],
		'start_dates': [edu.start_date for edu in AccountEducation.objects.filter(account=account)],
		'end_dates': [edu.end_date for edu in AccountEducation.objects.filter(account=account)],
		'organizations': [edu.organization for edu in AccountEducation.objects.filter(account=account)],
		'details': [edu.detail for edu in AccountEducation.objects.filter(account=account)],
		'success': True
	}

	return JsonResponse(response, safe=False)


@login_required
def add_education(request):
	user = request.user
	
	AccountEducation.objects.create(
		account=user.account,
		qualification = request.GET.get('qualification'),
		start_date = request.GET.get('start_date'),
		end_date = request.GET.get('end_date'),
		organization = request.GET.get('organization'),
		detail = request.GET.get('detail'),
	)
	return JsonResponse({'success' : True})


@login_required
def get_research_experience(request):
	account = request.user.account
	
	response = {
		'positions': [re.position for re in AccountResearchExperience.objects.filter(account=account)],
		'start_dates': [re.start_date for re in AccountResearchExperience.objects.filter(account=account)],
		'end_dates': [re.end_date for re in AccountResearchExperience.objects.filter(account=account)],
		'organizations': [re.organization for re in AccountResearchExperience.objects.filter(account=account)],
		'details': [re.detail for re in AccountResearchExperience.objects.filter(account=account)],
		'success': True
	}
	return JsonResponse(response, safe=False)


@login_required
def add_research_experience(request):
	AccountResearchExperience.objects.create(
		account=request.user.account,
		position=request.GET.get('position'),
		start_date=request.GET.get('start_date'),
		end_date=request.GET.get('end_date'),
		organization=request.GET.get('organization'),
		detail=request.GET.get('detail'),
	)
	return JsonResponse({'success' : True})


def __get_education(account):
	return {
		'edu_qualifications': [edu.qualification for edu in AccountEducation.objects.filter(account=account)],
		'edu_start_dates': [edu.start_date for edu in AccountEducation.objects.filter(account=account)],
		'edu_end_dates': [edu.end_date for edu in AccountEducation.objects.filter(account=account)],
		'edu_organizations': [edu.organization for edu in AccountEducation.objects.filter(account=account)],
		'edu_details': [edu.detail for edu in AccountEducation.objects.filter(account=account)],
	}


def __get_research_experience(account):
	return {
		're_positions': [re.position for re in AccountResearchExperience.objects.filter(account=account)],
		're_start_dates': [re.start_date for re in AccountResearchExperience.objects.filter(account=account)],
		're_end_dates': [re.end_date for re in AccountResearchExperience.objects.filter(account=account)],
		're_organizations': [re.organization for re in AccountResearchExperience.objects.filter(account=account)],
		're_details': [re.detail for re in AccountResearchExperience.objects.filter(account=account)],
	}


def __save_education(account, fields):
	n_records = len(fields['edu_qualifications'])
	
	for i in range(n_records):
		AccountEducation.objects.create(
			account=account,
			qualification = fields['edu_qualifications'][i],
			start_date = fields['edu_start_dates'][i],
			end_date = fields['edu_end_dates'][i],
			organization = fields['edu_organizations'][i],
			detail = fields['edu_details'][i],
		)


def __save_research_experience(account, fields):
	n_records = len(fields['re_positions'])
	
	for i in range(n_records):
		AccountResearchExperience.objects.create(
			account = account,
			position = fields['re_positions'][i],
			start_date = fields['re_start_dates'][i],
			end_date = fields['re_end_dates'][i],
			organization = fields['re_organizations'][i],
			detail = fields['re_details'][i],
		)
		
@login_required
@mentor_required
def get_mentor_profile(request):
	account = request.user.account

	content = {
		'introduction': account.introduction,
		'social_handle': account.social_handle,
		'area': account.mentor.mentorarea.get_area_display(),
		'subarea': account.mentor.mentorarea.subarea,
		'success': True,
	}

	content['area_choices'] = list(map(lambda x: x[1], Areas.choices))
	content.update(__get_education(account))
	content.update(__get_research_experience(account))
	return JsonResponse(content, safe=False)


@login_required
@mentee_required
def get_mentee_profile(request):
	account = request.user.account

	content = {
		'introduction': account.introduction,
		'success': True,
	}

	content.update(__get_education(account))
	content.update(__get_research_experience(account))
	return JsonResponse(content, safe=False)


@login_required
@mentor_required
def save_mentor_profile(request):
	fields = json.loads(request.body)
	
	user = request.user
	user.account.introduction = fields['introduction']
	user.account.social_handle = fields['social_handle']
	user.account.mentor.mentorarea.area = get_area_id(fields['area'])
	user.account.mentor.mentorarea.subarea = fields['subarea']

	user.account.save()
	user.account.mentor.mentorarea.save()
	
	AccountEducation.objects.filter(account=user.account).delete()
	AccountResearchExperience.objects.filter(account=user.account).delete()

	__save_education(user.account, fields)
	__save_research_experience(user.account, fields)
	
	return JsonResponse({'success': True})


@login_required
@mentee_required
def save_mentee_profile(request):
	fields = json.loads(request.body)

	user = request.user
	user.account.introduction = fields['introduction']
	user.account.save()
	
	AccountEducation.objects.filter(account=user.account).delete()
	AccountResearchExperience.objects.filter(account=user.account).delete()

	__save_education(user.account, fields)
	__save_research_experience(user.account, fields)

	return JsonResponse({'success': True})
