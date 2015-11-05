from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, CreateView, ListView
from Q_and_A.models import Question


class WelcomeView(TemplateView):
    template_name = 'welcome.html'

class UserCreate(CreateView):
    model = User
    success_url = "/accounts/login"
    form_class = UserCreationForm

class QuestionListView(ListView):
    model = Question

