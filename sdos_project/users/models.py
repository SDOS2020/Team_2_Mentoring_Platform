from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Top most - for authentication purpose only
class User(AbstractUser):
	is_admin = models.BooleanField(default=False)


class Admin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)


class Gender(models.IntegerChoices):
	male 				= 1, _('Male')
	female 				= 2, _('Female')
	prefer_not_to_say 	= 3, _('Prefer not to say')


"""
The main class that stores all the common information for a mentor and a mentee
"""
class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	age = models.IntegerField(
		null=True, 
		validators=[
			validators.MinValueValidator(16),
			validators.MaxValueValidator(100),
		]
	)

	gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.choices[-1])

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


"""
	The mentor class, stores attributes specific to a mentor
"""
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

	mentee_group_size = models.IntegerField(
		default=1,
		validators=[
			validators.MinValueValidator(1),
		]
	)

	is_open_to_mentorship = models.BooleanField(default=True)

	def __str__(self):
		return self.account.user.username


"""
	The mentee class, stores attributes specific to a mentee
"""
class Mentee(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	needs_mentoring = models.BooleanField(default=True)
	needs_urgent_mentoring = models.BooleanField(default=False)
	topics = models.TextField(max_length=512, null=True)

	def __str__(self):
		return self.account.user.username


"""
	Stores the mentees assigned to a mentor, you can get the mentees assigned to a mentor by 
	querying, MyMentee.objects.filter(mentor='current-mentor')
"""
class MyMentee(models.Model):
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentor.account.user.username + ' -> ' + self.mentee.account.user.username


"""
	For performance gains
	Stores the mentors assigned to a mentee, you can get the mentors assigned to a mentee by 
	querying, MyMentor.objects.filter(mentee='current-mentee')
"""
class MyMentor(models.Model):
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentee.account.user.username + ' -> ' + self.mentor.account.user.username


"""
	For a mentor to view menteeship requests
"""
class MentorSentRequest(models.Model):
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentor.account.user.username + ' -> ' + self.mentee.account.user.username


"""
	For a mentee to view mentorship requests
"""
class MenteeSentRequest(models.Model):
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentee.account.user.username + ' -> ' + self.mentor.account.user.username


class MenteeRoles(models.IntegerChoices):
	"""
	The different type of users that can exist. These types are accessed in the 
	types of mentee a mentor needs, and also the types of mentor a mentee needs.
	"""
	faculty       = 1, _('Faculty')
	developer     = 2, _('Developer')
	undergraduate = 3, _('BTech')
	graduate      = 4, _('MTech')
	post_graduate = 5, _('PhD')


class MentorRoles(models.IntegerChoices):
	faculty   = 1, _('Faculty')
	developer = 2, _('Developer')


class Fields(models.IntegerChoices):
	"""The different fields of users that can exist"""
	computer_science                             = 1, _('CSE')
	electronics_and_communication                = 2, _('ECE')
	computer_science_and_design                  = 3, _('CSD')
	computer_science_and_mathematics             = 4, _('CSAM')
	computer_science_and_social_sciences         = 5, _('CSSS')
	computer_science_and_artificial_intelligence = 6, _('CSAI')


class MentorRoleField(models.Model):
	"""
	Stores the mentors qualifications, their role (current / past), their fields(current / past)
	"""
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	role = models.IntegerField(choices=MentorRoles.choices, null=True)
	field = models.IntegerField(choices=Fields.choices, null=True)

	def __str__(self):
		return "{} -> {} -> {}".format(self.mentor.account.user.username, self.get_role_display(), self.get_field_display())


"""
	Stores the mentees qualifications, their role (current / past), their fields (current / past)
"""
class MenteeRoleField(models.Model):
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	role = models.IntegerField(choices=MenteeRoles.choices, null=True)
	field = models.IntegerField(choices=Fields.choices, null=True)

	def __str__(self):
		return "{} -> {} -> {}".format(self.mentee.account.user.username, self.get_role_display(), self.get_field_display())


"""
	Stores what the mentors expect from mentees in terms of their
	qualifications, their role (current / past), their fields(current / past)
"""
class MentorExpectedRoleField(models.Model):
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	role = models.IntegerField(choices=MentorRoles.choices, null=True)
	field = models.IntegerField(choices=Fields.choices, null=True)

	def __str__(self):
		return self.mentor.account.user.username + ' -> ' + self.get_role_display() + ' -> ' + self.get_field_display()


"""
	Stores what the mentees expect from mentors in terms of their
	qualifications, their role (current / past), their fields (current / past)

	NOTE: this might be deleted later on...
"""
class MenteeExpectedRoleField(models.Model):
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	role = models.IntegerField(choices=MenteeRoles.choices, null=True)
	field = models.IntegerField(choices=Fields.choices, null=True)

	def __str__(self):
		return self.mentee.account.user.username + ' -> ' + self.get_role_display() + ' -> ' + self.get_field_display()


"""
	Table to store the chat messages among users.
"""
class Message(models.Model):
	sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='message_sender')
	receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='message_receiver')
	content = models.TextField(max_length=512, null=True)
	time_posted = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.user.username + ' messaged ' + self.receiver.user.username


class Meeting(models.Model):
	creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='meeting_creator')
	guest = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='meeting_guest')
	title = models.CharField(max_length=64, default="Untitled Meeting")
	agenda = models.CharField(max_length=128, default="")
	time = models.DateTimeField(auto_now_add=False)
	meeting_url = models.CharField(max_length=128, default="https://www.meet.google.com")

	def __str__(self):
		return self.creator.user.username + ' created a meeting with ' + self.guest.user.username


'''
Reference: http://csrankings.org/
'''
class Areas(models.IntegerChoices):
	algorithms_and_complexity            =  1, _('Algorithms and Complexity')
	artificial_intelligence              =  2, _('Artificial Intelligence')
	computational_bio_and_bioinformatics =  3, _('Computational Bio and Bioinformatics')
	computer_architecture                =  4, _('Computer Architecture')
	computer_graphics                    =  5, _('Computer Graphics')
	computer_networks                    =  6, _('Computer Networks')
	computer_security                    =  7, _('Computer Security')
	computer_vision                      =  8, _('Computer Vision')
	cryptography                         =  9, _('Cryptography')
	databases                            = 10, _('Databases')
	design_automation                    = 11, _('Design Automation')
	economics_and_computation            = 12, _('Economics and Computation')
	embedded_and_real_time_systems       = 13, _('Embedded and Real-Time Systems')
	high_performance_computing           = 14, _('High-Performance Computing')
	human_computer_interaction           = 15, _('Human-Computer Interaction')
	logic_and_verification               = 16, _('Logic and Verification')
	machine_learning_and_data_mining     = 17, _('Machine Learning and Data Mining')
	measurement_and_performance_analysis = 18, _('Measurement and Performance Analysis')
	mobile_computing                     = 19, _('Mobile Computing')
	natural_language_processing          = 20, _('Natural Language Processing')
	operating_systems                    = 21, _('Operating Systems')
	programming_languages                = 22, _('Programming Languages')
	robotics                             = 23, _('Robotics')
	software_engineering                 = 24, _('Software Engineering')
	the_web_and_information_retrieval    = 25, _('The Web and Information Retrieval')
	visualization                        = 26, _('Visualization')


class MentorArea(models.Model):
	mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
	area = models.IntegerField(choices=Areas.choices, null=True)
	subarea = models.CharField(max_length=64, null=True)

	def __str__(self):
		return "{} of area {}".format(self.mentor.account.user.username, self.get_area_display())
