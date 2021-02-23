from django.urls import path
from . import views as api_views


urlpatterns = [
	path("search_users/", api_views.search_users, name="search_users"),

	path("get_user_requests/", api_views.get_user_requests, name="get_user_requests"),
	path("accept_mentorship_request/", api_views.accept_mentorship_request, name="accept_mentorship_request"),
	path("cancel_mentorship_request/", api_views.cancel_mentorship_request, name="cancel_mentorship_request"),
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
	
	path("get_education/", api_views.get_education, name="get_education"),
	path("add_education/", api_views.add_education, name="add_education"),

	path("get_research_experience/", api_views.get_research_experience, name="get_research_experience"),
	path("add_research_experience/", api_views.add_research_experience, name="add_research_experience"),

	path("update_settings/", api_views.update_settings, name="update_settings"),
	
	path("end_relationship/", api_views.end_relationship, name="end_relationship"),

	# My Mentor-Mentee specific page
	path("get_messages/<str:chatter_username>/", api_views.get_messages, name="get_messages"),
	path("send_message/", api_views.send_message, name="send_message"),

	path("get_meetings/<str:guest_name>", api_views.get_meetings, name="get_meetings"),
	path("add_meeting/", api_views.add_meeting, name="add_meeting"),
	path("edit_meeting/", api_views.edit_meeting, name="edit_meeting"),

	path("has_pending_requests/", api_views.has_pending_requests, name="has_pending_requests"),

	path("get_meeting_summaries/<str:guest_name>", api_views.get_meeting_summaries, name="get_meeting_summaries"),
	path("add_meeting_summary/", api_views.add_meeting_summary, name="add_meeting_summary"),
	
	path("get_milestones/", api_views.get_milestones, name="get_milestones"),
	path("add_milestone/", api_views.add_milestone, name="add_milestone"),

	# Edit profile
	path("save_mentor_profile/", api_views.save_mentor_profile, name="save_mentor_profile"),
	path("get_mentor_profile/", api_views.get_mentor_profile, name="get_mentor_profile"),

	path("save_mentee_profile/", api_views.save_mentee_profile, name="save_mentee_profile"),
	path("get_mentee_profile/", api_views.get_mentee_profile, name="get_mentee_profile"),
]
