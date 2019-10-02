from django.urls import path
from .import views as quizapp_views 
urlpatterns = [
    path('newhome/quiz_home',quizapp_views.quiz_home,name="quiz_home"),
	path('newhome/quiz',quizapp_views.quiz_view,name="take_quiz"),
	path('newhome/create_quiz',quizapp_views.create_quiz,name="create_quiz"),
	path('newhome/create_quiz/questions/',quizapp_views.create_questions,name="create_questions"),
	path('newhome/take_quiz/',quizapp_views.take_quiz_view,name="take_quiz_vish"),
	path('newhome/create_quiz/questions/<int:pk>/',quizapp_views.ques_detail_view,name="ques_detail"),
]