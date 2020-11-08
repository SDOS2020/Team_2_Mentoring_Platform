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
	pattern = request.GET.get('pattern')
	print(Mentor.objects.all())
	print(Mentee.objects.all())
	
	shortlist = []

	for account in Account.objects.all():
		if pattern.lower() in account.user.username.lower():
			shortlist.append({
				'id': account.id,
				'name': account.user.username,
				'is_mentor': account.is_mentor
			})

	return JsonResponse(shortlist, safe=False)


@login_required
def get_user_requests(request):
	current_user = request.user
	print(current_user)

	user_requests = []
	
	if current_user.account.is_mentor:
		for user_request in MenteeSentRequest.objects.filter(mentor=current_user.account.mentor):
			user_requests.append({
				'id': user_request.id,
				'username': user_request.mentee.account.user.username
			})
	else:
		for user_request in MentorSentRequest.objects.filter(mentor=current_user.account.mentor):
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
	
