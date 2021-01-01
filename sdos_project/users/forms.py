from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Areas, Gender, Fields, User, MentorRoles, MenteeRoles, Account, MentorArea


class MentorRegistrationForm(UserCreationForm):
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
		choices=Gender.choices,
		initial=Gender.choices[-1],
		required=True
	)

	age = forms.IntegerField(
		min_value=16,
		max_value=100,
		required=True
	)

	field = forms.ChoiceField(
		choices=Fields.choices,
		initial=Fields.choices[-1],
		required=True
	)

	role = forms.ChoiceField(
		choices=MentorRoles.choices,
		initial=MentorRoles.choices[-1],
		required=True
	)

	area = forms.ChoiceField(
		choices=Areas.choices,
		initial=Areas.choices[-1],
		required=True
	)

	subarea = forms.CharField(
		max_length=64,
		required=False,
		initial=''
	)

	social_handle = forms.URLField(
		required=False,
		help_text="Link to your personal website/LinkedIn profile"
	)

	class Meta:
		# model that will be affected is the user model, i.e. at form.save(), it will update the User model
		model = User
		# fields needed in form in this order
		fields = (
			"first_name",
			"last_name",
			"gender",
			"age",
			"username",
			"email",
			"role",
			"field",
			"area",
			"subarea",
			"social_handle",
			"password1",
			"password2"
		)


class MenteeRegistrationForm(UserCreationForm):
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
		choices=Gender.choices,
		initial=Gender.choices[-1],
		required=True
	)

	age = forms.IntegerField(
		min_value=16,
		max_value=100,
		required=True
	)

	field = forms.ChoiceField(
		choices=Fields.choices,
		initial=Fields.choices[-1],
		required=True
	)

	role = forms.ChoiceField(
		choices=MenteeRoles.choices,
		initial=MenteeRoles.choices[-1],
		required=True
	)

	class Meta:
		# model that will be affected is the user model, i.e. at form.save(), it will update the User model
		model = User
		# fields needed in form in this order
		fields = (
			"first_name",
			"last_name",
			"gender",
			"age",
			"username",
			"email",
			"role",
			"field",
			"password1",
			"password2"
		)



class EditNameForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ("first_name", "last_name")


class EditMentorDetailsForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ("introduction", "education", "research_experience", "social_handle")

class EditMenteeDetailsForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ("introduction", "education", "research_experience")

class EditAreasForm(forms.ModelForm):
	class Meta:
		model = MentorArea
		fields = ("area", "subarea")
