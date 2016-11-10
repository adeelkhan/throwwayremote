from django.db import models
from django.utils import timezone


# Create your models here.


class QuestionTopic(models.Model):
    """ This would represent Major Topics for Questions """

    topic_text = models.CharField(max_length=200)
    additional_info = models.CharField(max_length=200)

    def __str__(self):
        return self.topic_text


class QuestionSubTopic(models.Model):
    """ This would keep track of sub Topics inside Major Topics """

    topic = models.ForeignKey(QuestionTopic, default=None)
    subtopic_text = models.CharField(max_length=200, default="NA")

    def __str__(self):
        return self.subtopic_text


class Question(models.Model):
    """ This would represent Questions """

    RATINGS = (
        ('1', 'Not Answered'),
        ('2', 'Bad'),
        ('3', 'Satisfactory'),
        ('4', 'Good'),
        ('5', 'Excellent'),
    )

    sub_topic = models.ForeignKey(QuestionSubTopic, default=None)
    question_text = models.CharField(max_length=200)
    difficulty_level = models.IntegerField(default=0)
    solution = models.CharField(max_length=200)

    num_of_times_asked = models.IntegerField(default=0)
    num_of_times_answered = models.IntegerField(default=0)

    comments = models.CharField(max_length=500)
    reviewer_votes = models.IntegerField(default=0)
    answer_ratings = models.CharField(max_length=1, choices=RATINGS)

    created_at = models.DateTimeField('created at')
    response_given_by = models.CharField(max_length=50, default="NA")
    response_at = models.DateTimeField('response at', default=timezone.now())

    def __str__(self):
        return self.question_text
