from django.contrib import admin
from t3manager.models import Profile, Project
from django.contrib.auth.models import User
    
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('username', 'last_name', 'first_name', 'email')

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'contactName', 'contactEmail')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)