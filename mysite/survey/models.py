import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'

    QUESTION_TYPES = (
        (TEXT, 'Text'),
        (RADIO, 'Radio')
    )

    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=RADIO)
    
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class UserResponse(models.Model):

    user = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200, null=True)

    def __str__(self):
        return '{}'.format(self.user)
