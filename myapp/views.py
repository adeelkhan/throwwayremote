from django.shortcuts import render
from .models import QuestionTopic, QuestionSubTopic, Question
from django.utils import timezone


from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout


@login_required(login_url="/view_login")
def dashboard(request):
    dict = {}

    # topic is already selected by user
    if request.POST.get("topic") is None:
        topics = QuestionTopic.objects.all()
        dict['topics_list'] = topics
        dict['sub_topic'] = False
    else:
        # first time accessing dashboard
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

    dict = {}
    sub_topic_id = request.POST.get("sub_topic")
    difficulty_level = request.POST.get("difficulty_level")
    print(sub_topic_id)
    print difficulty_level
    print(type(difficulty_level))

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

    dict = {}
    question = Question.objects.get(id=qid)
    dict["question"] = question

    return render(request, 'myapp/question_response.html', dict)


@login_required(login_url="/view_login")
def save_response(request,qid):

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
    if int(rating) is not rating_choice['Not Answered']:
        question.num_of_times_answered += 1

    question.answer_ratings = int(rating)
    question.num_of_times_asked += 1
    question.response_at = timezone.now()
    question.response_given_by = request.user.username
    question.comments = comments
    question.save()


    print(question.sub_topic.id)

    sub_topic_id = question.sub_topic.id
    question_list = Question.objects.filter(sub_topic_id = sub_topic_id).\
                                            order_by('-num_of_times_asked')

    return render(request, 'myapp/questions.html', {
        'response_saved': True,     # for successful msg response
        'sub_topic': sub_topic_id,
        'question_list': question_list
    })


@login_required(login_url="/view_login")
def user_dashboard(request):
    return render(request,'myapp/dashboard.html',{})

def view_login(request):
    return render_to_response('myapp/view_login.html', {},
                                RequestContext(request))

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return render(request, 'myapp/logout.html', {})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'auth_app/view_login.html', {})

@login_required(login_url="/view_login")
def user_logout(request):
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/view_login/')

def user_signup(request):
    return HttpResponse("signup.")

# Create your views here.
