from datetime import date
import email
from django.db import models
from psycopg2 import Date

# Create your models here.
class ClientServiceInfo(models.Model):
    pic = models.ImageField(null=True)
    name = models.CharField(max_length=30)
    cost = models.FloatField()
    details = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Service"       

class ClientInfo(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=100)
    plotSize = models.IntegerField()
    builtArea = models.IntegerField()
    numFloor = models.IntegerField()
    plotAddress = models.CharField(max_length=100)
    projectDescription = models.CharField(max_length=200,null=True)
    serviceOpted = models.ManyToManyField(ClientServiceInfo)
    interiorArea = models.IntegerField(default=0,null=True)
    basementArea = models.IntegerField(default=0,null=True)
    totalCost = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    approved = models.BooleanField(default=False)
    referenceID = models.CharField(max_length=50,default="",null=True)
    projectTitle = models.CharField(max_length=50,default="",null=True)
    tokenAmount = models.IntegerField(default=0,null=True)
    pendingAmount = models.IntegerField(default=0,null=True)
    clientRequirements = models.CharField(max_length=200,default="",null=True)
    projectStartDate = models.DateField(default=date.today,null=True)
    projectEndDate = models.DateField(default=date.today,null=True)
    projectStatus = models.CharField(max_length=50,default="Pending",null=True)
    projectStarted = models.CharField(max_length=50,default="No",null=True)
    def __str__(self):
        return self.name

class WorkPost(models.Model):
    client = models.ForeignKey(ClientInfo,on_delete=models.CASCADE)
    def __str__(self):
        return self.client.name

class Post(models.Model):
    workPost = models.ForeignKey(WorkPost,on_delete=models.CASCADE)
    pic1 = models.ImageField(null=True)
    pic2 = models.ImageField(null=True)
    pic3 = models.ImageField(null=True,blank=True)
    pic4 = models.ImageField(null=True,blank=True)
    pic5 = models.ImageField(null=True,blank=True)
    pic6 = models.ImageField(null=True,blank=True)
    pic7 = models.ImageField(null=True,blank=True)
    pic8 = models.ImageField(null=True,blank=True)
    pic9 = models.ImageField(null=True,blank=True)
    pic10 = models.ImageField(null=True,blank=True)
    name = models.CharField(max_length=20,null=True)
    detail = models.CharField(max_length=50)
    publishDate = models.DateField(default=date.today,null=True)
    def __str__(self):
        return self.detail  

class Project(models.Model):
    pic1 = models.ImageField()
    pic2 = models.ImageField()
    projectTitle = models.CharField(max_length=20,null=False)
    projectCost = models.FloatField(null=True)
    projectArea = models.FloatField(null=True)
    projectDesc = models.CharField(max_length=200,null=False)
    publishDate = models.DateField(default=date.today,null=True)
    def __str__(self):
        return self.projectTitle

class Team(models.Model):
    pic = models.ImageField()
    name = models.CharField(max_length=20,null=False)
    phone = models.CharField(max_length=10,null=True)
    jobRole = models.CharField(max_length=30,null=True)
    jobDesc = models.CharField(max_length=200,null=False)
    salary = models.IntegerField()
    joiningDate = models.DateField(default=date.today,null=True)
    def __str__(self):
        return self.name        

class RecEmail(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    msg = models.CharField(max_length=300)
    date = models.DateField(default=date.today,null=True)
    def __str__(self):
        return self.name  
    class Meta:
        verbose_name = "Received Email"      

class SendEmail(models.Model):
    client = models.ForeignKey(ClientInfo,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    msg = models.CharField(max_length=300)
    date = models.DateField(default=date.today,null=True)
    def __str__(self):
        return self.client.name
    class Meta:
        verbose_name = "Send Email"     
