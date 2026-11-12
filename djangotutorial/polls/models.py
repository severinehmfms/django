import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.db.models import Sum

MAX_LENGTH = 20

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        date_locale = timezone.localtime(self.pub_date)
        return self.question_text[:20] + " - " + date_locale.strftime("%d/%m/%Y à %Hh%M")

    def __repr__(self): return "<Question: {}>".format(self.question_text)

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )

    def was_published_recently(self):
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def age(self):
        return timezone.now() - self.pub_date

    def get_choices(self):
        choices = self.choice_set.all()
        resultat = self.choice_set.aggregate(total=Sum('votes'))
        total = resultat['total']
        #return [(c.choice_text, c.votes, c.votes / total * 100 ) for c in choices]
        return [(c.choice_text, c.votes, (c.votes / total * 100) if total > 0 else 0) for c in choices]

    def get_max_choice(self):
        choices = self.choice_set.all()
        resultat = self.choice_set.aggregate(total=Sum('votes'))
        total = resultat['total']
        max_choice = max(choices, key=lambda c: c.votes / total)
        return (max_choice.choice_text, (max_choice.votes / total) if total > 0 else 0)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text[:20]