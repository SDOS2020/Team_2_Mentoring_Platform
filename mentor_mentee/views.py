from django.shortcuts import render, redirect
from users.decorators import login_required
from users.models import MyMentor, MyMentee
from users.decorators import mentor_required, mentee_required


@login_required
@mentee_required
def my_mentor(request, mentor_username):
	user = request.user
	my_mentors = MyMentor.objects.filter(mentee=user.account.mentee).all()

	my_mentor = None
	for mentor in my_mentors:
		if mentor.mentor.account.user.username == mentor_username:
			my_mentor = mentor
			break

	if not my_mentor:
		return redirect("homepage")

	context = {
		"mentor": mentor_username
	}
	
	return render(request, "mentor_mentee/my_mentor.html", context)
	

@login_required
@mentor_required
def my_mentee(request, mentee_username):
	user = request.user
	my_mentees = MyMentee.objects.filter(mentor=user.account.mentor).all()

	my_mentee = None
	for mentee in my_mentees:
		if mentee.mentee.account.user.username == mentee_username:
			my_mentee = mentee
			break

	if not my_mentee:
		return redirect("homepage")

	context = {
		"mentee": mentee_username
	}

	return render(request, "mentor_mentee/my_mentee.html", context)
