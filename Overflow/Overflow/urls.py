"""Overflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth.decorators import login_required
from Q_and_A.views import WelcomeView, UserCreate, QuestionListView, CreateQuestionView, QuestionCreation, QuestionDetailView,\
    MakeQuestion, CreateAnswerView, ProfileDetailView, UpVote, DownVote, TagListView, TagDetailView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', WelcomeView.as_view(), name='welcome'),
    url(r'^create_user/$', UserCreate.as_view(), name='create_user'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^questions/$', QuestionListView.as_view(), name='question_list'),
    url(r'questions/(?P<pk>\d+)/$', QuestionDetailView.as_view(), name='question_detail'),
    url(r'^create_question/$', login_required(QuestionCreation.as_view()), name='create_question'),
    url(r'^make_question/$', login_required(MakeQuestion.as_view()), name='make_question'),
    url(r'^make_answer/(?P<pk>\d+)/$', login_required(CreateAnswerView.as_view()), name='create_answer'),
    url(r'^profile/(?P<pk>\d+)/$', login_required(ProfileDetailView.as_view()), name='user_profile'),
    url(r'^upvote/(?P<answer_id>\d+)/$', UpVote.as_view(), name="upvote"),
    url(r'^downvote/(?P<answer_id>\d+)/$', DownVote.as_view(), name="downvote"),
    url(r'^tags/$', TagListView.as_view(), name='tag_list'),
    url(r'^tags/(?P<pk>\d+)/$', TagDetailView.as_view(), name='tag_detail')

]
