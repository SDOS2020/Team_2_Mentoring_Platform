from functools import wraps
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
