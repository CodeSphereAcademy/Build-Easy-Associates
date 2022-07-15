import json
from django.http import HttpResponse, QueryDict
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .models import ClientInfo,ClientServiceInfo,Post, Project, RecEmail, SendEmail, Team,WorkPost
from datetime import date
import urllib.request
import urllib.parse

def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

def userHome(request):
    
    clientServiceInfo = ClientServiceInfo.objects.all()

    navActive = "active"
    
    if request.method == 'POST':

        resBody = QueryDict(request.body)
        msg = resBody.dict()

        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        address = request.POST["address"]
        plotSize = request.POST["plotsize"]
        approxPlotSize = request.POST["approxplotsize"]
        numFloor = request.POST["numfloor"]
        plotAddress = request.POST["plotaddress"]
        proDescription = request.POST["prodesc"]
        services = request.POST.getlist('service')

        try:
            interior = request.POST["interior"]
        except:
            interior = "No"
            interiorArea = 0
        try:    
            basement = request.POST["basement"]
        except:
            basement = "No"
            basementArea = 0
        try:
            emailSend = request.POST["emailsend"]
        except:
            emailSend = "No"

        estimateCost = 0
        
        projectCost = int(approxPlotSize) * int(numFloor) * 1450
        
        if interior == "yes":
            interiorArea = request.POST["interiorArea"]
            estimateCost += int(interiorArea) * 40
        if basement == "yes":
            basementArea = request.POST["basementArea"]
            estimateCost += int(basementArea) * 1850 * 0.055

        service = ClientServiceInfo.objects.filter(id__in=services)
        
        for s in service:
            estimateCost += ( projectCost * s.cost ) / 100    

        client = ClientInfo.objects.create(name=name,phone=phone,email=email,address=address,plotSize=plotSize,builtArea=approxPlotSize,numFloor=numFloor,plotAddress=plotAddress,projectDescription=proDescription,interiorArea=interiorArea,basementArea=basementArea,totalCost=estimateCost,approved=False)
        client.serviceOpted.set(service)
        client.save()

        if emailSend == "yes":
            send_mail(str(name)+" - New Quotation",str(msg),"buildeasy01@gmail.com",[str(email),"buildeasy01@gmail.com"])
            # email = SendEmail.objects.create(client=client,title="New Quotation",msg=str(msg))
            # email.save()

        if emailSend == "No":
            send_mail(str(name)+" - New Quotation",str(msg),"buildeasy01@gmail.com",["buildeasy01@gmail.com"])
            # email = SendEmail.objects.create(client=client,title="New Quotation",msg=str(msg))
            # email.save()    

        return redirect(quoteResponse,permanent=True)
    else:
        return render(request,"userPage/userHome.html",{'service':clientServiceInfo,'homeActive':navActive})

def quoteResponse(request):
    return render(request,'userPage/quoteResponse.html',{})

def userProjects(request):
    projects = Project.objects.all()
    navActive = "active"
    return render(request,'userPage/userProjects.html',{'projectsActive':navActive,'projects':projects})

def userAbout(request):
    navActive = "active"
    return render(request,'userPage/userAbout.html',{'aboutActive':navActive})

def userServices(request):
    navActive = "active"
    services = ClientServiceInfo.objects.all()
    return render(request,'userPage/userServices.html',{'servicesActive':navActive,"services":services})

def userContact(request):
    navActive = "active"
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        msg = request.POST["msg"]
        responseMsg = "Thank you for your Query, we'll get back to you soon.\n\nRegards,\nBuild-Easy"
        send_mail(str(name)+" - Query",str(msg),"buildeasy01@gmail.com",["buildeasy01@gmail.com"])
        send_mail("Build-Easy Associates",str(responseMsg),"buildeasy01@gmail.com",[str(email)])
        recEmail = RecEmail.objects.create(name=name,email=email,phone=phone,msg=msg)
        recEmail.save()
    return render(request,'userPage/userContact.html',{'contactActive':navActive})                

