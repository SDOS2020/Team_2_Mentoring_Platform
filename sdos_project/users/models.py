from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser


# Top most - for authentication purpose only
class User(AbstractUser):
	is_admin = models.BooleanField(default=False)


class Admin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)


class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	age = models.IntegerField(
		null=True, 
		validators=[
			validators.MinValueValidator(16),
			validators.MaxValueValidator(100),
		]
	)


	MALE = 'M'
	FEMALE = 'F'
	PREFER_NOT_TO_SAY = '-'

	GENDER_CHOICES = [
		(MALE, 'Male'),
		(FEMALE, 'Female'),
		(PREFER_NOT_TO_SAY, 'Prefer not to say'),
	]

	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=PREFER_NOT_TO_SAY)


	STUDENT = 'S'
	FACULTY = 'F'

	DESIGNATION_CHOICES = [
		(STUDENT, 'Student'),
		(FACULTY, 'Faculty'),
	]

	designation = models.CharField(max_length=1, choices=DESIGNATION_CHOICES, null=True)


	mobile = models.CharField(
		max_length=10,
		null=True,
		validators=[
			validators.MinLengthValidator(10),
		]
	)


	introduction = models.TextField(max_length=512, null=True)
	education = models.TextField(max_length=512, null=True)
	experience = models.TextField(max_length=512, null=True)
	expertise = models.TextField(max_length=512, null=True)
	social_handles = models.TextField(max_length=512, null=True)
	
	rating = models.DecimalField(
		null=True,
		max_digits=3,
		decimal_places=1, 
		validators=[
			validators.MinValueValidator(0.0),
			validators.MaxValueValidator(5.0),
		]
	)

	
	is_mentor = models.BooleanField(default=False)
	is_mentee = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username


class Mentor(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	mentorship_duration = models.IntegerField(
		default=6,
		help_text='In months',
		validators=[
			validators.MinValueValidator(1),
			validators.MaxValueValidator(24),
		]
	)

	mentee_types = models.TextField(max_length=512, null=True)
	mentee_group_size = models.IntegerField(
		default=1,
		validators=[
			validators.MinValueValidator(1),
		]
	)

	is_open_to_mentorship = models.BooleanField(default=True)

	def __str__(self):
		return self.account.user.username


class Mentee(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	needs_mentoring = models.BooleanField(default=True)
	needs_urgent_mentoring = models.BooleanField(default=False)
	topics = models.TextField(max_length=512, null=True)

	def __str__(self):
		return self.account.user.username


class MyMentee(models.Model):
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentor.account.user.username + ' -> ' + self.mentee.account.user.username


"""
	For performance gains
"""
class MyMentor(models.Model):
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentee.account.user.username + ' -> ' + self.mentor.account.user.username


"""
	For a mentor to view menteeship requests
"""
class PendingMenteeshipRequest(models.Model):
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentor.account.user.username + ' -> ' + self.mentee.account.user.username


"""
	For a mentee to view mentorship requests
"""
class PendingMentorshipRequest(models.Model):
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentee.account.user.username + ' -> ' + self.mentor.account.user.username

