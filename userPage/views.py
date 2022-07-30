import json
from django.http import HttpResponse, JsonResponse, QueryDict
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .models import ClientInfo,ClientServiceInfo,Post, Project, RecEmail, SendEmail, Team, UpdateVariable, WorkPost
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

    servicesText = ""

    variables = UpdateVariable.objects.all()
    if variables:
        variables = variables[0]
    
    clientServiceInfo = ClientServiceInfo.objects.all()

    navActive = "active"
    
    if request.method == 'POST':

        # resBody = QueryDict(request.body)
        # msg = resBody.dict()

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
            servicesText += s.name+", "    

        client = ClientInfo.objects.create(name=name,phone=phone,email=email,address=address,plotSize=plotSize,builtArea=approxPlotSize,numFloor=numFloor,plotAddress=plotAddress,projectDescription=proDescription,interiorArea=interiorArea,basementArea=basementArea,totalCost=estimateCost,approved=False)
        client.serviceOpted.set(service)
        client.save()

        msg = """WELCOME TO BUILD-EASY ASSOCIATES

Hello {name},
Thank you for sending your information. We are delighted to assist you. We will begin your project after receiving a 25% advance payment. Following this, your reference ID will generate, which allows you to track your project. Enjoy our services.

NAME - {name}
CONTACT NO. - {phone}
EMAIL ID - {email}
ADDRESS - {address}
PLOT AREA (SQ.FT.) - {plotSize} sqft.
SUPER BUILT-UP AREA (SQ.FT.) - {builtArea} sqft.
NO. OF FLOOR - {numFloors}
PLOT ADDRESS - {plotAddress}
PROJECT DESCRIPTION - {projectDescriptions}
SERVICES - {services}

Your estimated project cost is {projectCost} Rs.
Payable amount 25% (approx.) {minAmount} Rs.

Regards
BUILD-EASY ASSOCIATES""".format(name=name,phone=phone,email=email,address=address,plotSize=plotSize,builtArea=approxPlotSize,numFloors=numFloor,plotAddress=plotAddress,projectDescriptions=proDescription,services=servicesText,projectCost=estimateCost,minAmount=int(estimateCost)*0.25)

        if emailSend == "yes":
            send_mail(str(name)+" - New Quotation",str(msg),"buildeasy01@gmail.com",[str(email),"buildeasy01@gmail.com"])
            email = SendEmail.objects.create(client=client,title="New Quotation",msg=str(msg))
            email.save()

        if emailSend == "No":
            send_mail(str(name)+" - New Quotation",str(msg),"buildeasy01@gmail.com",["buildeasy01@gmail.com"])
            email = SendEmail.objects.create(client=client,title="New Quotation",msg=str(msg))
            email.save()    

        return redirect(quoteResponse,permanent=True)
    else:
        return render(request,"userPage/userHome.html",{'service':clientServiceInfo,'homeActive':navActive,'var':variables})

def quoteResponse(request):
    return render(request,'userPage/quoteResponse.html',{})

def userProjects(request):
    projects = Project.objects.all()
    navActive = "active"
    return render(request,'userPage/userProjects.html',{'projectsActive':navActive,'projects':projects})

def userAbout(request):
    navActive = "active"
    variables = UpdateVariable.objects.all()
    if variables:
        variables = variables[0] 
    return render(request,'userPage/userAbout.html',{'aboutActive':navActive,'var':variables})

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
    try:
        if(request.method == "POST"):
            id = request.POST["tokenID"]
            client = ClientInfo.objects.get(id=int(id))
            workPost = WorkPost.objects.get(client=client)
            posts = Post.objects.filter(workPost=workPost)
            return render(request,'userPage/userPosts.html',{'client':client,'workPost':workPost,'posts':posts})
    except:
        return redirect(pageNotFound,param="Reference ID",permanent=True)       
    return render(request,'userPage/userToken.html',{})

def userPost(request,id):
    try:
        post = Post.objects.get(id=id)
    except:
        return redirect(pageNotFound,param="Post",permanent=True)
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
        msg = """Hello {name}, 

BUILD- EASY ASSOCIATES has approved your project. To track your project, use the reference ID {refID}. Enjoy our services.

RECEIVED AMOUNT- {tokenAmt}
PENDING AMOUNT- {pendingAmt}

Regards,
BUILD-EASY ASSOCIATES
""".format(name=str(client.name),refID=str(client.referenceID),tokenAmt=str(client.tokenAmount),pendingAmt=str(client.pendingAmount))
        send_mail(str(name)+" - APPROVAL OF PROJECT",str(msg),"buildeasy01@gmail.com",[str(client.email)])
        email = SendEmail.objects.create(client=client,title="Token Received - "+str(client.name),msg=msg)
        email.save()
    return render(request,'userPage/verifyClients.html',{'clients':clients})    

