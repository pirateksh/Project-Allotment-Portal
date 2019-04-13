from django.urls import path
from lead_allot import views

urlpatterns = [
    path('leader_home/<str:lead_reg_no>', views.leader_home, name="Leader Home"),
    path('student_home/<str:stu_reg_no>', views.student_home, name="Student Home"),
    path('lead_change_password/<str:lead_reg_no>/', views.lead_change_password, name="Leader Change Password"),
    path('student_change_password/<str:stu_reg_no>/', views.stu_change_password, name="Student Change Password"),
    path('invite/<str:lead_reg_no>/<str:stu_reg_no>/', views.invite, name="Invite students"),
    path('preference/<str:lead_reg_no>/', views.preference, name="Preference set"),
    path('accept_invite/<str:lead_reg_no>/<str:stu_reg_no>/', views.accept_invite, name="Accept invite"),
    path('returned/<str:lead_reg_no>/', views.returned_lead, name="Return to Leader Home"),
]
