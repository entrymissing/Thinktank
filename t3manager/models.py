from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

class UserProfile(models.Model):  
	user = models.OneToOneField(User)  

	def __str__(self):
		return "%s's profile" % self.user

	def getProfile(self):
		userProfile = get_object_or_404(Profile, username=self.user.username)
		return userProfile

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  
 
User.profile = property(lambda u: u.userprofile.getProfile() )
post_save.connect(create_user_profile, sender=User)

class Profile(models.Model):
    post_date = models.DateTimeField('date subscribed')
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    degrees = models.CharField(max_length=500)
    email = models.CharField(max_length=200)
    experience_functions = models.TextField()
    interest_functions = models.TextField()
    experience = models.TextField()
    experience_areas = models.TextField()
    interest_areas = models.TextField()
    interest_problems = models.TextField()
    interest_thinktank = models.TextField()
    experience_thinktank = models.TextField()
    time_commitment = models.CharField(max_length=200)
    comments = models.TextField(blank=True)
    imageLink = models.URLField(max_length=400)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Project(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	contactName = models.CharField(max_length=200)
	status = models.CharField(max_length=200)
	recruiting = models.CharField(max_length=200)
	contactEmail = models.EmailField()
	projectLeads = models.ManyToManyField(Profile, related_name='project_leader')
	teamMembers = models.ManyToManyField(Profile, related_name='project_teamMembers', blank=True)
	candidates = models.ManyToManyField(Profile, related_name='project_candidates', blank=True)
	description_file = models.FileField(upload_to='/var/www/Thinktank/mediafiles/', blank=True)
	
	def getDescriptionFileName(self):
		print 'asdf'
		return 'USPS.pdf'
	
	def __unicode__(self):
		return self.title
		
