from django.http import JsonResponse
from users.models import (
	User,
	Account, 
	Mentor, 
	Mentee, 
	MenteeSentRequest, 
	MentorSentRequest, 
	MyMentee, 
	MyMentor)

from django.contrib.auth.decorators import login_required

# TODO: Filters
@login_required
def search_users(request):
	user = request.user
	pattern = request.GET.get('pattern')
	print(Mentor.objects.all())
	print(Mentee.objects.all())
	
	shortlist = []

	# Status codes
	NOT_ALLOWED = 0
	REQUEST_MENTORSHIP = 1
	PENDING_REQUEST = 2
	REQUEST_RECEIVED = 3
	MY_MENTEE = 4
	MY_MENTOR = 5

	for account in Account.objects.all():
		status = NOT_ALLOWED
		if account.is_mentor != user.account.is_mentor:
			if user.account.is_mentor:
				# current user is a mentor, other user is a mentee
				if MyMentee.objects.filter(mentor=user.account.mentor, mentee=account.mentee).exists():
					status = MY_MENTEE
				elif MentorSentRequest.objects.filter(mentor=user.account.mentor, mentee=account.mentee).exists():
					status = PENDING_REQUEST
				elif MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=account.mentee).exists():
					status = REQUEST_RECEIVED
				else:
					status = REQUEST_MENTORSHIP
			else:
				# current user is a mentee, other user is a mentor
				if MyMentor.objects.filter(mentor=account.mentor, mentee=user.account.mentee).exists():
					status = MY_MENTOR
				elif MenteeSentRequest.objects.filter(mentor=account.mentor, mentee=user.account.mentee).exists():
					status = PENDING_REQUEST
				elif MentorSentRequest.objects.filter(mentor=account.mentor, mentee=user.account.mentee).exists():
					status = REQUEST_RECEIVED
				else:
					status = REQUEST_MENTORSHIP

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
@login_required
def send_mentorship_request(request):
	user = request.user
	requestee = request.GET.get('requestee')
	requestee = User.objects.get(username=requestee)

	if user.account.is_mentor == requestee.account.is_mentor:
		# Checks if the user and the requestee are of the same type
		# You should only be able to send request to different types of users
		return JsonResponse({"success" : False}, safe=False)

	if user.account.is_mentor:
		# user is a mentor
		# requestee is a mentee
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
			MentorSentRequest.objects.create(mentor=user.account.mentor, mentee=requestee.account.mentee)
	else:
		# user is a mentee
		# requestee is a mentor
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
			MenteeSentRequest.objects.create(mentee=user.account.mentee, mentor=requestee.account.mentor)
	
	return JsonResponse({"success" : True})


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


# TODO : 1. avoid duplicate requests, 
# TODO : 2. check if the request already exists
# TODO : 3. check if the user and the requestor are of different type (mentor / mentee)
@login_required
def accept_request(request):
	user = request.user
	requestor = request.GET.get('requestor')
	requestor = User.objects.get(username=requestor)
	print('Got requestor:', requestor)

	if user.account.is_mentor == requestor.account.is_mentor:
		# checks if the type of the users is the same
		# same type users can not be in a mentor / mentee relationship
		return JsonResponse({"success" : False}, safe=False)

	if user.account.is_mentor:
		# user is a mentor
		# requestor is a mentee

		if MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).exists():
			# executes only if, requestor is not already a mentee of the user and it is the requestor that sent the 
			# mentorship request to the user
			MyMentee.objects.create(mentor=user.account.mentor, mentee=requestor.account.mentee)
			MyMentor.objects.create(mentor=user.account.mentor, mentee=requestor.account.mentee)
			MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).delete()
	else:
		# user is a mentee
		# requestor is a mentor
		if MentorSentRequest.objects.filter(mentor=requestor.account.mentor, mentee=user.account.mentee).exists():
			# executes if mentor is not already the mentor of the mentee
			# and if mentor actually sent a mentorship request to the mentee
			MyMentor.objects.create(mentee=user.account.mentee, mentor=requestor.account.mentor)
			MyMentee.objects.create(mentee=user.account.mentee, mentor=requestor.account.mentor)
			MentorSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestor.account.mentor).delete()
	
	return JsonResponse({"success": True}, safe=False)


# TODO : 1. avoid duplicate requests, 
# TODO : 2. check if the request already exists
# TODO : 3. check if the user and the requestor are of different type (mentor / mentee)
@login_required
def reject_request(request):
	user = request.user
	requestor = request.GET.get('requestor')
	requestor = User.objects.get(username=requestor)
	print('Got requestor:', requestor)

	if user.account.is_mentor == requestor.account.is_mentor:
		# checks if the user and the requestor are of different type
		# same type users cannot reject mentorship request
		return JsonResponse({"success" : False}, safe=False)

	if user.account.is_mentor:
		# user is a mentor
		# requestor is a mentee
		if MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).exists():
			# delete a request only if the request exists
			MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).delete()
	else:
		# user is a mentee
		# requestor is a mentor
		if MentorSentRequest.objects.filter(mentor=requestor.account.mentor, mentee=user.account.mentee).exists():
			# delete a request only if the request exists
			MentorSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestor.account.mentor).delete()
	
	return JsonResponse({"success": True}, safe=False)
	
