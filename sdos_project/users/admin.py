from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Account)
admin.site.register(Mentor)
admin.site.register(Mentee)
admin.site.register(MyMentee)
admin.site.register(MyMentor)
admin.site.register(MenteeSentRequest)
admin.site.register(MentorRoleField)
admin.site.register(MenteeRoleField)
admin.site.register(MentorExpectedRoleField)
admin.site.register(MenteeExpectedRoleField)
admin.site.register(Message)
admin.site.register(Meeting)
admin.site.register(MentorArea)
admin.site.register(MentorshipRequestMessage)
admin.site.register(MeetingSummary)
admin.site.register(Milestone)
admin.site.register(DeletedMentorMenteeRelation)
admin.site.register(AccountEducation)
