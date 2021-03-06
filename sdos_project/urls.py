from django.contrib import admin
from django.urls import path, include


urlpatterns = [
	path("", include("home.urls")),
	path("admin/", admin.site.urls),
	path("api/", include("api.urls")),
	path("users/", include("users.urls")),
	path("mentor_mentee/", include("mentor_mentee.urls")),
]
