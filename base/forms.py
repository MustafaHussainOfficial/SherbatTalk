from django.forms import ModelForm #Importing the django default form

from .models import Room, User, Resource

from django.contrib.auth.forms import UserCreationForm 

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar' ,'name','username', 'email', 'bio']
        

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'topic', 'description']

class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = ['link', 'description']