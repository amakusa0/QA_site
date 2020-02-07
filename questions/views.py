from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Answer, Profile
from .forms import AnswerForm, QuestionForm

from django.shortcuts import get_object_or_404

class IndexView(generic.TemplateView):
    template_name = 'questions/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_form'] = QuestionForm()
        context['unsolved_questions'] = Question.objects.filter(isSolved=False).order_by('pub_date')
        context['solved_questions'] = Question.objects.filter(isSolved=True).order_by('pub_date')
        return context


class QuestionDetailView(generic.TemplateView):
    template_name = 'questions/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs['question_id']
        context['question'] = get_object_or_404(Question, pk=question_id)
        context['answers'] = Answer.objects.filter(question__id=question_id)
        context['answer_form'] = AnswerForm()
        return context



class ProfileDetailView(generic.TemplateView):
    template_name = 'questions/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        context['profile'] = get_object_or_404(Profile, user__username=username)
        context['questions'] = Question.objects.filter(username=username).order_by('pub_date')
        context['answers'] = Answer.objects.filter(username=username).order_by('pub_date')
        return context



class QuestionFromView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'questions/question_form.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_form'] = QuestionForm()
        return context


@login_required
def PostAnswer(request, question_id):
    form = AnswerForm(request.POST)
    question = get_object_or_404(Question, pk=question_id)
    if form.is_valid():
        answer = Answer(
            question=question,
            username=request.user,
            text=form.cleaned_data['text'],
        )
        answer.save()
        question.numAnswer += 1
        question.save()

    return HttpResponseRedirect(reverse('questions:QustionDetail', args=(question_id, )))



@login_required
def PostQuestion(request):
    form = QuestionForm(request.POST)
    if form.is_valid():
        question = Question(
            title=form.cleaned_data['title'],
            text=form.cleaned_data['text'],
            username=request.user,
        )
        question.save()
    return HttpResponseRedirect(reverse('questions:index', args=()))




@login_required
def VoteAnswer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    user = User.objects.get(username=answer.username)
    profile = Profile.objects.get(user=user)
    if answer.username != request.user.username:
        answer.votes += 1
        profile.answer_votes += 1
        answer.save()
        profile.save()
    return HttpResponseRedirect(reverse('questions:QustionDetail', args=(answer.question.id, )))




@login_required
def VoteQuestion(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = User.objects.get(username=question.username)
    profile = Profile.objects.get(user=user)
    if question.username != request.user.username:
        question.votes += 1
        profile.question_votes += 1
        question.save()
        profile.save()
    return HttpResponseRedirect(reverse('questions:QustionDetail', args=(question_id, )))



@login_required
def Solve(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.username == request.user.username:
        question.isSolved = True
        question.save()
    return HttpResponseRedirect(reverse('questions:QustionDetail', args=(question_id, )))





