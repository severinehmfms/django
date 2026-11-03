import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        date_locale = timezone.localtime(self.pub_date)
        return self.question_text[:20] + " - " + date_locale.strftime("%d/%m/%Y à %Hh%M")

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def age(self):
        return timezone.now() - self.pub_date

    def get_choices(self):
        return self.choice_set.all()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text[:20]