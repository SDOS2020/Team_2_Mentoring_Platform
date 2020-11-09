from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Account, Mentor, Mentee
from django.contrib.auth.decorators import login_required
from users.models import User


def register_mentor(request):
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

			username = form.cleaned_data.get("username")
			messages.success(request, f"Mentor account created for {username}!")
			return redirect("login")
	else:
		form = UserRegisterForm()
	
	context = {
		"form" : form
	}

	return render(request, "users/register_mentor.html", context)


def register_mentee(request):
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

			username = form.cleaned_data.get("username")
			messages.success(request, f"Mentee account created for {username}!")
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
	return render(request, "users/dist/profile.html", {'requested_user': requested_user})


@login_required
def search_users(request):
	return render(request, "users/search_users.html")


@login_required
def chat_user(request):
	return render(request, "users/chats.html")
