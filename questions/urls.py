from django.urls import path
from . import views


app_name = 'questions'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('detail/<int:question_id>/', views.QuestionDetailView.as_view(), name='QustionDetail'),
	path('form/', views.QuestionFromView.as_view(), name='QuestionFrom'),
	path('post/question', views.PostQuestion, name='PostQuestion'),
	path('post/answer/<int:question_id>', views.PostAnswer, name='PostAnswer'),
	path('vote/question/<int:question_id>', views.VoteQuestion, name='VoteQuestion'),
	path('vote/answer/<int:answer_id>', views.VoteAnswer, name='VoteAnswer'),
	path('solve/<int:question_id>', views.Solve, name='solve'),
	path('user/<str:username>', views.ProfileDetailView.as_view(), name='ProfileDetail'),
]
