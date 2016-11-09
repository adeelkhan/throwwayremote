from django.contrib import admin

# Register your models here.

from .models import  QuestionTopic, QuestionSubTopic,  Question

admin.site.register(QuestionTopic)
admin.site.register(QuestionSubTopic)
admin.site.register(Question)

