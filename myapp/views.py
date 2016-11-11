from django.shortcuts import render
from .models import QuestionTopic, QuestionSubTopic, Question
from .models import QuestionResponse
from django.utils import timezone

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout


@login_required(login_url="/view_login")
def view_dashboard(request):

    """
    Enable user to view dashboard. Handles both functionality of listing
    topics and subtopics

    :param request:
    :return None:

    """
    dict = {}

    # first time accessing list only Topics
    if request.POST.get("topic") is None:
        topics = QuestionTopic.objects.all()
        dict['topics_list'] = topics
        dict['sub_topic'] = False
    else:
        # list both topics and subtopics
        topics = QuestionTopic.objects.all()
        dict['topics_list'] = topics

        topic_id = request.POST.get("topic")
        topic = QuestionTopic.objects.get(id=topic_id)
        sub_topic_list = topic.questionsubtopic_set.all()

        dict['sub_topics_list'] = sub_topic_list
        dict['sub_topic'] = True
    return render(request, 'myapp/dashboard.html', dict)


@login_required(login_url="/view_login")
def questions_list(request):
    """
    Enable user to view questions for a sub topic.

    :param request:
    :return None:

    """
    dict = {}

    sub_topic_id=1
    if request.POST.get("sub_topic") is not None:
        sub_topic_id = request.POST.get("sub_topic")
    elif request.GET.get("sub_topic") is not None:
        sub_topic_id = request.GET.get("sub_topic")

    difficulty_level = request.POST.get("difficulty_level")

    # Show all when no difficulty filter applied
    if difficulty_level is None or \
                    int(difficulty_level) is 4:
        question_list = Question.objects.filter(
            sub_topic_id=sub_topic_id) \
            .order_by('-num_of_times_asked')

    # apply a filter based on difficulty
    else:
        question_list = Question.objects.filter(
            sub_topic_id=sub_topic_id,
            difficulty_level=difficulty_level
        ).order_by('-num_of_times_asked')
    dict["question_list"] = question_list
    dict["sub_topic"] = sub_topic_id

    return render(request, 'myapp/questions.html', dict)


@login_required(login_url="/view_login")
def question_response(request, qid):
    """
    Enable user to view response page for a question

    :param request: http request object
            qid: question id for the question selected by user
    :return None:

    """

    dict = {}
    question = Question.objects.get(id=qid)
    dict["question"] = question
    dict["sub_topic"] = question.sub_topic.id

    return render(request, 'myapp/question_response.html', dict)


@login_required(login_url="/view_login")
def save_response(request, qid):
    """
    Enable user to save his/her response for a question

    :param request: http request object
            qid: question id for the question selected by user
    :return None:

    """

    rating_choice = {
        'Not Answered': 1,
        'Bad': 2,
        'Satisfactory': 3,
        'Good': 4,
        'Excellent': 5
    }

    rating = request.POST.get("ratings")
    comments = request.POST.get("comments")

    question = Question.objects.get(id=qid)
    question_response = QuestionResponse(question_id = qid,
                                         answer_ratings=int(rating),
                                         response_at=timezone.now(),
                                         response_given_by=request.user.username,
                                         comments=comments)

    if int(rating) is not rating_choice['Not Answered']:
        question.num_of_times_answered += 1
    question.num_of_times_asked += 1

    question_response.save()
    question.save()

    sub_topic_id = question.sub_topic.id
    question_list = Question.objects.filter(sub_topic_id=sub_topic_id). \
        order_by('-num_of_times_asked')

    return render(request, 'myapp/questions.html', {
        'response_saved': True,  # for successful msg response
        'sub_topic': sub_topic_id,
        'question_list': question_list
    })

@login_required(login_url="/view_login")
def view_question_responses(request, qid):
    """
    Enable user to view all responses for a question

    :param request: http request object
            qid: question id for the question selected by user
    :return None:

    """

    sub_topic_id = request.GET.get("sub_topic")
    #print(sub_topic_id)

    rating_choice = ['',
                     'Not Answered',
                     'Bad',
                     'Satisfactory',
                     'Good',
                     'Excellent'
                     ]
    question_responses = QuestionResponse.objects.filter(question_id=qid)

    dict = {}

    q = Question.objects.get(id = qid)
    #print q
    #q = question_response[0]
    print "sub_topic is:" + str(q.sub_topic_id)

    dict['ratings'] = rating_choice
    dict["question_response_list"] = question_responses
    dict["sub_topic"] = sub_topic_id

    return render(request, 'myapp/view_question_responses.html', dict)

@login_required(login_url="/view_login")
def user_dashboard(request):
    """
    Enable user to view dashboard page

    :param request: request object having values
    :return None:
    """

    return render(request, 'myapp/dashboard.html', {})

def view_login(request):
    """
    Enable user to view login page

    :param request: request object having values
    :return None:
    """

    return render_to_response('myapp/view_login.html', {},
                              RequestContext(request))


def user_login(request):
    """
    This view authenticate user for a username, password

    :param request: request object having values
    :return None:
    """

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return render(request, 'myapp/logout.html', {})

    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'auth_app/view_login.html', {})


@login_required(login_url="/view_login")
def user_logout(request):
    """
    Enable user to logout from app

    :param request: request object having values
    :return None:
    """
    logout(request)
    # Take the user back to login.
    return HttpResponseRedirect('/view_login/')

def user_signup(request):
    """
    Enable user signup to app

    :param request: request object having values
    :return None:
    """
    return HttpResponse("signup.")


