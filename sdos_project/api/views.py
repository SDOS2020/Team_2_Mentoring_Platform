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
	MY_MENTEE = 3
	MY_MENTOR = 4

	for account in Account.objects.all():
		status = NOT_ALLOWED
		if account.is_mentor != user.account.is_mentor:
			if user.account.is_mentor:
				# current user is a mentor, other user is a mentee
				if MyMentee.objects.filter(mentor=user.account.mentor, mentee=account.mentee).exists():
					status = MY_MENTEE
				elif MentorSentRequest.objects.filter(mentor=user.account.mentor, mentee=account.mentee).exists():
					status = PENDING_REQUEST
				else:
					status = REQUEST_MENTORSHIP
			else:
				# current user is a mentee, other user is a mentor
				if MyMentor.objects.filter(mentor=account.mentor, mentee=user.account.mentee).exists():
					status = MY_MENTOR
				elif MenteeSentRequest.objects.filter(mentor=account.mentor, mentee=user.account.mentee).exists():
					status = PENDING_REQUEST
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


@login_required
def send_mentorship_request(request):
	user = request.user
	requestee = request.GET.get('requestee')
	requestee = User.objects.get(username=requestee)

	if user.account.is_mentor:
		MentorSentRequest.objects.create(mentor=user.account.mentor, mentee=requestee.account.mentee)
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


@login_required
def accept_request(request):
	user = request.user
	requestor = request.GET.get('requestor')
	requestor = User.objects.get(username=requestor)
	print('Got requestor:', requestor)
	if user.account.is_mentor:
		# user is a mentor
		# requestor is a mentee
		MyMentee.objects.create(mentor=user.account.mentor, mentee=requestor.account.mentee)
		MyMentor.objects.create(mentor=user.account.mentor, mentee=requestor.account.mentee)
		MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).delete()
	else:
		# user is a mentee
		# requestor is a mentor
		MyMentor.objects.create(mentee=user.account.mentee, mentor=requestor.account.mentor)
		MyMentee.objects.create(mentee=user.account.mentee, mentor=requestor.account.mentor)
		MentorSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestor.account.mentor).delete()
	
	return JsonResponse({"success": True}, safe=False)

@login_required
def reject_request(request):
	user = request.user
	requestor = request.GET.get('requestor')
	requestor = User.objects.get(username=requestor)
	print('Got requestor:', requestor)
	if user.account.is_mentor:
		# user is a mentor
		# requestor is a mentee
		MenteeSentRequest.objects.filter(mentor=user.account.mentor, mentee=requestor.account.mentee).delete()
	else:
		# user is a mentee
		# requestor is a mentor
		MentorSentRequest.objects.filter(mentee=user.account.mentee, mentor=requestor.account.mentor).delete()
	
	return JsonResponse({"success": True}, safe=False)
	
