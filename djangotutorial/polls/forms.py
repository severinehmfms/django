from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


class QuestionForm(forms.Form):
    def verifier_question(value):
        if "?" not in value:
            raise ValidationError("La question doit contenir un point d'interrogation.")

    question_text = forms.CharField(
        label="Texte de la question",
        help_text="Minimum 10 caractères, maximum 200 caractères",
        max_length=200,
        error_messages={"required": "La question est obligatoire"}, #permet de personnaliser le message d'erreur renvoyé par Django., mais ne fonctionne pas si le navigateur vérifie AVANT
        validators=[
            MinLengthValidator(10),
            verifier_question
        ],
    )

    pub_date = forms.DateTimeField(
        label="Date et heure de publication",
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"type": "datetime-local"}
        )
    )

    choice1 = forms.CharField(
        label="Choix 1",
        max_length=200,
        required=False
    )

    choice2 = forms.CharField(
        label="Choix 2",
        max_length=200,
        required=False
    )

    choice3 = forms.CharField(
        label="Choix 3",
        max_length=200,
        required=False
    )

    choice4 = forms.CharField(
        label="Choix 4",
        max_length=200,
        required=False
    )

    choice5 = forms.CharField(
        label="Choix 5",
        max_length=200,
        required=False
    )
