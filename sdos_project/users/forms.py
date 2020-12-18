from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Mentor, Mentee, Account, MentorArea


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

	gender = forms.ChoiceField(
		choices=Account.GENDER_CHOICES,
		initial=Account.GENDER_CHOICES[-1],
		required=True
	)

	class Meta:
		# model that will be affected is the user model, i.e. at form.save(), it will update the User model
		model = User
		# fields needed in form in this order
		fields = ("first_name", "last_name", "gender", "username", "email", "password1", "password2")


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


class EditAreasForm(forms.ModelForm):
	class Meta:
		model = MentorArea
		fields = ("area", "subarea")
