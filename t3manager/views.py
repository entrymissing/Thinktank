from django.shortcuts import render
from models import Profile, Project, UserProfile
from django.http import HttpResponse, HttpResponseRedirect
import csv
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from django.forms import ModelForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from random import choice
from os.path import basename

class ProfileForm(ModelForm):
    class Meta:
        model = Profile

class editMember(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'editform.html'
    
    def get_success_url(obj):
        return '/filterMembers'

class ProjectForm(ModelForm):
    class Meta:
        model = Project

class editProject(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'editform.html'
    
    def get_success_url(obj):
        return '/showProjects'

@login_required
def filterMembers(request):
	res_Members = Profile.objects.all().order_by('-first_name')
	if 'email' in request.GET:
		res_Members = res_Members.filter(email__contains=request.GET['email'])
		res_Members = res_Members.filter(position__contains=request.GET['position'])
		res_Members = res_Members.filter(time_commitment__contains=request.GET['time_commitment'])
		res_Members = res_Members.filter(Q(first_name__contains=request.GET['name']) | Q(last_name__contains=request.GET['name']))
		res_Members = res_Members.filter(Q(experience_thinktank__contains=request.GET['experience']) | Q(experience_areas__contains=request.GET['experience']) | Q(experience_functions__contains=request.GET['experience']) | Q(experience__contains=request.GET['experience']))
		res_Members = res_Members.filter(Q(interest_functions__contains=request.GET['intests']) | Q(interest_areas__contains=request.GET['intests']) | Q(interest_problems__contains=request.GET['intests']) | Q(interest_thinktank__contains=request.GET['intests']))
		
	context = {'members': res_Members}
	return render(request, 'filterMembers.html', context)

@login_required
def showProjectOverview(request):
	res_Projects = Project.objects.all()
	context = {'projects': res_Projects}
	return render(request, 'showProjects.html', context)

@login_required
def viewProject(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	isAdmin = project.projectLeads.filter(username = request.user.profile.username)
	project.fname = basename(project.description_file.name)
	return render(request, 'viewProject.html', {'project': project, 'isAdmin': isAdmin})

@login_required
def updateMembers(request, project_id, profile_id, command):
	#make sure the user is actually an admin for the project
	project = get_object_or_404(Project, pk=project_id)
	if len(project.projectLeads.filter(username = request.user.profile.username)) > 0:
		if command == 'addCandidate':
			newCandidate = get_object_or_404(Profile, pk=profile_id)
			project.candidates.add(newCandidate)
			project.save()
			
		if command == 'removeCandidate':
			newCandidate = get_object_or_404(Profile, pk=profile_id)
			project.candidates.remove(newCandidate)
			project.save()

		if command == 'addMember':
			newCandidate = get_object_or_404(Profile, pk=profile_id)
			project.teamMembers.add(newCandidate)
			project.save()
			
		if command == 'removeMember':
			newCandidate = get_object_or_404(Profile, pk=profile_id)
			project.teamMembers.remove(newCandidate)
			project.save()

		if command == 'promoteToMember':
			newCandidate = get_object_or_404(Profile, pk=profile_id)
			project.candidates.remove(newCandidate)
			project.teamMembers.add(newCandidate)
			project.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def viewMember(request, member_id):
	memberProfile = get_object_or_404(Profile, pk=member_id)
	leaderOfProjects = Project.objects.filter(projectLeads = memberProfile)
	memberOfProjects = Project.objects.filter(teamMembers = memberProfile)
	userLedProjects = Project.objects.filter(projectLeads = request.user.profile)
	return render(request, 'viewMember.html', {'member': memberProfile, 'userLedProjects':userLedProjects, 'leaderOfProjects':leaderOfProjects, 'memberOfProjects':memberOfProjects})

@login_required
def editProfile(request):
    profile = get_object_or_404(User, pk=request.user.id).profile
    return render(request, 'editProfile.html', {'profile': profile})

@login_required
def updateProfile(request):
	profile = get_object_or_404(Profile, username=request.POST['username'])
	profile.email = request.POST['email']
	profile.imageLink = request.POST['imageurl']	
	profile.first_name = request.POST['first_name']
	profile.last_name = request.POST['last_name']
	profile.position = request.POST['position']
	profile.department = request.POST['department']
	profile.degrees = request.POST['degrees']
	profile.experience_functions = request.POST['experience_functions']
	profile.interest_functions = request.POST['interest_functions']
	profile.experience = request.POST['experience']
	profile.experience_areas = request.POST['experience_areas']
	profile.interest_areas = request.POST['interest_areas']
	profile.interest_problems = request.POST['interest_problems']
	profile.interest_thinktank = request.POST['interest_thinktank']
	profile.experience_thinktank = request.POST['experience_thinktank']
	profile.time_commitment = request.POST['time_commitment']
	profile.comments = request.POST['comments']
	profile.save()
	return redirect('/')

@login_required
def frontpage(request):
	allProjects = Project.objects.all()
	myProjects = Project.objects.filter(Q(teamMembers = request.user.profile) | Q(projectLeads = request.user.profile)).distinct()
	allMembers = Profile.objects.all().order_by('-first_name')
	context = {'projects': allProjects,'myProjects':myProjects, 'members': allMembers}
	return render(request, 'frontpage.html', context)


@login_required
def userDetails(request, user_id):
    user = get_object_or_404(User, pk=request.user.id)
    profile = get_object_or_404(Profile, username=user.username)
    return render(request, 'userDetails.html', {'user':user, 'profile': profile})

#@login_required
#def updateProfile(request):
#    user = get_object_or_404(User, pk=request.user.id)
#    profile = get_object_or_404(Profile, username=user.username)
#    return render(request, 'userDetails.html', {'user':user, 'profile': profile})


@login_required
def uploadCSV(request):
	if request.user.is_superuser:
		return render(request, 'uploadNewMembers.html', None)
	else:
		return redirect('/')
	
@login_required
def importNewMembers(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			spamreader = csv.reader(request.FILES['csvFile'].readlines(), delimiter=',', quotechar='"')
			allRows = [curRow for curRow in spamreader]
			
			res = ['Added the following users and profiles:<br>']
			
			for row in allRows[1:]:
				newUsername = (row[1][0] + row[2]).lower().strip().replace(' ', '')
				newUsermail =  row[6]
				
				if not User.objects.filter(username=newUsername).count():
					res.append(newUsername + ' - ' + newUsermail + '<br>')
					newUser = User.objects.create_user(newUsername, newUsermail,row[17])
					newUser.first_name = row[1]
					newUser.last_name = row[2]
					newUser.save()
					
					newProfile = Profile(post_date = datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S'),
									username = newUsername,
									imageLink = "http://icons.iconarchive.com/icons/deleket/face-avatars/256/Male-Face-" + choice(['A','B']) + str(choice(range(1,6))) + "-icon.png",
									first_name = row[1], 
									last_name = row[2],
									position = row[3],
									department = row[4],
									degrees = row[5],
									email = newUsermail,
									experience_functions = row[7],
									interest_functions = row[8],
									experience = row[9],
									experience_areas = row[10],
									interest_areas = row[11],
									interest_problems = row[12],
									interest_thinktank = row[13],
									experience_thinktank = row[14],
									time_commitment = row[15],
									comments = row[16])
					newProfile.save()
				
			return HttpResponse(res)
		else:
			return redirect('/')
	else:
		return redirect('/')


@login_required
def importCSVBak(request):
	#from os import getcwd, listdir
	#return HttpResponse(listdir(getcwd()))
	#open('test.test','w+')
	with open('/var/www/Thinktank/AcceptedApplications.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		allRows = [curRow for curRow in spamreader]
	
		for row in allRows[1:]:
			newUsername = (row[1][0] + row[2]).lower()
			newUsermail =  row[6]

			if not User.objects.filter(username=newUsername).count():
				print 'Creating User ' + newUsername
				newUser = User.objects.create_user(newUsername, newUsermail,row[17])
				newUser.first_name = row[1]
				newUser.last_name = row[2]
				newUser.save()
				
				newProfile = Profile(post_date = datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S'),
								username = newUsername,
								imageLink = "http://icons.iconarchive.com/icons/deleket/face-avatars/256/Male-Face-" + choice(['A','B']) + str(choice(range(1,6))) + "-icon.png",
								first_name = row[1], 
								last_name = row[2],
								position = row[3],
								department = row[4],
								degrees = row[5],
								email = newUsermail,
								experience_functions = row[7],
								interest_functions = row[8],
								experience = row[9],
								experience_areas = row[10],
								interest_areas = row[11],
								interest_problems = row[12],
								interest_thinktank = row[13],
								experience_thinktank = row[14],
								time_commitment = row[15],
								comments = row[16])
				newProfile.save()
	return HttpResponse('Stuff Added')
"""
	with open('Projects.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		allRows = [curRow for curRow in spamreader]
	
		for row in allRows:
			newProject = Project(
						title = row[0],
						description = row[1],
						contactName = row[2],
						contactEmail = row[3])
			newProject.save()
			for curProfile in row[4].split(','):
				newProject.projectLeads.add( get_object_or_404(Profile, id=int(curProfile)))
			for curProfile in row[5].split(','):
				newProject.teamMembers.add( get_object_or_404(Profile, id=int(curProfile)))
			newProject.save()
"""