def clientInfo(request,id):  
    try:    
        client = ClientInfo.objects.get(id=id)
    except:
        return redirect(pageNotFound,param="Client",permanent=True)
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
    try:
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
    except:
        return redirect(pageNotFound,param="Project",permanent=True)    

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
        amtPaid = request.POST['pendingAmt']
        detail = request.POST['postDetail']
        post = Post(workPost=projectx,pic1=pic1,pic2=pic2,pic3=pic3,pic4=pic4,pic5=pic5,pic6=pic6,pic7=pic7,pic8=pic8,pic9=pic9,pic10=pic10,name=name,amtPaid=amtPaid,detail=detail,publishDate=date.today())
        post.save()
        client.pendingAmount = int(client.pendingAmount) - int(amtPaid)
        client.save()
        msg = """Hello, {name}

Your project has been updated. To track your project, use the reference ID {refID}. Enjoy our services.
Amount Received- {amtReceived}
Pending Amount- {pendingAmt}

Regards
BUILD-EASY ASSOCIATES
""".format(name=str(client.name),refID=str(client.referenceID),amtReceived=str(amtPaid),pendingAmt=str(client.pendingAmount))
        send_mail(str(name)+" - Project Updated",str(msg),"buildeasy01@gmail.com",[str(client.email)])
        email = SendEmail.objects.create(client=client,title="Project Updated - "+str(client.name),msg=msg)
        email.save()
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

    servicesText = ""

    if request.method == "POST":

        id = request.POST["id"]
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
            servicesText += s.name+", "   

        client = ClientInfo.objects.get(id=id)     

        client.name=name
        client.phone=phone
        client.email=email
        client.address=address
        client.plotSize=plotSize
        client.builtArea=approxPlotSize
        client.numFloor=numFloor
        client.plotAddress=plotAddress
        client.projectDescription=proDescription
        client.interiorArea=interiorArea
        client.basementArea=basementArea
        client.totalCost=estimateCost
        client.approved=False
        client.serviceOpted.set(service)
        client.save()

        msg = """WELCOME TO BUILD-EASY ASSOCIATES

Hello {name},
Thank you for sending your information. We are delighted to assist you. We will begin your project after receiving a 25% advance payment. Following this, your reference ID will generate, which allows you to track your project. Enjoy our services.

NAME - {name}
CONTACT NO. - {phone}
EMAIL ID - {email}
ADDRESS - {address}
PLOT AREA (SQ.FT.) - {plotSize} sqft.
SUPER BUILT-UP AREA (SQ.FT.) - {builtArea} sqft.
NO. OF FLOOR - {numFloors}
PLOT ADDRESS - {plotAddress}
PROJECT DESCRIPTION - {projectDescriptions}
SERVICES - {services}

Your estimated project cost is {projectCost} Rs.
Payable amount 25% (approx.) {minAmount} Rs.

Regards
BUILD-EASY ASSOCIATES""".format(name=name,phone=phone,email=email,address=address,plotSize=plotSize,builtArea=approxPlotSize,numFloors=numFloor,plotAddress=plotAddress,projectDescriptions=proDescription,services=servicesText,projectCost=estimateCost,minAmount=int(estimateCost)*0.25)

        send_mail(str(name)+" - Updated Quotation",str(msg),"buildeasy01@gmail.com",[str(email),"buildeasy01@gmail.com"])
        email = SendEmail.objects.create(client=client,title="New Quotation",msg=str(msg))
        email.save()

    try:
        client = ClientInfo.objects.get(id=id)
        # serviceOpted = client.serviceOpted.all()
        # print(serviceOpted)
    except:
        return redirect(pageNotFound,param="Client",permanent=True)  
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
    post = False
    if request.method == 'POST':
        id = request.POST["id"]
        mail = RecEmail.objects.get(id=id)
        sub = request.POST["subject"]
        msg = request.POST["msg"]
        send_mail(str(sub),str(msg),"buildeasy01@gmail.com",[str(mail.email)])
        post = True
    receiveMails = RecEmail.objects.all()
    sendMails = SendEmail.objects.all()
    return render(request,'userPage/emailQueries.html',{"rmail":receiveMails,"smail":sendMails,"post":post})

def updateVar(request):  
    if request.method == "POST":
        id = request.POST["id"]
        yoe = request.POST["YOE"]
        totalProjects = request.POST["totalProjects"]
        totalEmployees = request.POST["totalEmployees"]
        totalClients = request.POST["totalClients"]
        totalPartners = request.POST["totalPartners"]
        totalCities = request.POST["totalCities"]
        totalArea = request.POST["totalArea"]
        PAC = request.POST["PAC"]
        IAC = request.POST["IAC"]
        BAC = request.POST["BAC"]
        BACS = request.POST["BACS"]
        yt1 = request.POST["ytLink1"]
        yt2 = request.POST["ytLink2"]
        variables = UpdateVariable.objects.get(id=id)

        variables.YOE=yoe
        variables.totalProjects=totalProjects
        variables.totalEmployees=totalEmployees
        variables.totalClients=totalClients
        variables.totalPartners=totalPartners
        variables.totalCities=totalCities
        variables.totalArea=totalArea
        variables.PAC=PAC
        variables.IAC=IAC
        variables.BAC=BAC
        variables.BACS=BACS
        variables.yt1=yt1
        variables.yt2=yt2
        
        variables.save()
    variables = UpdateVariable.objects.all()
    if variables:
        variables = variables[0]    
    return render(request,'userPage/updateVariables.html',{'var':variables})    

def genratePdf(request,id):
    try:
        client = ClientInfo.objects.get(id=id)
        workPost = WorkPost.objects.get(client=client)
        posts = Post.objects.filter(workPost=workPost)
    except:
        return redirect(pageNotFound,param="Client",permanent=True)    
    return render(request,'userPage/genratePdf.html',{'client':client,'workPost':workPost,'posts':posts})       

def pageNotFound(request,param):
    return render(request,'userPage/NotFound.html',{'param':param})   

def rRead(request,id):
    mail = RecEmail.objects.get(id=id)
    mail.read = True
    mail.save()
    return JsonResponse("received",safe=False)

def sRead(request,id):
    mail = SendEmail.objects.get(id=id)
    mail.read = True
    mail.save()
    return JsonResponse("sent",safe=False)         