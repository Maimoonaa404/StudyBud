from django.contrib import admin
from . models import Room,Topic,Messages
# Register your models here.
admin.site.register(Room)#registering model with admin panel
admin.site.register(Topic)
admin.site.register(Messages)