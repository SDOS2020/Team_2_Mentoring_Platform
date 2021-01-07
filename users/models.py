from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractUser):
	"""
	Top most - for authentication purpose only
	"""
	is_admin = models.BooleanField(default=False)


class Admin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)


class Gender(models.IntegerChoices):
	male 				= 1, _('Male')
	female 				= 2, _('Female')
	prefer_not_to_say 	= 3, _('Prefer not to say')


class Account(models.Model):
	"""
	The main class that stores all the common information for a mentor and a mentee
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	age = models.IntegerField(
		null=True, 
		validators=[
			validators.MinValueValidator(16),
			validators.MaxValueValidator(100),
		]
	)

	gender = models.IntegerField(choices=Gender.choices, default=Gender.choices[-1])

	mobile = models.CharField(
		max_length=10,
		null=True,
		validators=[
			validators.MinLengthValidator(10),
		]
	)

	introduction = models.TextField(max_length=512, null=True)
	# education = models.TextField(max_length=512, null=True)
	# research_experience = models.TextField(max_length=512, null=True)
	expertise = models.TextField(max_length=512, null=True)
	social_handle = models.URLField(null=True, help_text="Link to your personal website/LinkedIn profile")
	
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


class AccountEducation(models.Model):
	"""
	Stores the education fields of accounts
	"""
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	qualification = models.CharField(max_length=128)
	start_date = models.DateField()
	end_date = models.DateField()
	organization = models.CharField(max_length=128)
	detail = models.TextField(max_length=512, null=True)

	def __str__(self):
		return self.account.user.username


class AccountResearchExperience(models.Model):
	"""
	Stores the research experience of accounts
	"""
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	position = models.CharField(max_length=128)
	start_date = models.DateField()
	end_date = models.DateField()
	organization = models.CharField(max_length=128)
	detail = models.TextField(max_length=512, null=True)

	def __str__(self):
		return self.account.user.username


class Mentor(models.Model):
	"""
	The mentor class, stores attributes specific to a mentor
	"""
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	mentorship_duration = models.IntegerField(
		default=6,
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
	
	will_mentor_faculty = models.BooleanField(default=False)
	will_mentor_phd = models.BooleanField(default=False)
	will_mentor_mtech = models.BooleanField(default=False)
	will_mentor_btech = models.BooleanField(default=False)

	
	# Responsibilities
	responsibility1 = models.BooleanField(default=False)
	responsibility2 = models.BooleanField(default=False)
	responsibility3 = models.BooleanField(default=False)
	responsibility4 = models.BooleanField(default=False)
	responsibility5 = models.BooleanField(default=False)
	responsibility6 = models.BooleanField(default=False)
	responsibility7 = models.BooleanField(default=False)
	responsibility8 = models.BooleanField(default=False)
	other_responsibility = models.TextField(null=True, max_length=512)

	def __str__(self):
		return self.account.user.username


class Mentee(models.Model):
	"""
	The mentee class, stores attributes specific to a mentee
	"""
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	needs_mentoring = models.BooleanField(default=True)
	needs_urgent_mentoring = models.BooleanField(default=False)
	topics = models.TextField(max_length=512, null=True)

	def __str__(self):
		return self.account.user.username


class MyMentee(models.Model):
	"""
	Stores the mentees assigned to a mentor, you can get the mentees assigned to a mentor by 
	querying, MyMentee.objects.filter(mentor='current-mentor')
	"""
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentor.account.user.username + ' -> ' + self.mentee.account.user.username


class MyMentor(models.Model):
	"""
	For performance gains
	Stores the mentors assigned to a mentee, you can get the mentors assigned to a mentee by 
	querying, MyMentor.objects.filter(mentee='current-mentee')
	"""
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

	def __str__(self):
		return self.mentee.account.user.username + ' -> ' + self.mentor.account.user.username


class MenteeSentRequest(models.Model):
	"""
	For a mentee to view mentorship requests
	"""
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
	"""
	The different fields of users that can exist
	"""
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
	mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
	role = models.IntegerField(choices=MentorRoles.choices, null=True)
	field = models.IntegerField(choices=Fields.choices, null=True)

	def __str__(self):
		return "{} -> {} -> {}".format(self.mentor.account.user.username, self.get_role_display(), self.get_field_display())


class MenteeRoleField(models.Model):
	"""
	Stores the mentees qualifications, their role (current / past), their fields (current / past)
	"""
	mentee = models.OneToOneField(Mentee, on_delete=models.CASCADE)
	role = models.IntegerField(choices=MenteeRoles.choices, null=True)
	field = models.IntegerField(choices=Fields.choices, null=True)

	def __str__(self):
		return "{} -> {} -> {}".format(self.mentee.account.user.username, self.get_role_display(), self.get_field_display())


class MentorExpectedRoleField(models.Model):
	"""
	Stores what the mentors expect from mentees in terms of their
	qualifications, their role (current / past), their fields(current / past)
	"""
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	role = models.IntegerField(choices=MentorRoles.choices, null=True)
	field = models.IntegerField(choices=Fields.choices, null=True)

	def __str__(self):
		return self.mentor.account.user.username + ' -> ' + self.get_role_display() + ' -> ' + self.get_field_display()


class MenteeExpectedRoleField(models.Model):
	"""
	Stores what the mentees expect from mentors in terms of their
	qualifications, their role (current / past), their fields (current / past)

	NOTE: this might be deleted later on...
	"""
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	role = models.IntegerField(choices=MenteeRoles.choices, null=True)
	field = models.IntegerField(choices=Fields.choices, null=True)

	def __str__(self):
		return self.mentee.account.user.username + ' -> ' + self.get_role_display() + ' -> ' + self.get_field_display()


class Message(models.Model):
	"""
	Table to store the chat messages among users.
	"""
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


class MentorResponsibility(models.IntegerChoices):
	"""
	Reference: Mail/Github Issue
	"""
	responsibility1 = 1, _('Listen to research proposals/initial research and give suggestions for improvement')
	responsibility2 = 2, _('Read papers written (the final version which the author wants to submit) and give inputs')
	responsibility3 = 3, _('Guide in literature reading')
	responsibility4 = 4, _('Help in understanding difficult concepts, discussing some papers/results')
	responsibility5 = 5, _('Guidance on where to submit a research paper')
	responsibility6 = 6, _('Guidance on the proper conduct of research and literature review')
	responsibility7 = 7, _('Review and comment on the resume')
	responsibility8 = 8, _('Guide on postdoc and other research job possibilities')


class Areas(models.IntegerChoices):
	'''
	Reference: http://csrankings.org/
	'''
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


class MentorshipRequestMessage(models.Model):
	"""
	Store the SOP, commitment, expectations of the mentee which is sent to the mentor at the time of requesting for
	mentorship
	"""

	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	sop = models.TextField(max_length=512, null=True)
	expectations = models.TextField(max_length=256, null=True)
	commitment = models.TextField(max_length=256, null=True)

	def __str__(self):
		return "{} sent a request to {}".format(
			self.mentee.account.user.username, self.mentor.account.user.username)


class MeetingSummary(models.Model):
	"""
	Store:
	1. Meeting date
	2. Meeting length (in hours)
	3. Meeting agenda
	4. Meeting todos (action items)
	5. Next meeting date (tentative)
	6. Next meeting agenda
	"""

	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)

	meeting_date = models.DateTimeField(auto_now_add=False)
	meeting_length = models.IntegerField()
	meeting_details = models.TextField(max_length=512)
	meeting_todos = models.TextField(max_length=512, null=True)

	next_meeting_date = models.DateTimeField(auto_now_add=False)
	next_meeting_agenda = models.TextField(max_length=512)

	def __str__(self):
		return "Meeting held at {} of length {} hours".format(
			self.meeting_date, self.meeting_length)


class Milestone(models.Model):
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	content = models.TextField(max_length=512)

	def __str__(self):
		return f'Mentor: {self.mentor}, Mentee: {self.mentee}'


class DeletedMentorMenteeRelation(models.Model):
	mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
	mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
	end_reason = models.TextField(max_length=512)
	date_ended = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'[ENDED] Mentor: {self.mentor}, Mentee: {self.mentee}'
