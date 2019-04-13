from django.urls import path
from prof_add import views


urlpatterns = [
    path('yes_no/', views.prof_add_or_not, name="Yes_or_no"),
    path('prof_entry/<str:username>/', views.professor, name="add_prof"),
]
