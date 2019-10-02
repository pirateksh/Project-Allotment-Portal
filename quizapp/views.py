from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core import serializers # to update the Page by sending queryset 
from .models import Quiz,Question,Option,Answer
from django.contrib.auth.models import User 
from .forms import QuizCreationForm,QuestionCreationForm,OptionCreationForm,AnswerCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
@login_required
def quiz_home(request):
	quizes = Quiz.objects.all()
	return render(request,'quizapp/quiz_home.html',{'quizes':quizes})


def quiz_view(request):
	quiz1 = Quiz.objects.all().first()
	questions = Question.objects.all() #return Query Set i.e. <QuerySet [<Question: Question object (1)>, <Question: Question object (2)>]>
	options = Option.objects.all() 
	answers = Answer.objects.all()
	# for question in questions:
		# print(question.option1)
	print(answers)
	return render(request,'quizapp/quiz.html',{'quiz1':quiz1,'questions':questions,'options':options,'answers':answers})
@login_required
def take_quiz_view(request):
	return render(request,"quizapp/take_quiz_vish.html") 

@staff_member_required
def create_quiz(request):
	if request.method == 'POST':
		form = QuizCreationForm(request.POST)
		form.instance.instructions = request.POST.get('instr') #i.e. get('name_attribute')
		form.instance.author = request.user
		if form.is_valid():
			form.save()
			# messages.success(request,f'Commeted Successfully!')
		# redirect(request.path_info)
			return redirect("create_questions")
		else:
			if form.errors:
				for field in form:
					for error in field.errors:
						print(error)
			return HttpResponse("Something Bad Just Happend")
	else:
		form = QuizCreationForm()
		context = {
			'form':form
		}
		return render(request,"quizapp/create_quiz.html",context)

@staff_member_required
def create_questions(request):
	if request.method == 'POST':
		# print(request.POST)
		quiz = Quiz.objects.all().last()
		que_obj = Question.objects.create(
			quiz = quiz,
			question = request.POST['question']
		)
		opt_obj = Option.objects.create(
			quiz = quiz,
			question = Question.objects.all().last(),
			option1 = request.POST['option1'],
			option2 = request.POST['option2'],
			option3 = request.POST['option3'],
			option4 = request.POST['option4']
		)
		ans_obj = Answer.objects.create(
			quiz = quiz,
			question = Question.objects.all().last(),
			corr_answer = request.POST.get('corr_answer',False),#to handle multivalue dictionary error
			extra_info = request.POST['extra_info']	
		)
		# TO send back whatever we have created using JsonResponse
		# question = {'question':que_obj.question}
		data={
			'question' : que_obj.question,
			'que_cnt' : Question.objects.all().filter(quiz=quiz).count(),
			'ques_id' :  Question.objects.all().last().id
		}
		return JsonResponse(data)

	else:
		form_que = QuestionCreationForm()
		form_opt = OptionCreationForm()
		form_ans = AnswerCreationForm()
		quiz = Quiz.objects.all().last()
		questions = Question.objects.all().filter(quiz = quiz) # using quiz = quiz.title gives inavlid literal error.
		que_cnt = questions.count()
		return render(request,"quizapp/create_questions.html",{'quiz':quiz,'questions':questions,'form_que':form_que,
															'form_opt':form_opt,'form_ans':form_ans,'que_cnt':que_cnt})
''' THIS CODE WORKS PERFECTLY FINE BUT FOR AJAXIFYING Create Questions we don't use it.
	# if request.method == 'POST':
	# 	form_que = QuestionCreationForm(request.POST)
	# 	curr_quiz = Quiz.objects.all().last()
	# 	form_que.instance.quiz = curr_quiz
	# 	if form_que.is_valid():
	# 		form_que.save()
	# 	form_opt = OptionCreationForm(request.POST)
	# 	form_ans = AnswerCreationForm(request.POST)
	# 	form_opt.instance.quiz = curr_quiz
	# 	form_ans.instance.quiz = curr_quiz
	# 	curr_que = Question.objects.all().last()
	# 	form_opt.instance.question = curr_que 
	# 	form_ans.instance.question = curr_que 
	# 	print(request.POST)
	# 	form_ans.instance.corr_answer = request.POST['correct_one']
	# 	if form_opt.is_valid() and form_ans.is_valid():
	# 		form_opt.save()
	# 		form_ans.save()
	# 		return HttpResponse("Question Addded Successfully")
	# 	else:
	# 		if form_ans.errors:
	# 			for field in form_ans:
	# 				for error in field.errors:
	# 					print(error)
	# 		return HttpResponse("Question NOT Addded Successfully")
'''
def ques_detail_view(request,pk):
	if request.method == 'POST':
		question = Question.objects.all().filter(id=pk)
		question_res = serializers.serialize('json', question)
		options = Option.objects.all().filter(question=question.first())
		options_res = serializers.serialize('json', options)
		answer = Answer.objects.all().filter(question=question.first())
		answer_res = serializers.serialize('json', answer)
		data={
			'question' : question_res,
			'options' : options_res,
			'answer' : answer_res
		}

		# return HttpResponse(options_res, content_type="text/json-comment-filtered")
		'''
		e.g. [{"model": "quizapp.question", "pk": 115, "fields": {"quiz": 18, "question": "Question from Quiz 4"}}]
		'''
		return JsonResponse(data)
		# print(question)
		# options  = Option.objects.all().filter(question=)
		# return HttpResponse("Hola")
