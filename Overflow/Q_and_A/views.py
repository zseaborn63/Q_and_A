from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView, CreateView, ListView, DetailView, View
from Q_and_A.models import Question, Answer, Tag, Profile, Vote


class WelcomeView(TemplateView):
    template_name = 'welcome.html'


class UserCreate(CreateView):
    model = User
    success_url = "/accounts/login"
    form_class = UserCreationForm


class QuestionListView(ListView):
    model = Question


class QuestionDetailView(DetailView):
    model = Question

    def get_queryset(self):
        question_id = self.kwargs.get("pk")
        return self.model.objects.filter(id=question_id)


class CreateQuestionView(CreateView):
    model = Question
    fields = ['title', 'body', 'tags']
    success_url = '/'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.asker = self.request.user
        return super().form_valid(form)


class QuestionCreation(TemplateView):

    template_name = 'questioncreation.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionCreation, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class MakeQuestion(View):

    def post(self, request):
        title = request.POST.get('title')
        body = request.POST.get('body')
        tags = request.POST.getlist('tags')
        question = Question.objects.create(asker=request.user, title=title, body=body)
        for tag in tags:
            question.tags.add(tag)
        question.save()
        return HttpResponseRedirect(reverse('welcome'))


class CreateAnswerView(CreateView):
    model = Answer
    fields = ['body']
    success_url = '/questions/'

    #def form_valid(self, form,):
    #    model = form.save(commit=False)
    #    model.answerer = self.request.user
    #    model.question_answered = Question.objects.get(id="pk")
    #    return super().form_valid(form)

    def post(self, request, pk):
        question_answered = Question.objects.get(id=pk)
        body = request.POST.get('body')
        Answer.objects.create(question_answered=question_answered, answerer=request.user, body=body)
        return HttpResponseRedirect(reverse('question_list'))


class ProfileDetailView(DetailView):
    model = Profile

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        return self.model.objects.filter(user__id=user_id)


class UpVote(View):

    def post(self, request, answer_id):
        answer = Answer.objects.get(id=answer_id)
        Vote.objects.create(type='up', voter=request.user, answer_voted=answer)
        return HttpResponseRedirect(reverse('question_detail', kwargs={"pk": answer.question_answered.id}))


class DownVote(View):

    def post(self, request, answer_id):
        answer = Answer.objects.get(id=answer_id)
        Vote.objects.create(type='down', voter=request.user, answer_voted=answer)
        return HttpResponseRedirect(reverse('question_detail', kwargs={"pk": answer.question_answered.id}))


class TagListView(ListView):
    model = Tag


class TagDetailView(DetailView):
    model = Tag

    def get_queryset(self):
        tag_id = self.kwargs.get("pk")
        return self.model.objects.filter(id=tag_id)

