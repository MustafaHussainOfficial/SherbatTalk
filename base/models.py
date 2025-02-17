from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100 ,null=True, default='')
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, default='') #Overwriting the default Email field of User Model
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email' #To set the email as the input variable to login.
    REQUIRED_FIELDS = ['username'] 




class Topic(models.Model):
    name = models.TextField(max_length=200) 

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True) #Setting null=True means that this feild can be blank. Otherwise it couldn't be left blank. Blank so that when submitting form it can be left blank.
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) #So that whenever we change something and save it takes the time stamp.
    created = models.DateTimeField(auto_now_add=True) #It takes the time stamp when it is saved for the first time.

    class Meta:
        ordering = ['-updated', '-created'] #This is to order the rooms by the time they were added

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, default=1)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # This is to make the one to many relation with the parent class. The the foreign key here is the primary key of the parent. on_delete=models.CASCADE: When a room is deleted all the messages get deleted.
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) #So that whenever we change something and save it takes the time stamp.
    created = models.DateTimeField(auto_now_add=True) #It takes the time stamp when it is saved for the first time.

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


class Resource(models.Model):
    room = models.ForeignKey(Room, related_name='resources', on_delete=models.CASCADE)
    link = models.URLField()
    description = models.TextField()

    def __str__(self):
        return f"Resource: {self.link}"