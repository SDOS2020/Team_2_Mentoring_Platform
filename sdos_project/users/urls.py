from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
	# When user is logged out
	path("login/", auth_views.LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True), name="login"),
	path("register_mentor/", user_views.register_mentor, name="register_mentor"),
	path("register_mentee/", user_views.register_mentee, name="register_mentee"),

	# When user is logged in
	path("logout/", auth_views.LogoutView.as_view(template_name="home/homepage.html"), name="logout"),
	path("profile/<str:username>", user_views.profile, name="profile"),
	path("search_users/", user_views.search_users, name="search_users"),
	path("chat_user/", user_views.chat_user, name="chat"),
  path("my_requests/", user_views.my_requests, name="my_requests"),
]
