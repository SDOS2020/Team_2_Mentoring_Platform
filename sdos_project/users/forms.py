from django import forms
from .models import User, Mentor, Mentee
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		# model that will be affected is the user model, i.e. at form.save(), it will update the User model
		model = User
		# fields needed in form in this order
		fields = ('username', 'email', 'password1', 'password2')


class MentorRegisterForm(forms.ModelForm):

	class Meta:
		model = Mentor
		fields = []

class MenteeRegisterForm(forms.ModelForm):

	class Meta:
		model = Mentee
		fields = []
		