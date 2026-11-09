from django import forms

class QuestionForm(forms.Form):

    question_text = forms.CharField(
        label="Texte de la question",
        max_length=200
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
