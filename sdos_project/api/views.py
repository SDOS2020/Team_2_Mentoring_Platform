from django.http import JsonResponse
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
)

from django.contrib.auth.decorators import login_required
import json

def filter_mentor(mentor, filters):

	for f in filters:
		role = f['Role']
		field = f['Field']

		if role != 'null':
			role = next(filter(lambda x: x[-1] == role, Roles.choices))[0]
		if field != 'null':
			field = next(filter(lambda x: x[-1] == field, Fields.choices))[0]

		if role == 'null' and field == 'null':
			return True
		elif role == 'null':
			# Definitely field exists
			if MentorRoleField.objects.filter(mentor=mentor, field=field).exists():
				return True
		elif field == 'null':
			# Definitely role exists
			if MentorRoleField.objects.filter(mentor=mentor, role=role).exists():
				return True
		else:
			# Both role and field exist
			if MentorRoleField.objects.filter(mentor=mentor, role=role, field=field).exists():
				return True
	
	return False

def filter_mentee(mentee, filters):

	for f in filters:
		role = f['Role']
		field = f['Field']

		if role != 'null':
			role = next(filter(lambda x: x[-1] == role, Roles.choices))[0]
		if field != 'null':
			field = next(filter(lambda x: x[-1] == field, Fields.choices))[0]

		if role == 'null' and field == 'null':
			return True
		elif role == 'null':
			# Definitely field exists
			if MenteeRoleField.objects.filter(mentee=mentee, field=field).exists():
				return True
		elif field == 'null':
			# Definitely role exists
			if MenteeRoleField.objects.filter(mentee=mentee, role=role).exists():
				return True
		else:
			# Both role and field exist
			if MenteeRoleField.objects.filter(mentee=mentee, role=role, field=field).exists():
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
