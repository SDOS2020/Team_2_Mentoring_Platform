from django.contrib import admin
from .models import User, Admin, Account, Mentor, Mentee
# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Account)
admin.site.register(Mentor)
admin.site.register(Mentee)