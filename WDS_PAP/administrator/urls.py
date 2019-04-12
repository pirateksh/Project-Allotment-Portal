from django.urls import path
from administrator import views


urlpatterns = [
    path('entry/', views.home, name="Entry"),
    path('leader_login/', views.home, name="Leader Login"),
    path('student_login/', views.home, name="Student Login"),
    path('admin_login/', views.home, name="Admin Login"),
    # Test
    path('admin_login_error/<str:username>', views.admin_login_error, name="Admin Login Error"),
    path('admin_home/<str:username>/returned', views.dummy_admin_home, name="Dummy Admin Home"),
    # Test over
    path('admin_home/<str:username>', views.admin_home, name="Admin Home"),
    path('register_gate/', views.register_gate, name="Register Gate"),
    path('register_admin', views.register_admin, name="Register Admin"),
    path('stu_pass_set/<str:username>', views.stu_pass_set, name="Default student password"),
    path('lead_allot/<str:username>', views.lead_allot, name="Leader Allotment"),
    path('assign_mentor_round_1/<str:username>', views.assign_mentor_round_1, name="Assign Mentor Round 1"),
    path('assign_mentor_round_2/<str:username>', views.assign_mentor_round_2, name="Assign Mentor Round 2"),
    path('assign_mentor_round_3/<str:username>', views.assign_mentor_round_3, name="Assign Mentor Round 3"),

]
