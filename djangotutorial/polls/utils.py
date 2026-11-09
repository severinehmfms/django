from django.db.models import Sum
from .models import Question, Choice

def minimax():
    questions = Question.objects.all()

    minimum = maximum = (questions[0], 0)

    for q in questions:
        n = q.choice_set.aggregate(sum=Sum('votes'))['sum'] or 0

        if n > maximum[1]:
            maximum = (q, n)

        if n < minimum[1]:
            minimum = (q, n)

    return (minimum[0], maximum[0])