from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"), #URL pattern for login view
    path('logout/', views.logoutUser, name="logout"), #URL pattern for logout view
    path('register/', views.registerPage, name="register"), #URL pattern for register view
    path('', views.home, name='home'), #URL for the main page when nothing is after the main URL
    path('room/<int:pk>', views.room, name='room'), #URL for each room
    path('create-room/', views.createRoom, name='create-room'), #URL for room creation form page
    path('update-room/<int:pk>', views.updateRoom, name='update-room'), #URL for room updation form hence the priary key for a room is passed in URL
    path('delete-room/<int:pk>', views.deleteRoom, name='delete-room'), #URL for the deletion of room
    path('delete-message/<int:pk>', views.deleteMessage, name='delete-message'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
]