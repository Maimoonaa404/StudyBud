from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import Room,Topic,Messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm
from django.contrib.auth.decorators import login_required

'''rooms=[
    {'id':1,'name':'lets learn django!'},
    {'id':2,'name':'Design with me!'},
    {'id':3,'name':'Developers!'},
]'''

def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        #making sure user exists
        try:
          user =User.objects.get(username=username)
        except:
          messages.error(request,'User does not exists')

        user=authenticate(request,username=username,password=password)
        #making sure credentials are crct
        #authenticate return user object
        if user is not None:
         login(request,user)
         return redirect('home')
        else:
            messages.error(request,'Username OR Password doesnt exists')
        
        
    context={'page':page}
    return render(request,'base/login-reg.html',context)

def regpage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')

    return render(request,'base\login-reg.html',{'form':form})

def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    #retrieve value of q parameter from req obj i.e url
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(desc__icontains=q)
        )#querying DB (upwards)
    topics=Topic.objects.all()
    room_count=rooms.count()
    room_messages=Messages.objects.filter(Q(room__topic__name__icontains=q)
                                          )
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}#passing in data to the template
    return render(request,'base/home.html',context)

def room(request,pk):
   ''' room=None
    for i in rooms:
        if i['id']==int(pk):# id of room=pk of url
            room=i'''
   room=Room.objects.get(id=pk)
   room_messages=room.messages_set.all().order_by('-created')
   participants=room.participants.all()
   #participants and msgs belonging to particular room id are extracted
   if request.method =='POST':
       message = Messages.objects.create (
           user=request.user,
           body=request.POST.get('body'),
           room=room)
       #The create method allows you to create a new instance of the Messages model in the database.
       room.participants.add(request.user)
       return redirect('room',pk=room.id)
           
   context={'room':room,'room_messages':room_messages,'participants':participants}
   return render(request,'base/room.html',context)
    # the room value can be null if no match is found
            

def userprofile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    #room related to user is extracted
    room_messages=user.messages_set.all()
    #messages related to user are extracted
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'topics':topics,'room_messages':room_messages}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
#redirects to login page
def createRoom(request):
    form=RoomForm()# we have a form
    if request.method =='POST':#send the post data which is recieved in request
        form=RoomForm(request.POST)#add the data to the form
        if form.is_valid():
            rooms = form.save(commit=False)
            rooms.host=request.user
            rooms.save()
            return redirect("home")
        
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')   
def updateRoom(request,pk):
    
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)#to tell it what room to update
    if request.user != room.host:
        return HttpResponse('you are not allowed here!!!')
    if request.method =='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you are not allowed here!!!')
    if request.method =='POST':
        room.delete()
        return redirect("home")

    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMsg(request,pk):
    message=Messages.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed here!!!')
    if request.method =='POST':
        message.delete()
        return redirect("home")

    return render(request,'base/delete.html',{'obj':message})

