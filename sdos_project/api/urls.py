from django.urls import path
from . import views as api_views


urlpatterns = [
	path("search_users/", api_views.search_users, name="search_users"),

	path("get_user_requests/", api_views.get_user_requests, name="get_user_requests"),
	path("accept_mentorship_request/", api_views.accept_mentorship_request, name="accept_mentorship_request"),
	path("reject_mentorship_request/", api_views.reject_mentorship_request, name="reject_mentorship_request"),
	path("send_mentorship_request/", api_views.send_mentorship_request, name="send_mentorship_request"),

	path("get_mentors/", api_views.get_mentors, name="get_mentors"),
	path("get_mentees/", api_views.get_mentees, name="get_mentees"),
	path("get_chatters/", api_views.get_chatters, name="get_chatters"),
	path("get_recommendations/", api_views.get_recommendations, name="get_recommendations"),

	path("get_mentor_roles/", api_views.get_mentor_roles, name="get_mentor_roles"),
	path("get_mentor_fields/", api_views.get_mentor_fields, name="get_mentor_fields"),
	path("get_mentor_areas/", api_views.get_mentor_areas, name="get_mentor_areas"),

	path("get_settings/", api_views.get_settings, name="get_settings"),
	path("update_settings/", api_views.update_settings, name="update_settings"),

	# My Mentor-Mentee specific page
	path("get_messages/<str:chatter_username>/", api_views.get_messages, name="get_messages"),
	path("send_message/", api_views.send_message, name="send_message"),

	path("get_meetings/<str:guest_name>", api_views.get_meetings, name="get_meetings"),
	path("add_meeting/", api_views.add_meeting, name="add_meeting"),

	path("get_meeting_summaries/<str:guest_name>", api_views.get_meeting_summaries, name="get_meeting_summaries"),
	path("add_meeting_summary/", api_views.add_meeting_summary, name="add_meeting_summary"),
]
