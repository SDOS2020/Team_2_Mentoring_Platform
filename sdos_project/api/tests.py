import logging
from django.test import TestCase


class MenteeTestcase(TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		logging.disable(logging.CRITICAL)
		# signals.post_save.disconnect(receiver=)


	@classmethod
	def tearDownClass(cls) -> None:
		return super().tearDownClass()


	def test_mentee_accesses_mentor_tags(self):
		self.assertEqual(1, 1)
