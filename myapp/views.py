from django.shortcuts import render

from .models import QuestionTopic, QuestionSubTopic , Question
# Create your views here.
from django.http import HttpResponse


def dashboard(request):
    dict = {}
    if request.POST.get("topic") is None:
        topics = QuestionTopic.objects.all()
        dict['topics_list'] = topics
        dict['sub_topic'] = False
    else:
        topics = QuestionTopic.objects.all()
        dict['topics_list'] = topics
        topic_id = request.POST.get("topic")
        topic = QuestionTopic.objects.get(id=topic_id)

        sub_topic_list = topic.questionsubtopic_set.all()
        dict['sub_topics_list'] = sub_topic_list
        dict['sub_topic'] = True
    return render(request, 'myapp/dashboard.html', dict)

def questions_list(request):
    dict = {}
    sub_topic_id = request.POST.get("sub_topic")

    difficulty_level = request.POST.get("difficulty_level")
    print(sub_topic_id)
    print difficulty_level
    print(type(difficulty_level))

    if difficulty_level is None or \
            int(difficulty_level) is 4:
        print("here")
        question_list = Question.objects.filter(sub_topic_id=sub_topic_id).order_by('-num_of_times_asked')

    else:
        print("there")
        question_list = Question.objects.filter(sub_topic_id=sub_topic_id,
                                                difficulty_level=difficulty_level).order_by('-num_of_times_asked')


    print(questions_list)

    dict["question_list"] = question_list
    dict["sub_topic"] = sub_topic_id

    return render(request, 'myapp/questions.html', dict)

def question_response(request, qid):
    return HttpResponse("view question response: " + qid)