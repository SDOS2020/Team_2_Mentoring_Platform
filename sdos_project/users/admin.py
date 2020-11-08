from django.contrib import admin
from .models import (
	User, 
	Admin, 
	Account, 
	Mentor, 
	Mentee, 
	MyMentee, 
	MyMentor, 
	MenteeSentRequest, 
	MentorSentRequest
)


# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Account)
admin.site.register(Mentor)
admin.site.register(Mentee)
admin.site.register(MyMentee)
admin.site.register(MyMentor)
admin.site.register(MenteeSentRequest)
admin.site.register(MentorSentRequest)
