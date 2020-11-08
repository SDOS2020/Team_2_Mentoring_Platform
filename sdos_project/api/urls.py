from django.urls import path
from . import views as api_views


urlpatterns = [
	path("search_users/", api_views.search_users, name="search_users"),
	path("get_user_requests/", api_views.get_user_requests, name="get_user_requests"),
	path("accept_request/", api_views.accept_request, name="accept_request"),
	path("reject_request/", api_views.reject_request, name="reject_request"),
]