def userToken(request):
    if(request.method == "POST"):
        id = request.POST["tokenID"]
        client = ClientInfo.objects.get(id=int(id))
        workPost = WorkPost.objects.get(client=client)
        posts = Post.objects.filter(workPost=workPost)
        return render(request,'userPage/userPosts.html',{'client':client,'workPost':workPost,'posts':posts})
    return render(request,'userPage/userToken.html',{})

def userPost(request,id):
    post = Post.objects.get(id=id)
    return render(request,'userPage/userPost.html',{'post':post})

def adminPage(request):
    return render(request,'userPage/adminPage.html',{})

def clientPage(request):
    clients = ClientInfo.objects.filter(approved=True)
    return render(request,'userPage/clientPage.html',{'clients':clients})

def verifyClients(request):
    clients = ClientInfo.objects.filter(approved=False)
    if request.method == "POST":
        clientId = request.POST["clientID"]
        client = ClientInfo.objects.get(id=clientId)
        name = str(client.name)    
        client.projectTitle = request.POST["projectTitle"]
        client.tokenAmount = request.POST["tokenAmount"]
        client.totalCost = request.POST["finalProjectCost"]
        client.pendingAmount = int(request.POST["finalProjectCost"]) - int(request.POST["tokenAmount"])
        client.clientRequirements = request.POST["reqClient"]
        client.projectStartDate = request.POST["startDate"]
        client.projectEndDate = request.POST["endDate"]
        client.approved = True
        refID = name[slice(0,4)]+"@"+str(clientId)
        client.referenceID = refID.replace(" ","")
        client.save()
        project = WorkPost.objects.create(client=client)
        project.save()
        msg = "Hello, "+str(client.name)+"\nYour Reference ID: "+str(client.referenceID)+"\nAmount Paid: "+str(client.tokenAmount)+"\nPending Amount: "+str(client.pendingAmount)+"\n\nRegards,\nBuild-Easy"
        send_mail(str(name)+" - Token Received",str(msg),"buildeasy01@gmail.com",[str(client.email)])
        email = SendEmail.objects.create(client=client,title="Token Received - "+str(client.name),msg=msg)
        email.save()
    return render(request,'userPage/verifyClients.html',{'clients':clients})    

def clientInfo(request,id):  
    client = ClientInfo.objects.get(id=id)
    return render(request,'userPage/clientInfo.html',{'client':client}) 

def servicePage(request):
    if(request.method == 'POST'):
        pic = request.FILES['serviceIcon']
        name = request.POST['serviceName']
        cost = request.POST['serviceCost']
        details = request.POST['serviceDetail']
        service = ClientServiceInfo.objects.create(pic=pic,name=name,cost=cost,details=details)
        service.save()
    services = ClientServiceInfo.objects.all()    
    return render(request,'userPage/servicePage.html',{"services":services})

def projects(request):
    projects = WorkPost.objects.all()
    return render(request,'userPage/projects.html',{'projects':projects})

def project(request,id=0):
    if(request.method == "POST"):
        id = request.POST["tokenID"]
    client = ClientInfo.objects.get(id=id)
    try:
        project = WorkPost.objects.get(client=client)
        posts = Post.objects.filter(workPost=project)
    except:
        project = None
        posts = None       
    return render(request,'userPage/project.html',{'client':client,'project':project,'posts':posts})

def postUpload(request,id=0):
    if(request.method == 'POST'):
        id = request.POST['clientId']
        client = ClientInfo.objects.get(id=id)
        projectx = WorkPost.objects.get(client=client)
        pic1 = None
        pic2 = None
        pic3 = None
        pic4 = None
        pic5 = None
        pic6 = None
        pic7 = None
        pic8 = None
        pic9 = None
        pic10 = None
        try:
            pic1 = request.FILES['imageFile1']
            pic2 = request.FILES['imageFile2']
            pic3 = request.FILES['imageFile3']
            pic4 = request.FILES['imageFile4']
            pic5 = request.FILES['imageFile5']
            pic6 = request.FILES['imageFile6']
            pic7 = request.FILES['imageFile7']
            pic8 = request.FILES['imageFile8']
            pic9 = request.FILES['imageFile9']
            pic10 = request.FILES['imageFile10']
        except:
            pass    
        name = request.POST['postName']
        detail = request.POST['postDetail']
        post = Post(workPost=projectx,pic1=pic1,pic2=pic2,pic3=pic3,pic4=pic4,pic5=pic5,pic6=pic6,pic7=pic7,pic8=pic8,pic9=pic9,pic10=pic10,name=name,detail=detail,publishDate=date.today())
        post.save()
        return redirect(project,id=id,permanent=True)
    else:    
        client = ClientInfo.objects.get(id=id)
        projectx = WorkPost.objects.get(client=client)
        return render(request,'userPage/uploadPost.html',{'project':projectx})    

