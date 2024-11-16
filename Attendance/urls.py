from django.urls import path
from Attendance import views

app_name="Attendance"

urlpatterns=[path('',views.home,name="home"),
path('Reports/',views.Report,name="Report"),
path('Login/',views.loginuser,name="Login"),
path('ManageStudents/',views.manageStudents,name="manage"),
path('LogOut/',views.logoutUser,name="logout"),
path('LoginStudent/',views.loginStudent,name="StudLogin"),
path('MarkAttendance/',views.markattendance,name="MarkAttendance")]