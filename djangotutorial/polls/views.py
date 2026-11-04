from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import Sum
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

class AllView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")


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

def frequency(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    #Pour chacun des choix on va récupérer le nombre de votes, et max_choice
    choices = question.get_choices();
    print(choices);
    return render(request,
                  "polls/frequency.html",
                  {"question": question,
                        "choices": choices
                   }
                  )
def statistics(request):
    question_list = Question.objects.order_by("-pub_date")

    # On va récupérer les informations qu'on souhaite ensuite afficher
    # le nombre total de sondage enregistrés
    nb_sondages = question_list.count()
    nb_sondagesbis = Question.objects.count()

    # le nombre total de choix possibles
    nb_total_choices = Choice.objects.count()

    # le nombre total de votes (voir aide pdf)
    nb_total_votes = Choice.objects.aggregate(Sum("votes"))

    # la moyenne du nombre de votes par sondage


    # [optionnel] la question la plus populaire

    # [optionnel] la question la moins populaire

    # la dernière question enregistrée

    # On va implanter ces informations dans le context qui sera ensuite envoyé au gabarit
    statistics_dict = {
        "nb_sondages": nb_sondagesbis,
        "nb_total_choices": nb_total_choices,
        "nb_total_votes": nb_total_votes
    }

    context = {"question_list": question_list,
                "statistics_dict": statistics_dict

               }
    # template = loader.get_template("polls/index.html")
    # return HttpResponse(template.render(context, request))
    # Raccourci pour les deux dernières lignes commentées :

    # On envoie le context au template de statistics
    return render(request, "polls/statistics.html", context)