def upcomingProjects(request):
    if request.method == "POST":
        try:
            if request.POST["startDate"]:
                client = ClientInfo.objects.get(id=request.POST["clientID"])
                client.projectStartDate = request.POST["startDate"]
                client.projectEndDate = request.POST["endDate"]
                client.save()
        except:
            pass          
        try:
            if request.POST["startNow"]:
                client = ClientInfo.objects.get(id=request.POST["clientID"])
                client.projectStarted = "Yes"
                client.save()       
        except:
            pass        
    clients = ClientInfo.objects.filter(projectStarted="No",approved=True)
    projects = WorkPost.objects.filter(client__in=clients)
    return render(request,'userPage/upcomingProjects.html',{'projects':projects})

def ongoingProjects(request):
    if request.method == "POST":    
        try:
            if request.POST["startNow"]:
                client = ClientInfo.objects.get(id=request.POST["clientID"])
                client.projectStarted = "Done"
                client.save()       
        except:
            pass    
    clients = ClientInfo.objects.filter(projectStarted="Yes",approved=True)
    projects = WorkPost.objects.filter(client__in=clients)
    return render(request,'userPage/ongoingProjects.html',{'projects':projects})

def pastProjects(request): 
    clients = ClientInfo.objects.filter(projectStarted="Done",approved=True)
    projects = WorkPost.objects.filter(client__in=clients)
    return render(request,'userPage/pastProjects.html',{'projects':projects})

def recentPosts(request):
    posts = Post.objects.all()
    return render(request,'userPage/recentPosts.html',{'posts':posts})

def tokenSearch(request):
    return render(request,'userPage/tokenSearch.html',{})

def updateClientInfo(request,id):
    clientServiceInfo = ClientServiceInfo.objects.all()
    client = ClientInfo.objects.get(id=id)
    return render(request,'userPage/updateClientInfo.html',{'client':client,'service':clientServiceInfo,})

def updateWebsite(request):
    if(request.method == 'POST'):
        pic1 = request.FILES['firstImg']
        pic2 = request.FILES['secondImg']
        name = request.POST['projectName']
        cost = request.POST['projectCost']
        area = request.POST['projectArea']
        desc = request.POST['projectDesc']
        project = Project.objects.create(pic1=pic1,pic2=pic2,projectTitle=name,projectCost=cost,projectArea=area,projectDesc=desc)
        project.save()
    projects = Project.objects.all()    
    return render(request,'userPage/updateWebsite.html',{"projects":projects})

def updateTeams(request):
    if(request.method == 'POST'):
        pic = request.FILES['profileImg']
        name = request.POST['memberName']
        phone = request.POST['memberMob']
        jobRole = request.POST['memberRole']
        jobDesc = request.POST['memberRoleDesc']
        salary = request.POST['memberSalary']
        staff = Team.objects.create(pic=pic,name=name,phone=phone,jobRole=jobRole,jobDesc=jobDesc,salary=salary)
        staff.save()
    team = Team.objects.all()   
    return render(request,'userPage/updateTeams.html',{"team":team}) 

def emailQueries(request):
    return render(request,'userPage/emailQueries.html',{})

def projectWrapUp(request):
    projects = WorkPost.objects.all()
    return render(request,'userPage/projectWrapUp.html',{'projects':projects})    

def genratePdf(request,id):
    client = ClientInfo.objects.get(id=id)
    workPost = WorkPost.objects.get(client=client)
    posts = Post.objects.filter(workPost=workPost)
    return render(request,'userPage/genratePdf.html',{'client':client,'workPost':workPost,'posts':posts})       