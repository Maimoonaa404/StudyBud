from django.db import models
from django.contrib.auth.models import User
#Foreign Keys:
'''Room model has a foreign key to the User model with host. This means a room has one host (user).
Room model also has a foreign key to the Topic model with topic. This means a room can have one topic (optional).
Messages model has a foreign key to the User model with user. This means a message belongs to one user.
Messages model has a foreign key to the Room model with room. This means a message belongs to one room. '''


class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Room(models.Model):
    #Uses models.ForeignKey to establish a relationship between Room and User.
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
     #host field connects to the User model.
    # on_delete=models.SET_NULL specifies that if a user is deleted,
    #the host field in the Room model will be set to null instead of raising an error.
    #null=True allows the host field to be null
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    desc=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    update=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-update','-created']

    def __str__(self):
        return self.name


class Messages(models.Model):
    #user can have many messages but msg has one user *-1
    user=models.ForeignKey(User,on_delete=models.CASCADE)
     #each room has many msg but msg belongs to one room *-1
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    update=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-update','-created']

    def __str__(self):
        return self.body[0:50]





             