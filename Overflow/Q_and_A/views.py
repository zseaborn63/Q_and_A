from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView, CreateView, ListView, DetailView, View
from Q_and_A.models import Question


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