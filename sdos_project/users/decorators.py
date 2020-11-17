from users.models import User, Account, Mentor, Mentee
from django.shortcuts import redirect, render

from functools import wraps

def mentor_required(view_func):

	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0]
		user = request.user

		if not user.account.is_mentor:
			return redirect("homepage")
		
		return view_func(*args, **kwargs)
	
	return wrapper


def mentee_required(view_func):

	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0]
		user = request.user

		if not user.account.is_mentee:
			print("Hello There ol friend")
			return redirect("homepage")
		
		return view_func(*args, **kwargs)
	
	return wrapper