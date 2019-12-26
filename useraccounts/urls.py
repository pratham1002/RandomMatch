from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('GetUserID',views.GetUserData,name='GetUserData'),
    path('SignUp',views.SignUp,name='SignUp'),
    path('Login',views.Login,name='Login'),
    path('NewUser',views.NewUser,name='NewUser'),
    path('FindUser',views.FindUser,name='FindUser'),
    path('Logout',views.Logout,name='Logout'),
    path('Welcome',views.Welcome,name='Welcome'),
    path('Change_participation',views.Change_participation,name='Change_participation'),
    path('PopulateData',views.PopulateData,name='PopulateData'),
    path('MatchUsers',views.MatchUsers,name='MatchUsers')
]
