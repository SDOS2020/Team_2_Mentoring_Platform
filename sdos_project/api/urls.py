from django.urls import path
from . import views as api_views


urlpatterns = [
	path("search_users/", api_views.search_users, name="search_users"),
	path("get_user_requests/", api_views.get_user_requests, name="get_user_requests"),
	path("accept_request/", api_views.accept_request, name="accept_request"),
	path("reject_request/", api_views.reject_request, name="reject_request"),
	path("send_request/", api_views.send_request, name="send_request"),
	path("get_mentors/", api_views.get_mentors, name="get_mentors"),
	path("get_mentees/", api_views.get_mentees, name="get_mentees"),
	path("get_recommendations/", api_views.get_recommendations, name="get_recommendations"),
	path("get_tags/", api_views.get_tags, name="get_tags"),
	path("get_my_tags/", api_views.get_my_tags, name="get_my_tags"),
	path("update_my_tags/", api_views.update_my_tags, name="update_my_tags"),
	path("get_settings/", api_views.get_settings, name="get_settings"),
	path("update_settings/", api_views.update_settings, name="update_settings"),
]
