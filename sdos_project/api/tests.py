import logging
from django.test import TestCase
from users.models import *
from .data_testing import *
import json


class RegistrationTestCases(TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		logging.disable(logging.CRITICAL)
		# signals.post_save.disconnect(receiver=)


	@classmethod
	def tearDownClass(cls) -> None:
		return super().tearDownClass()


	def test_single_mentor_valid(self):
		response = self.client.post('/users/register_mentor/', data=VALID1)
		self.assertEqual(response.status_code, 302)


	def test_single_mentee_valid(self):
		response = self.client.post('/users/register_mentee/', data=VALID1)
		self.assertEqual(response.status_code, 302)


	def test_single_mentor_invalid_username(self):
		response = self.client.post('/users/register_mentor/', data=INVALID_USERNAME)
		self.assertEqual(response.status_code, 200)


	def test_single_mentee_invalid_username(self):
		response = self.client.post('/users/register_mentee/', data=INVALID_USERNAME)
		self.assertEqual(response.status_code, 200)


	def test_single_mentor_passwords_not_same(self):
		response = self.client.post('/users/register_mentor/', data=PASSWORDS_NOT_SAME)
		self.assertEqual(response.status_code, 200)


	def test_single_mentee_passwords_not_same(self):
		response = self.client.post('/users/register_mentee/', data=PASSWORDS_NOT_SAME)
		self.assertEqual(response.status_code, 200)


	def test_single_mentor_invalid_password(self):
		response = self.client.post('/users/register_mentor/', data=INVALID_PASSWORD)
		self.assertEqual(response.status_code, 200)


	def test_single_mentee_invalid_password(self):
		response = self.client.post('/users/register_mentee/', data=INVALID_PASSWORD)
		self.assertEqual(response.status_code, 200)


	def test_single_mentor_invalid_email(self):
		response = self.client.post('/users/register_mentor/', data=INVALID_EMAIL)
		self.assertEqual(response.status_code, 200)


	def test_single_mentee_invalid_email(self):
		response = self.client.post('/users/register_mentee/', data=INVALID_EMAIL)
		self.assertEqual(response.status_code, 200)


	def test_multiple_create_mentors_valid(self):
		response = self.client.post('/users/register_mentor/', data=VALID1)
		response = self.client.post('/users/register_mentor/', data=VALID2)
		self.assertEqual(response.status_code, 302)


	def test_multiple_create_mentees_valid(self):
		response = self.client.post('/users/register_mentee/', data=VALID1)
		response = self.client.post('/users/register_mentee/', data=VALID2)
		self.assertEqual(response.status_code, 302)


	def test_multiple_mentors_with_non_unique_username(self):
		response = self.client.post('/users/register_mentor/', data=VALID1)
		response = self.client.post('/users/register_mentor/', data=VALID1)
		self.assertEqual(response.status_code, 200)


	def test_multiple_mentees_with_non_unique_username(self):
		response = self.client.post('/users/register_mentee/', data=VALID1)
		response = self.client.post('/users/register_mentee/', data=VALID1)
		self.assertEqual(response.status_code, 200)


class LoginTestCases(TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		logging.disable(logging.CRITICAL)
		# signals.post_save.disconnect(receiver=)


	@classmethod
	def tearDownClass(cls) -> None:
		return super().tearDownClass()


	def test_basic_login(self):
		self.client.post('/users/register_mentee/', data=VALID1)
		data = {
			'username': 'ananya',
			'password': 'pass4321'
		}

		response = self.client.post('/users/login/', data=data)
		self.assertEqual(response.status_code, 302)


	def test_basic_login_wrong_password(self):
		self.client.post('/users/register_mentee/', data=VALID1)
		data = {
			'username': 'ananya',
			'password': 'pass'
		}

		response = self.client.post('/users/login/', data=data)
		self.assertEqual(response.status_code, 200)


	def test_basic_login_incorrect_username(self):
		self.client.post('/users/register_mentee/', data=VALID1)
		data = {
			'username': 'ananyaaaaaaa',
			'password': 'pass4321'
		}

		response = self.client.post('/users/login/', data=data)
		self.assertEqual(response.status_code, 200)


	def test_accessing_settings_while_logged_in(self):
		self.client.post('/users/register_mentee/', data=VALID1)
		data = {
			'username': 'ananya',
			'password': 'pass4321'
		}

		response = self.client.post('/users/login/', data=data)
		response = self.client.get('/users/settings/')
		self.assertEqual(response.status_code, 200)


	def test_accessing_settings_while_logged_out(self):
		response = self.client.get('/users/settings/')
		self.assertEqual(response.status_code, 302)


	def test_accessing_chats_while_logged_in(self):
		self.client.post('/users/register_mentee/', data=VALID1)
		data = {
			'username': 'ananya',
			'password': 'pass4321'
		}

		response = self.client.post('/users/login/', data=data)
		response = self.client.get('/users/chat_user/')
		self.assertEqual(response.status_code, 200)


	def test_accessing_chats_while_logged_out(self):
		response = self.client.get('/users/chat_user/')
		self.assertEqual(response.status_code, 302)


	def test_edit_profile_while_logged_in(self):
		self.client.post('/users/register_mentee/', data=VALID1)
		data = {
			'username': 'ananya',
			'password': 'pass4321'
		}

		response = self.client.post('/users/login/', data=data)
		response = self.client.get('/users/edit_profile/')
		self.assertEqual(response.status_code, 200)


	def test_edit_profile_while_logged_out(self):
		response = self.client.get('/users/edit_profile/')
		self.assertEqual(response.status_code, 302)


	def test_view_profile_while_logged_in(self):
		self.client.post('/users/register_mentee/', data=VALID1)
		data = {
			'username': 'ananya',
			'password': 'pass4321'
		}

		response = self.client.post('/users/login/', data=data)
		response = self.client.get('/users/profile/ananya/')
		self.assertEqual(response.status_code, 200)


	def test_view_profile_while_logged_in_invalid_user(self):
		self.client.post('/users/register_mentee/', data=VALID1)
		data = {
			'username': 'ananya',
			'password': 'pass4321'
		}

		response = self.client.post('/users/login/', data=data)
		try:	
			response = self.client.get('/users/profile/helle/')
		except Exception as e:
			s = 'User matching query does not exist.'
			self.assertTrue(s in str(e))

	def test_view_profile_while_logged_out(self):
		response = self.client.get('/users/profile/ananya/')
		self.assertEqual(response.status_code, 302)


class IntegrationTestCases(TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		logging.disable(logging.CRITICAL)
		# signals.post_save.disconnect(receiver=)


	@classmethod
	def tearDownClass(cls) -> None:
		return super().tearDownClass()


	def create_user(self, data, role):
		if role == 'MENTOR':	
			self.client.post('/users/register_mentor/', data=data)
		else:
			self.client.post('/users/register_mentee/', data=data)


	def login_user(self, username, password):
		data = {
			'username': username,
			'password': password
		}
		self.client.post('/users/login/', data=data)


	def test_integration_1(self):
		'''
		Create a mentor and a mentee
		Mentee sends request to mentor
		Mentor accepts
		Check if mentee in mentor's list of mentees
		Mentor sends message to mentee
		Check if message in mentee's chats with mentor
		'''
		self.create_user(VALID1, role='MENTEE')
		self.create_user(VALID2, role='MENTOR')

		self.login_user('ananya', 'pass4321')
		data = {
			'requestee': 'karan',
			'sop': 'Sir please please please',
			'expectations': 'CGPA > 2',
			'commitment': '0 years',
		}
		response = self.client.get('/api/send_mentorship_request/', data)
		self.assertEqual(response.status_code, 200)
		self.client.post('/users/logout/')
		
		self.login_user('karan', 'pass4321')
		response = self.client.post('/api/accept_mentorship_request/?requestor=ananya')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/api/get_mentees/')
		mentees = json.loads(response.content.decode())['mentees']
		mentee_names = [mentee['username'] for mentee in mentees]
		self.assertTrue('ananya' in mentee_names)

		message = 'Hi beta. How are you?'
		data = {
			'message': {
				'content': message,
				'receiver': 'ananya',
			}
		}
		response = self.client.post(f'/api/send_message/', json.dumps(data), content_type='application/json')
		self.client.post('/users/logout/')

		self.login_user('ananya', 'pass4321')
		response = self.client.get('/api/get_messages/karan/')
		messages = json.loads(response.content.decode())['messages']
		message_contents = [msg['content'] for msg in messages]
		self.assertTrue(message in message_contents)


	def test_integration_2(self):
		'''
		Create a mentor
		Login
		Edit your profile
		Check that DB has been updated
		Update settings
		Check that DB has been updated
		Logout
		Try to update settings again
		Mus be redirected to login page
		'''

		self.create_user(VALID2, role='MENTOR')
		self.login_user('karan', 'pass4321')

		response = self.client.post('/users/edit_profile/', data=EDIT_PROFILE_FORM)
		user = User.objects.get(username='karan')

		self.assertEqual(EDIT_PROFILE_FORM['area'], user.account.mentor.mentorarea.area)
		self.assertEqual(EDIT_PROFILE_FORM['subarea'], user.account.mentor.mentorarea.subarea)
		self.assertEqual(EDIT_PROFILE_FORM['introduction'], user.account.introduction)
		self.assertEqual(EDIT_PROFILE_FORM['education'], user.account.education)
		self.assertEqual(EDIT_PROFILE_FORM['research_experience'], user.account.research_experience)

		self.client.post('/api/update_settings/', json.dumps(UPDATE_SETTINGS_FORM), content_type='application/json')

		# Now fetch settings
		response = self.client.get('/api/get_settings/')
		settings = json.loads(response.content.decode())
		self.assertEqual(UPDATE_SETTINGS_FORM['mentorship_duration'], settings['mentorship_duration'])
		self.assertEqual(UPDATE_SETTINGS_FORM['is_open_to_mentorship'], settings['is_open_to_mentorship'])

		self.client.post('/users/logout/')

		response = self.client.get('/api/get_settings/')
		self.assertEqual(response.status_code, 302)
