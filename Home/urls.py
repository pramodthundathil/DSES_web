from django.urls import path 
from .import views 

urlpatterns = [

    path("",views.Index,name="Index"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignIn",views.SignIn,name="SignIn"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("Gallery",views.Gallery,name="Gallery"),
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),
    path("Users",views.Users,name="Users"),
    path("Gallery_admin",views.Gallery_admin,name="Gallery_admin"),
    path("Membersingleview/<int:pk>",views.Membersingleview,name="Membersingleview"),
    path("MemberSingleProfile",views.MemberSingleProfile,name="MemberSingleProfile"),
    path("Registration_confirmation/<int:pk>",views.Registration_confirmation,name="Registration_confirmation"),
    path("delete_gallery/<int:pk>",views.delete_gallery,name="delete_gallery"),
    path("Disable_user/<int:pk>",views.Disable_user,name="Disable_user"),
    path("IssueIdCard/<int:pk>",views.IssueIdCard,name="IssueIdCard"),
    path("DESS_INFO",views.DESS_INFO,name="DESS_INFO"),
    path("Active_members_list",views.Active_members_list,name="Active_members_list"),
    path("Inctive_members_list",views.Inctive_members_list,name="Inctive_members_list"),
    path("Messageing",views.Messageing,name="Messageing"),
]   