from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from users.models import *
from .decorators import mentee_required, mentor_required
from .models import Account, AccountEducation, Mentor, Mentee, MentorRoleField, MenteeRoleField
from .forms import *

def register_mentor(request):
	if request.user.is_authenticated:
		return redirect("homepage")

	if request.method == "POST":
		form = MentorRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			account = Account(
				user=user,
				gender=form.cleaned_data['gender'],
				age=form.cleaned_data['age'],
				social_handle=form.cleaned_data['social_handle'],
				is_mentor=True
			)

			account.save()

			mentor = Mentor(account=account)
			mentor.save()

			mentor_role_field = MentorRoleField(
				mentor=mentor,
				role=form.cleaned_data['role'],
				field=form.cleaned_data['field']
			)
			mentor_role_field.save()

			mentor_area = MentorArea(
				mentor=mentor,
				area=form.cleaned_data['area'],
				subarea=form.cleaned_data['subarea']
			)
			mentor_area.save()

			# return render(request, "users/login.html")
			return redirect("login")
	else:
		form = MentorRegistrationForm()

	context = {
		"form" : form,
	}

	return render(request, "users/register_mentor.html", context)


def register_mentee(request):
	if request.user.is_authenticated:
		return redirect("homepage")

	if request.method == "POST":
		form = MenteeRegistrationForm(request.POST)
		if form.is_valid():

			user = form.save()
			account = Account(
				user=user,
				gender=form.cleaned_data['gender'],
				age=form.cleaned_data['age'],
				is_mentee=True
			)

			account.save()

			mentee = Mentee(account=account)
			mentee.save()

			mentee_role_field = MenteeRoleField(
				mentee=mentee,
				role=form.cleaned_data['role'],
				field=form.cleaned_data['field']
			)
			mentee_role_field.save()

			return redirect("login")
	else:
		form = MenteeRegistrationForm()

	context = {
		"form" : form,
	}

	return render(request, "users/register_mentee.html", context)


@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)

		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('homepage')

		else:
			messages.error(request, 'Please correct the error below.')

	else:
		form = PasswordChangeForm(request.user)

	return render(request, 'users/change_password.html', {'form': form})

def get_responsibilities(mentor):
	responsibilities = []
	s = 'responsibility'
	for i, j in MentorResponsibility.choices:
		if getattr(mentor, s + str(i)):
			responsibilities.append(j)
	return responsibilities

@login_required
def profile(request, username):
	requested_user = User.objects.get(username=username)
	
	educations = AccountEducation.objects.filter(account=requested_user.account).all()
	educations = sorted(educations, key=lambda x: x.start_date, reverse=True)
	
	experiences = AccountResearchExperience.objects.filter(account=requested_user.account).all()[::-1]
	experiences = sorted(experiences, key=lambda x: x.start_date, reverse=True)
	
	if (request.user == requested_user) or (requested_user.account.is_mentor):
		responsibilities = []
		if requested_user.account.is_mentor:
			responsibilities = get_responsibilities(requested_user.account.mentor)
		return render(request, "users/dist/profile.html", {"requested_user": requested_user, "responsibilities": responsibilities, "educations": educations, "experiences": experiences})

	return redirect("homepage")


@login_required
@mentee_required
def search_users(request):
	return render(request, "users/search_users.html")


@login_required
def chat_user(request):
	return render(request, "users/chats.html")


@login_required
@mentor_required
def my_requests(request):
	return render(request, "users/my_requests.html")


@login_required
@mentee_required
def my_mentors(request):
	return render(request, "users/my_mentors.html")


@login_required
@mentor_required
def my_mentees(request):
	return render(request, "users/my_mentees.html")


@login_required
def settings(request):
	return render(request, "users/settings.html")


@login_required
@mentee_required
def my_recommendations(request):
	return render(request, "users/my_recommendations.html")


@login_required
def edit_profile(request):
	if request.user.account.is_mentor:
		return render(request, "users/edit_mentor_profile.html")

	return render(request, "users/edit_mentee_profile.html")
