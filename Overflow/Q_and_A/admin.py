from django.contrib import admin

# Register your models here.
from Q_and_A.models import Profile, Question, Answer, Tag, Vote

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Vote)