from django.urls import path
from . import views


urlpatterns = [
	path("my_mentee/<str:mentee_username>/", views.my_mentee, name="my_mentee"),
	path("my_mentor/<str:mentor_username>/", views.my_mentor, name="my_mentor"),
]
