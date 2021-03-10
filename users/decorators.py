from functools import wraps
from django.contrib.auth.decorators import login_required as login_required_inbuilt
from django.contrib import messages
from django.shortcuts import redirect


def mentor_required(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		user = args[0].user
		if not user.account.is_mentor:
			return redirect("homepage")

		return view_func(*args, **kwargs)

	return wrapper


def mentee_required(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		user = args[0].user
		if not user.account.is_mentee:
			return redirect("homepage")

		return view_func(*args, **kwargs)

	return wrapper


def login_required(view_func):
	@wraps(view_func)
	@login_required_inbuilt
	def wrapper(*args, **kwargs):
		account = args[0].user.account
		if account.is_mentor and (not account.mentor.verified):
			messages.error(args[0], "Please wait for verification")
			return redirect("homepage")

		return view_func(*args, **kwargs)

	return wrapper