from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
	path('register/', user_views.register, name='register'),
	path('profile/', user_views.profile, name='profile'),
	path('register_mentor/', user_views.register_mentor, name='register_mentor'),
	path('register_mentee/', user_views.register_mentee, name='register_mentee'),
	path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

