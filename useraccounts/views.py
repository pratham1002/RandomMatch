import xlrd
from django.shortcuts import render, redirect
from .models import SiteUser, Places, Sitesettings
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.postgres.search import *
from django.core.exceptions import *
import random
from django.core.mail import send_mail
from main.settings import EMAIL_HOST_USER
from datetime import datetime

# Create your views here.

def home(request):
    return render(request, 'home.html')

def GetUserData(request):
    try:
        userdata=SiteUser.objects.get(email=(request.GET['fhp']+request.GET['year']+request.GET['roll_no']+"@pilani.bits-pilani.ac.in"))

    except ObjectDoesNotExist:
        return render(request, 'home.html',{"message":"incorrect id"})

    if User.objects.filter(email=userdata.email).exists():
        return render(request,'Login.html',{"userdata":userdata})

    else:
        #random_number=random.randint(1,9999)

        #userdata.verification_code=random_number
        #userdata.save()

        #subject = 'Welcome to MySite'
        #message = 'Here is your login code ' + str(random_number)
        #recepient=userdata.email

        #send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

        return render(request, 'SignUp.html', {"userdata":userdata})

def SignUp(request):
    return render(request, 'SignUp.html')

def Login(request):
    return render(request, 'Login.html')

def NewUser(request):
    userdata=SiteUser.objects.get(email=request.POST['email'])
    password1=request.POST['password']
    password2=request.POST['re_password']
    input_code=request.POST['verification_code']
    
    if input_code==userdata.verification_code:
        if(password1==password2):
            if User.objects.filter(email=userdata.email).exists():
                return render(request,'SignUp.html',{"userdata":userdata, "message":"User already exists"})
            else:
                user=User.objects.create_user(username=userdata.bits_id, password=password1, email=userdata.email, first_name=userdata.name)
                user.save();
                user=auth.authenticate(username=userdata.bits_id,password=password1)

                if user is not None:
                    auth.login(request,user)
                    return Welcome(request)
            
        else:
            return render(request,'SignUp.html',{"userdata":userdata, "message":"Passwords Do Not Match"})
    else:
        return render(request,'SignUp.html',{"userdata":userdata, "message":"Verification Code Does Not Match"})

def FindUser(request):
    userdata=SiteUser.objects.get(email=request.POST['email'])
    password=request.POST['password']

    user=auth.authenticate(username=userdata.bits_id,password=password)

    if user is not None:
        auth.login(request,user)
        return Welcome(request)

    else:
        return render(request,'Login.html',{"userdata":userdata, "message":"invalid password"})

def Welcome(request):
    if request.method=="POST" :
        userdata=SiteUser.objects.get(email=request.POST['email'])
    else:
        userdata=SiteUser.objects.get(email=request.GET['email'])
    return render(request, 'Welcome.html',{"userdata":userdata})

def Change_participation(request):
    sitesettings=Sitesettings.objects.get(obj_number=1)
    userdata=SiteUser.objects.get(email=request.POST['email'])

    if sitesettings.allow_change_participation == False :
        return render(request, 'Welcome.html',{"userdata":userdata, "message":"Time for changing request is over"} )

    if request.POST['preference']=="True" and userdata.participate_request_change_pr==True:
        userdata.participate_request_change_pr=False
        userdata.participate_request=True
        sitesettings.pr_no +=1
        sitesettings.save()
        userdata.priority_number=sitesettings.pr_no
    else:
        userdata.participate_request_change_pr=True
        userdata.participate_request=False
        userdata.assigned_place=""
    userdata.save()
    sitesettings.save()
    return MatchUsers(request)
    #return render(request, 'Welcome.html',{"userdata":userdata} )

def Logout(request):
    auth.logout(request)
    return redirect('/')

def PopulateData(request):
    sitesettings=Sitesettings.objects.get(obj_number=1)
    if sitesettings.data_populated==True :
        return HttpResponse("Data has already been populated")

    loc=("SULIST.xlsx")
    wb=xlrd.open_workbook(loc)
    sheet=wb.sheet_by_index(0)

    for i in range(sheet.nrows):
        newuser=SiteUser()
        newuser.name=sheet.cell_value(i,1)
        newuser.bits_id=sheet.cell_value(i,0)
        newuser.year=newuser.bits_id[0:4]
        newuser.email=sheet.cell_value(i,5)+"@pilani.bits-pilani.ac.in"
        hostel=sheet.cell_value(i,2)

        if hostel=="MR":
            newuser.gender='F'
        else:
            newuser.gender='M'
        
        newuser.save()
    sitesettings.data_populated=True
    sitesettings.save()
    return HttpResponse("Success")

def MatchUsers(request):
    sitesettings=Sitesettings.objects.get(obj_number=1)
    if sitesettings.allow_user_match==False :
        return HttpResponse("Matches not allowed rn")

    participants=SiteUser.objects.filter(participate_request=True)
    female_participants_priority_number=[]
    male_participants_priority_number=[]
    years=["2019","2018","2017","2016"]

    for year in years :

        for participant in participants:
            userdata=SiteUser.objects.get(email=participant.email)
            if userdata.gender=='F' and userdata.year==year :
                female_participants_priority_number.append(userdata.priority_number)
            if userdata.gender=='M' and userdata.year==year :
                male_participants_priority_number.append(userdata.priority_number)

        number_of_females=len(female_participants_priority_number)
        number_of_males=len(male_participants_priority_number)

        female_participants_priority_number.sort()
        male_participants_priority_number.sort()

        places=Places.objects.all()


        if number_of_males >= number_of_females:
            for i in range(number_of_males) :
                if i < number_of_females:

                    userdatafemale=SiteUser.objects.get(priority_number=female_participants_priority_number[i])
                    userdatafemale.participate_request_granted=True
                    userdatafemale.assigned_place=places[i].place_name
                    userdatafemale.match_id=year + str(i)

                    userdatamale=SiteUser.objects.get(priority_number=male_participants_priority_number[i])
                    userdatamale.participate_request_granted=True
                    userdatamale.assigned_place=places[i].place_name
                    userdatamale.match_id=year + str(i)

                    userdatamale.mathed_with=userdatafemale.bits_id
                    userdatafemale.mathed_with=userdatamale.bits_id

                    userdatafemale.save()
                    userdatamale.save()
                else:
                    userdata=SiteUser.objects.get(priority_number=male_participants_priority_number[i])
                    userdata.assigned_place='Waitlist ' + str(i-number_of_females+1) 
                    userdata.save()
        else:
            for i in range(number_of_females):
                if i < number_of_males:

                    userdatafemale=SiteUser.objects.get(priority_number=female_participants_priority_number[i])
                    userdatafemale.participate_request_granted=True
                    userdatafemale.assigned_place=places[i].place_name
                    userdatafemale.match_id=year + str(i)

                    userdatamale=SiteUser.objects.get(priority_number=male_participants_priority_number[i])
                    userdatamale.participate_request_granted=True
                    userdatamale.assigned_place=places[i].place_name
                    userdatamale.match_id=year + str(i)

                    userdatamale.mathed_with=userdatafemale.bits_id
                    userdatafemale.mathed_with=userdatamale.bits_id

                    userdatafemale.save()
                    userdatamale.save()
                else:
                    userdata=SiteUser.objects.get(priority_number=female_participants_priority_number[i])
                    userdata.assigned_place='Waitlist ' + str(i-number_of_males+1) 
                    userdata.save()
    return Welcome(request)