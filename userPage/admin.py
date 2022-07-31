from django.contrib import admin
from .models import ClientInfo, ClientServiceInfo, Post, Project, RecEmail, SendEmail, UpdateVariable, WorkPost, Team

class ClientInfoAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','totalCost','approved','projectStarted','projectStatus')

class ClientServiceInfoAdmin(admin.ModelAdmin):
    list_display = ('id','name','cost')    

class PostStackInline(admin.StackedInline):
    model = Post
    extra = 0    

class WorkPostAdmin(admin.ModelAdmin):
    list_display = ('id','client')
    inlines = [PostStackInline]

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','workPost','detail','publishDate')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id','name','jobRole','joiningDate')    

class ReceivedEmail(admin.ModelAdmin):
    list_display = ('name','email','date')

class SendedEmail(admin.ModelAdmin):
    list_display = ('client','title','date')    

# Register your models here.
admin.site.register(ClientInfo,ClientInfoAdmin)
admin.site.register(ClientServiceInfo,ClientServiceInfoAdmin)
admin.site.register(WorkPost,WorkPostAdmin)
admin.site.register(Post,PostAdmin) 
admin.site.register(Project)
admin.site.register(Team,TeamAdmin)
admin.site.register(RecEmail,ReceivedEmail)
admin.site.register(SendEmail,SendedEmail)
admin.site.register(UpdateVariable)
