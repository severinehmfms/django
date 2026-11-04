from django.urls import path

from . import views

app_name = "polls"

""" Vues "normales"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # added the word 'specifics' : Si on veut modifier l'url pour le détail c'est ici qu'il faut le faire !
    # path("specifics/<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]"""

# Vues génériques pour IndexView DetailView et ResultsView
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("all/", views.AllView.as_view(), name="all"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]