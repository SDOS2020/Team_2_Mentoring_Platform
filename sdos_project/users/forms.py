from django import forms
from .models import User, Mentor, Mentee, Account
from django.contrib.auth.forms import UserCreationForm
from django.core import validators



class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	first_name = forms.CharField(
		max_length=50,
		required=True,
	)

	last_name = forms.CharField(
		max_length=50,
		required=True,
	)

	class Meta:
		# model that will be affected is the user model, i.e. at form.save(), it will update the User model
		model = User
		# fields needed in form in this order
		fields = ("first_name", "last_name", "username", "email", "password1", "password2")


class MentorRegisterForm(forms.ModelForm):
	class Meta:
		model = Mentor
		fields = "__all__"


class MenteeRegisterForm(forms.ModelForm):
	class Meta:
		model = Mentee
		fields = "__all__"


class EditNameForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ("first_name", "last_name")


class EditDetailsForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ("introduction", "education", "experience")
		# fields = '__all__'

	# first_name = forms.CharField(
	# 	max_length=50,
	# 	required=True,
	# )

	# last_name = forms.CharField(
	# 	max_length=50,
	# 	required=True,
	# )

	# introduction = forms.CharField(
	# 	widget=forms.Textarea,
	# 	max_length=512,
	# 	required=True,
	# )

	# education = forms.CharField(
	# 	widget=forms.Textarea,
	# 	max_length=512,
	# 	required=True,
	# )

	# experience = forms.CharField(
	# 	widget=forms.Textarea,
	# 	max_length=512,
	# 	required=True,
	# )

