from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as user_views


urlpatterns = [
	# When user is logged out
	path("login/", auth_views.LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True), name="login"),
	path("register_mentor/", user_views.register_mentor, name="register_mentor"),
	path("register_mentee/", user_views.register_mentee, name="register_mentee"),
	path("change_password/", user_views.change_password, name="change_password"),
	path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

	# When user is logged in
	path("logout/", auth_views.LogoutView.as_view(template_name="home/homepage.html"), name="logout"),
	path("profile/<str:username>/", user_views.profile, name="profile"),
	path("edit_profile/", user_views.edit_profile, name="edit_profile"),
	path("search_users/", user_views.search_users, name="search_users"),
	path("chat_user/", user_views.chat_user, name="chat"),
	path("my_requests/", user_views.my_requests, name="my_requests"),
	path("my_mentors/", user_views.my_mentors, name="my_mentors"),
	path("my_mentees/", user_views.my_mentees, name="my_mentees"),
	path("my_recommendations/", user_views.my_recommendations, name="my_recommendations"),
	path("settings/", user_views.settings, name="settings"),
]
