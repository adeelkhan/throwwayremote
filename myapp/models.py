from django.db import models

# Create your models here.


class QuestionTopic(models.Model):

    topic_text = models.CharField(max_length=200)
    additional_info = models.CharField(max_length=200)

    def __str__(self):
        return self.topic_text


class QuestionSubTopic(models.Model):

    topic = models.ForeignKey(QuestionTopic,default = None)
    subtopic_text = models.CharField(max_length=200, default="NA")

    def __str__(self):
        return self.subtopic_text

class Question(models.Model):
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

    comments = models.CharField(max_length=200)
    reviewer_votes = models.IntegerField(default=0)
    answer_ratings = models.CharField(max_length=1, choices=RATINGS)
    created_at = models.DateTimeField('created at')

    def __str__(self):
        return self.question_text
