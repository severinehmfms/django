from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice


# Create your views here.

#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

#def index(request):
#    latest_question_list = Question.objects.order_by("-pub_date")[:5]
#    output = ", ".join([q.question_text for q in latest_question_list])
#    return HttpResponse(output)

'''
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    # template = loader.get_template("polls/index.html")
    # return HttpResponse(template.render(context, request))
    # Raccourci pour les deux dernières lignes commentées :
    return render(request, "polls/index.html", context)'''

#def detail(request, question_id):
#    return HttpResponse("You're looking at question %s." % question_id)

#En gérant l'erreur 404 si la question n'existe pas
"""def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})"""

# On remplace les vues par des génériques
'''
#En gérant l'erreur 404 si la question n'existe pas en utilisant Un raccourci : get_object_or_404()
#Pour info : Il y a aussi une fonction get_list_or_404(), qui fonctionne comme get_object_or_404(), sauf qu’elle utilise filter() au lieu de la méthode get(). Elle lève une exception Http404 si la liste est vide.
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
'''

# Vues génériques
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        #On récupère le choix correspondant à celui envoyé par le formulaire (donc le choix de l'utilisateur)
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return \
            (
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
