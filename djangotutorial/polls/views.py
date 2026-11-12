from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F, Max
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
#from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.db.models import Sum

from polls.forms import QuestionForm
from polls.models import Question, Choice
from polls.utils import minimax

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.

NB_MAX_CHOIX = 5



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
        # return Question.objects.order_by("-pub_date")[:5]
        """
        Return the last five published questions (not including those set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

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
    """
    if not request.user.is_authenticated:
        #return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        return render(request, "polls/login_error.html")"""

    #question_list = Question.objects.order_by("-pub_date")

    # On va récupérer les informations qu'on souhaite ensuite afficher
    # le nombre total de sondage enregistrés
    #nb_sondages = question_list.count()
    nb_sondages = Question.objects.count()

    # le nombre total de choix possibles
    nb_total_choices = Choice.objects.count()

    # le nombre total de votes (voir aide pdf)
    #nb_total_votes = Choice.objects.aggregate(Sum("votes"))
    nbr_votes = Choice.objects.aggregate(somme=Sum('votes'))['somme']

    # la moyenne du nombre de votes par sondage
    moyenne_par_sondage = nbr_votes / nb_sondages

    # [optionnel] la question la plus populaire ET [optionnel] la question la moins populaire
    question_la_moins_populaire, question_la_plus_populaire = minimax()

    # la dernière question enregistrée
    id_derniere_question = Question.objects.aggregate(max=Max('id'))['max']

    # On va implanter ces informations dans le context qui sera ensuite envoyé au gabarit
    context = {
        "nbr_sondages": nb_sondages,
        "nb_total_choices": nb_total_choices,
        "nb_total_votes": nbr_votes,
        'moyenne_par_sondage': moyenne_par_sondage,

        'question_la_plus_populaire': question_la_plus_populaire,
        'question_la_moins_populaire': question_la_moins_populaire,
        'derniere_question': id_derniere_question,

    }
    # template = loader.get_template("polls/index.html")
    # return HttpResponse(template.render(context, request))
    # Raccourci pour les deux dernières lignes commentées :

    # On envoie le context au template de statistics
    return render(request, "polls/statistics.html", context)


#Version avec formulaire simple (pas utilisé ModelForm)
@login_required
def ajouter_question(request):

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            # Récupération du texte de la question
            question_text = form.cleaned_data["question_text"]

            # Récupération de la date
            pub_date = form.cleaned_data["pub_date"]

            # Si aucune date n'est renseignée
            if not pub_date:
                pub_date = timezone.now()

            # Création de la question
            question = Question.objects.create(
                question_text=question_text,
                pub_date=pub_date
            )

            # Récupération des cinq choix
            choices = [
                form.cleaned_data["choice1"],
                form.cleaned_data["choice2"],
                form.cleaned_data["choice3"],
                form.cleaned_data["choice4"],
                form.cleaned_data["choice5"]
            ]

            # Création des choix renseignés
            for choice_text in choices:

                if choice_text:
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text
                    )

            messages.success(request, "La question a bien été ajoutée.")
            # Sans le raccourci
            # return HttpResponseRedirect(reverse("polls:index"))
            # En utilisant le raccourci de from django.shortcuts import redirect
            return redirect("polls:index")
    else:
        form = QuestionForm()

    return render(
        request,
        "polls/ajouter_question.html",
        {"form": form}
    )

def modifier_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Si on vient du formulaire (donc rempli)
    if request.method == "POST":
        # On récupère l'objet du formulaire
        form = QuestionForm(request.POST)

        if form.is_valid():
            # S'il est valide on récupère les informations de la question et on la sauvegarde
            question.question_text = form.cleaned_data["question_text"]
            question.pub_date = form.cleaned_data["pub_date"]
            question.save()

            # On récupère la liste des choix actuellement associés à la question
            choix_existants = list(question.choice_set.all())

            # On parcoure les inputs des choix
            for i in range(1, 6):
                # On récupère le texte de l'input
                texte = form.cleaned_data[f"choice{i}"]

                # Tant qu'on est dans le nombre de choix qui existaient déjà, on les modifie
                if i <= len(choix_existants):
                    choix = choix_existants[i - 1]
                    # Si l'input est rempli on modifie le choix
                    if texte:
                        choix.choice_text = texte
                        choix.save()
                    # Sinon on le supprime
                    else:
                        choix.delete()
                # Sinon on crée un nouveau choix
                elif texte:
                    Choice.objects.create(question=question, choice_text=texte)

            messages.success(request, "La question a bien été modifiée.")

            return redirect("polls:index")

    else:
        """form = QuestionForm(initial={
            "question_text": question.question_text,
            "pub_date": question.pub_date,
        })"""
        # On récupère les choix associés à cette question
        choix = question.choice_set.all()
        # Initial : crée le formulaire avec les valeurs actuelles de la question à modifier
        initial = {
            "question_text": question.question_text,
            "pub_date": question.pub_date,
        }

        for i, choice in enumerate(choix, start=1):
            initial[f"choice{i}"] = choice.choice_text

        form = QuestionForm(initial=initial)

    return render(request, "polls/modifier_question.html", {
        "form": form,
        "question": question
    })

@login_required
def supprimer_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(f"On va supprimer la question numéro {question_id} ")
    question.delete()

    messages.success(request, "La question a bien été supprimée.")

    return redirect("polls:index")

@login_required
def add(request):
    #return render(request, 'polls/add.html')

    return render(request, 'polls/add.html', {
    'liste_no_choix': range(NB_MAX_CHOIX)
    })

def confirm_add(request):
    # récupération du libellé de la question,
    # sans les éventuels espaces avant et après
    question_text = request.POST['question_text'].strip()
    if question_text:
        # ajout de la question si elle n'est pas vide
        question = Question(question_text=question_text, pub_date=timezone.now())
        question.save()

        # on traite à présent les champs de choix remplis
        # (on s'arrête au premier vide)
        for no_choix in range(NB_MAX_CHOIX):
            nom_champ = 'choix_{}'.format(no_choix)
            choice_text = request.POST[nom_champ].strip()
            if choice_text:
                choice = Choice(question=question, choice_text=choice_text)
                choice.save()
            else:
                break

        return render(request, 'polls/confirm_add.html')
    else:
        # réaffichage du formulaire de saisie de la question
        # avec le message d'erreur
        return render(request, 'polls/add.html', {
        'error_message': "You didn't enter a question text",
        })

""" Sans utiliser authenticationForm 
def login_view(request):
    # username = request.POST["username"]
    # password = request.POST["password"]

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect("polls:index")
    else:
        # Return an 'invalid login' error message.
        return render(request, "polls/index.html", {
            "error_message": "Identifiant ou mot de passe incorrect."
        })
"""

def login_view(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # On récupère l'url demandée pour retourner dessus et non sur la page d'accueil
            next_url = request.POST.get("next")  #next_url = request.GET.get("next") ?

            if next_url:
                return redirect(next_url)

            return redirect("polls:index")

    else:
        form = AuthenticationForm()

    return render(request, "polls/login.html", {
        "form": form
    })



"""
# Avec méthode GET (lien seul)
def logout_view(request):
    logout(request)
    return redirect("polls:index")
"""
def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("polls:index")