from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
				is_mentor = True
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


@login_required
def edit_profile(request):
	initial_areas = None
	if request.user.account.is_mentor:
		initial_areas = {
			"area": request.user.account.mentor.mentorarea.area,
			"subarea": request.user.account.mentor.mentorarea.subarea
		}

	initial_details = {
		"introduction": request.user.account.introduction,
		"education": request.user.account.education,
		"research_experience": request.user.account.research_experience
	}

	areas_form, details_form = None, None

	if request.method == "POST":
		if request.user.account.is_mentor:
			areas_form = EditAreasForm(request.POST)
	
		details_form = EditDetailsForm(request.POST)

		if details_form.is_valid():
			user = request.user
			
			if request.user.account.is_mentor and areas_form.is_valid():
				user.account.mentor.mentorarea.area = areas_form.cleaned_data["area"]
				user.account.mentor.mentorarea.subarea = areas_form.cleaned_data["subarea"]
				user.account.mentor.mentorarea.save()

			user.account.introduction = details_form.cleaned_data["introduction"]
			user.account.education = details_form.cleaned_data["education"]
			user.account.research_experience = details_form.cleaned_data["research_experience"]
			user.account.save()
			print('Saved')
			return redirect("homepage")

	elif request.method == "GET":
		if request.user.account.is_mentor:
			areas_form = EditAreasForm(initial=initial_areas)
			
		details_form = EditDetailsForm(initial=initial_details)

	context = {
		"details_form": details_form
	}

	if request.user.account.is_mentor:
		context["areas_form"] = areas_form

	return render(request, "users/edit_profile.html", context)
