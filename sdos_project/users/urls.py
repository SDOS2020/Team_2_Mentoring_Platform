from django.urls import path
from . import views

urlpatterns = [
	path('register/', views.register, name='register'),
	path('register/mentor/', views.register_mentor, name='register_mentor'),
	path('register/mentee/', views.register_mentee, name='register_mentee'),
]

