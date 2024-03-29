from . import views
from django.urls import path

urlpatterns = [
    path('',views.userHome,name="userHome"),
    path('quoteResponse/',views.quoteResponse,name="quoteResponse"),
    path('userProjects/',views.userProjects,name="userProjects"),
    path('userAbout/',views.userAbout,name="userAbout"),
    path('userServices/',views.userServices,name="userServices"),
    path('userContact/',views.userContact,name="userContact"),
    path('userToken/',views.userToken,name="userToken"),
    path('userPost/<int:id>',views.userPost,name="userPost"),
    path('adminPage/',views.adminPage,name="adminPage"),
    path('clientPage/',views.clientPage,name="clientPage"),
    path('verifyClients/',views.verifyClients,name="verifyClients"),
    path('clientInfo/<int:id>',views.clientInfo,name="clientInfo"),
    path('servicePage/',views.servicePage,name="servicePage"),
    path('projects/',views.projects,name="projects"),
    path('project/<int:id>',views.project,name="project"),
    path('postUpload/<int:id>',views.postUpload,name="postUpload"),
    path('postUpload/',views.postUpload,name="postUpload"),
    path('pastProjects/',views.pastProjects,name="pastProjects"),
    path('ongoingProjects/',views.ongoingProjects,name="ongoingProjects"),
    path('upcomingProjects/',views.upcomingProjects,name="upcomingProjects"),
    path('recentPosts/',views.recentPosts,name="recentPosts"),
    path('tokenSearch/',views.tokenSearch,name="tokenSearch"),
    path('updateWebsite/',views.updateWebsite,name="updateWebsite"),
    path('updateTeams/',views.updateTeams,name="updateTeams"),
    path('updateClientInfo/<int:id>',views.updateClientInfo,name="updateClientInfo"),
    path('emailQueries/',views.emailQueries,name="emailQueries"),
    path('updateVariables/',views.updateVar,name="updateVariables"),
    path('genratePdf/<int:id>',views.genratePdf,name="genratePdf"),
    path('notFound/<str:param>',views.pageNotFound,name="notFound"),
    path('rRead/<int:id>',views.rRead,name="rRead"),
    path('sRead/<int:id>',views.sRead,name="sRead")
]
