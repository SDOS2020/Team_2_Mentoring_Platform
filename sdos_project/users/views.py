from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Account, Mentor, Mentee


def register(request):

	return render(request, 'users/register.html')

def register_mentor(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			account = Account(user=user)
			
			# Register as a mentor
			account.is_mentor = True
			account.save()

			mentor = Mentor(account=account)
			mentor.save()

			username = form.cleaned_data.get('username')
			messages.success(request, f'Mentor account Created for {username}!')
			return redirect('register')
	else:
		form = UserRegisterForm()
	
	context = {
		'form' : form
	}

	return render(request, 'users/register_mentor.html', context)

def register_mentee(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			
			user = form.save()
			account = Account(user=user)
			
			# Register as a mentee
			account.is_mentee = True
			account.save()

			mentee = Mentee(account=account)
			mentee.save()
			
			username = form.cleaned_data.get('username')
			messages.success(request, f'Mentee account Created for {username}!')
			return redirect('register')
	else:
		form = UserRegisterForm()

	context = {
		'form' : form,
	}

	return render(request, 'users/register_mentee.html', context)
