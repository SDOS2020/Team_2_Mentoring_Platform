from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from users.models import User
from .decorators import mentee_required, mentor_required
from .models import Account, Mentor, Mentee, MentorRoleField, MenteeRoleField
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


@login_required
def profile(request, username):
	requested_user = User.objects.get(username=username)
	return render(request, "users/dist/profile.html", {"requested_user": requested_user})


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


def edit_mentor_profile(request):
	"""
	Edit mentor profile
	"""
	user = request.user

	initial_areas = {
		"area": user.account.mentor.mentorarea.area,
		"subarea": user.account.mentor.mentorarea.subarea
	}

	initial_details = {
		"introduction": user.account.introduction,
		"education": user.account.education,
		"research_experience": user.account.research_experience,
		"social_handle": user.account.social_handle
	}

	areas_form, details_form = None, None

	if request.method == "POST":
		areas_form = EditAreasForm(request.POST)
		details_form = EditMentorDetailsForm(request.POST)

		if details_form.is_valid() and areas_form.is_valid():
			user.account.mentor.mentorarea.area = areas_form.cleaned_data["area"]
			user.account.mentor.mentorarea.subarea = areas_form.cleaned_data["subarea"]

			user.account.introduction = details_form.cleaned_data["introduction"]
			user.account.education = details_form.cleaned_data["education"]
			user.account.research_experience = details_form.cleaned_data["research_experience"]
			user.account.social_handle = details_form.cleaned_data["social_handle"]
			
			user.account.mentor.mentorarea.save()
			user.account.save()
			return redirect("homepage")

	elif request.method == "GET":
		areas_form = EditAreasForm(initial=initial_areas)
		details_form = EditMentorDetailsForm(initial=initial_details)

	context = {
		"details_form": details_form,
		"areas_form" : areas_form
	}

	return render(request, "users/edit_profile.html", context)


def edit_mentee_profile(request):
	"""
	Edit mentee profile
	"""
	user = request.user

	initial_details = {
		"introduction": user.account.introduction,
		"education": user.account.education,
		"research_experience": user.account.research_experience,
	}

	details_form = None

	if request.method == "POST":
		details_form = EditMenteeDetailsForm(request.POST)

		if details_form.is_valid():
			user.account.introduction = details_form.cleaned_data["introduction"]
			user.account.education = details_form.cleaned_data["education"]
			user.account.research_experience = details_form.cleaned_data["research_experience"]
			
			user.account.save()
			return redirect("homepage")

	elif request.method == "GET":
		details_form = EditMenteeDetailsForm(initial=initial_details)

	context = {
		"details_form": details_form
	}

	return render(request, "users/edit_profile.html", context)


@login_required
def edit_profile(request):
	if request.user.account.is_mentor:
		return edit_mentor_profile(request)
	else:
		return edit_mentee_profile(request)
