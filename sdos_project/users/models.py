from django.db import models
from django.contrib.auth.models import AbstractUser


# Top most - for authentication purpose only
class User(AbstractUser):
	is_admin = models.BooleanField(default=False)


class Admin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)


class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	age = models.IntegerField(null=True)

	is_mentor = models.BooleanField(default=False)
	is_mentee = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username


class Mentor(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	mentorship_duration = models.IntegerField(null=True)

	def __str__(self):
		return self.account.user.username


class Mentee(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	needs_mentoring = models.BooleanField(default=True)

	def __str__(self):
		return self.account.user.username
