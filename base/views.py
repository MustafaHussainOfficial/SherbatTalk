from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User, Resource #Importing 'Room' and 'Topic' data tables from models.py file.
from .forms import RoomForm, UserForm, MyUserCreationForm #Importing the default django form form the 'form.py' file.
from django.http import HttpResponse
from django.db.models import Q 
from django.contrib import messages #For Django Flash messages
from django.contrib.auth import authenticate, login, logout #For Login authentication
from django.contrib.auth.decorators import login_required #Decorator that is used for restricting the pages this specific one will restrict the unauthenticated users to perform a certain action.

def loginPage(request):
    
    page = 'login'

    if request.user.is_authenticated:
            return redirect('home')


    if request.method == 'POST': #Check whether the method is set to 'POST' in the form in the html.
        email = request.POST.get('email').lower() #Extracts the username from the form
        password = request.POST.get('password') #Extracts the password from the form 
        try:
            user = User.objects.get(email=email) #Checking whether the username exist in the database.
        except:
           messages.error(request, 'User does not exist') #If user name does not exist show this flash message.
        user = authenticate(request, email=email, password=password) #Authenticate the username and password from the the database.

        if user is not None: # Checks whether the credentials match the ones in the data base is it return not none then they match.
            login(request, user) # Logs in the user.
            return redirect('home') # Redirects to the home page once the user is logged in.
        else:
            messages.error(request, 'Username or password is incorrect') # If the user variable is None which means the password is incorrect then display this flash message.

    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request) # simply logs the user out.
    return redirect('home') # once the user is loged out redirects to the home page.

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid(): # Checks whether the form is valid.
            user = form.save(commit=False) # Saves the form to the database.
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.error_messages)
    context = {'page' : page, 'form': form}
    return render(request, 'base/login_register.html', context)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' #This checks what the query token is and captures what is added to the home page url when filtering things.

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q) | Q(host__username__icontains = q)) #This applies filter to the the querry from the database. The Q method or fuction is used so that the search querry can be made dynamic.
        #Topic name matches the search | Name of the room matches search | Room decription matches search
    topics = Topic.objects.all()[0:5] # Queries all the topics from the database.
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q) | Q(user__username__icontains = q))
    context = {'rooms': rooms, 'topics': topics, 'room_count' : room_count, 'room_messages':room_messages} #Contains all the variable that will be shared with 'home' template.
    return render(request, 'base/home.html', context)


def room(request, pk): #It takes in the primary key of a specific 'room', and it captures that through the url which has the primary key in it.
    room = Room.objects.get(id = pk) #It gets the room with an ID matching the primary key given.
    room_messages = room.message_set.all() #This is accessing the messages that are related to this room. A parent model can access the child model.
                                                     #.order_by('-created') is to desplay the most recent message first.

    participants = room.participants.all()
    context = {'room' : room, 'room_messages' : room_messages, 'participants': participants} #Contains all the variable that will be shared with 'home' template.
    return render(request, 'base/room.html', context) 

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user' : user, 'rooms' : rooms, 'room_messages': room_messages, 'topics' : topics}
    
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        resource_count = 0
        while f'link_{resource_count}' in request.POST:
            link = request.POST.get(f'link_{resource_count}')
            description = request.POST.get(f'description_{resource_count}')
            if link and description:
                Resource.objects.create(
                    room=room,
                    link=link,
                    description=description,
                )
            resource_count += 1
        
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)  
    form = RoomForm(instance=room)  
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        room.resources.all().delete()

        resource_links = request.POST.getlist('resource_link')
        resource_descriptions = request.POST.getlist('resource_description')

        for link, description in zip(resource_links, resource_descriptions):
            if link and description:  
                Resource.objects.create(
                    room=room,
                    link=link,
                    description=description
                )

        return redirect('home')

    return render(request, 'base/update_room.html', {
        'form': form,
        'room': room,
        'topics': topics,
    })

@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed to edit this room!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url = 'login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed to delete the message!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)

    return render(request, 'base/update_user.html', {'form' : form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics' : topics})

def activityPage(request):

    room_messages = Message.objects.all()




    return render(request, 'base/activity.html', {'room_messages' : room_messages})