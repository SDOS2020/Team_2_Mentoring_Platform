from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, EditDetailsForm, EditNameForm
from .models import Account, Mentor, Mentee
from django.contrib.auth.decorators import login_required
from users.models import User, Roles, Fields
from .decorators import mentee_required


def register_mentor(request):
	if request.user.is_authenticated:
		return redirect("homepage")

	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			account = Account(user=user)

			# Register as a mentor
			account.is_mentor = True
			account.save()

			mentor = Mentor(account=account)
			mentor.save()

			return redirect("login")
	else:
		form = UserRegisterForm()

	context = {
		"form" : form
	}

	return render(request, "users/register_mentor.html", context)


def register_mentee(request):
	if request.user.is_authenticated:
		return redirect("homepage")

	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():

			user = form.save()
			account = Account(user=user)

			# Register as a mentee
			account.is_mentee = True
			account.save()

			mentee = Mentee(account=account)
			mentee.save()

			return redirect("login")
	else:
		form = UserRegisterForm()

	context = {
		"form" : form,
	}

	return render(request, "users/register_mentee.html", context)


@login_required
def profile(request, username):
	requested_user = User.objects.get(username=username)
	return render(request, "users/dist/profile.html", {"requested_user": requested_user})


@login_required
def search_users(request):
	return render(request, "users/search_users.html")


@login_required
def chat_user(request):
	return render(request, "users/chats.html")


@login_required
def my_requests(request):
	return render(request, "users/my_requests.html")


@login_required
def my_mentors(request):
	return render(request, "users/my_mentors.html")


@login_required
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

	initial_dict_name_form = {
		"first_name": request.user.first_name,
		"last_name": request.user.last_name,
	}

	initial_dict_details_form = {
		"introduction": request.user.account.introduction,
		"education": request.user.account.education,
		"experience": request.user.account.experience
	}

	if request.method == "POST":

		details_form = EditDetailsForm(request.POST or None, initial = initial_dict_details_form)

		if details_form.is_valid():
			user = request.user
			user.account.introduction = details_form.cleaned_data["introduction"]
			user.account.education = details_form.cleaned_data["education"]
			user.account.experience = details_form.cleaned_data["experience"]

			user.save()
			user.account.save()
			return redirect("homepage")

	else:
		details_form = EditDetailsForm(request.POST or None, initial = initial_dict_details_form)

	context = {
		"details_form": details_form
	}

	return render(request, "users/edit_profile.html", context)
