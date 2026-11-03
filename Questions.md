

2.2.1.3 Questions

o Voyez-vous tous les attributs de vos classes ?

Sur la liste non on voit seulement la question, mais quand on clique dessus pour le modifier on voit aussi la date. Idem pour le choix

o Pouvez-vous filtrer vos données suivants tous les attributs ?

Non

o Pouvez-vous trier vos données suivants tous les attributs ?

Non

o Pouvez-vous chercher un contenu parmi tous les champs ?

Non

2.2.2.2 Questions 

1. Lister tous les objets de type Question : faites une boucle pour afficher les attributs de
chaque question sur une ligne différente. Indice : remarquer que
Question.objects.all() est un itérable sur lequel vous pouvez boucler avec une
simple boucle for

>>> Question.objects.all()
<QuerySet [<Question: Quoi de neuf ?>, <Question: Préfères tu le ski ou la plage?>, <Question: Que penses tu d'Halloween?>, <Question: Langage de programmation préféré?>, <Question: Plongée ou Canyoning?>]>

>>> for question in Question.objects.all():
...     print(question)
... 
Quoi de neuf ?
Préfères tu le ski ou la plage?
Que penses tu d'Halloween?
Langage de programmation préféré?
Plongée ou Canyoning?
>>> 

2. Ajoutez un filtre sur la date de publication – portant par ex. sur un de ses composants4
suivants : year, month, day – de vos questions et lister un sous-ensemble de vos
questions suivant les dates que vous avez saisies à l'exercice précédent.

>>> from django.utils import timezone            
>>> current_month = timezone.now().month
>>> Question.objects.get(pub_date__month=current_month)
<Question: Quoi de neuf ?>

>>> from django.utils import timezone                  
>>> Question.objects.get(pub_date__month=7)                                      
<Question: Langage de programmation préféré?>

3. Trouvez la deuxième question (pour laquelle l'attribut de clé primaire id = 2) de votre base
de données, puis affichez les valeurs de tous ses attributs et tous les choix associés.

>>> q = Question.objects.get(pk=2)         
>>> print(q.id, q.question_text, q.pub_date)
5 Plongée ou Canyoning? 2025-06-18 15:02:09+00:00
>>> q.choice_set.all()            
<QuerySet [<Choice: Le ski !>, <Choice: La plage>, <Choice: Ni l'un ni l'autre>]>

4. Faites une boucle pour afficher les attributs de chaque question et leurs choix associés.

for question in Question.objects.all():
    print(question.id, question.question_text, question.pub_date)

    for choice in question.choice_set.all():
        print("  -", choice.choice_text, choice.votes)
		
		
>>> for question in Question.objects.all():
...     print(question.id, question.question_text, question.pub_date)
...     for choice in question.choice_set.all():
...         print("  -", choice.choice_text, choice.votes)
... 
1 Quoi de neuf ? 2026-11-03 07:52:06+00:00
  - Il fait beau aujourd'hui 0
  - La routine ! 0
  - Je suis malade 0
2 Préfères tu le ski ou la plage? 2026-08-07 08:52:06+00:00
  - Le ski ! 0
  - La plage 0
  - Ni l'un ni l'autre 0
3 Que penses tu d'Halloween? 2026-10-30 23:00:00+00:00
  - Trop bien ! 0
  - Je n'aime pas les bonbons 0
  - Je ne fête jamais Halloween 0
4 Langage de programmation préféré? 2026-07-18 15:32:09+00:00
  - Python of course 0
  - Java bien sur 0
  - PHP c'est trop la classe 0
5 Plongée ou Canyoning? 2025-06-18 15:02:09+00:00
  - La plongée, de préférence avec des tortues, requins ou autres 0
  - Canyoning mais attention à la tête 0
  - Ni l'un ni l'autre c'est trop dangereux 0


5. Affichez le nombre de choix enregistrés pour chaque question.

for question in Question.objects.all():
    print(question.question_text, question.choice_set.count())
	
>>> for question in Question.objects.all():
...     print(question.question_text, question.choice_set.count())
... 
Quoi de neuf ? 3
Préfères tu le ski ou la plage? 3
Que penses tu d'Halloween? 3
Langage de programmation préféré? 3
Plongée ou Canyoning? 3
	
6. [optionnel] Cherchez toutes les questions triées par le nombre de votes à chaque choix, en
utilisant la méthode order_by() – la méthode values() peut également être utilisée
pour obtenir un affichage plus complet des questions. Essayer d'utiliser Recherches
traversant les relations pour obtenir une solution la plus synthétique possible.

>>> Question.objects.order_by("choice__votes")
<QuerySet [<Question: Quoi de neuf ?>, <Question: Quoi de neuf ?>, <Question: Quoi de neuf ?>, <Question: Préfères tu le ski ou la plage?>, <Question: Préfères tu le ski ou la plage?>, <Question: Préfères tu le ski ou la plage?>, <Question: Que penses tu d'Halloween?>, <Question: Que penses tu d'Halloween?>, <Question: Que penses tu d'Halloween?>, <Question: Langage de programmation préféré?>, <Question: Langage de programmation préféré?>, <Question: Langage de programmation préféré?>, <Question: Plongée ou Canyoning?>, <Question: Plongée ou Canyoning?>, <Question: Plongée ou Canyoning?>]>

Question.objects.order_by("-choice__votes").values("id","question_text",
    "pub_date",
    "choice__choice_text",
    "choice__votes"
)

7. Triez les questions par ordre antéchronologique.

>>> Question.objects.order_by("-pub_date")
<QuerySet [<Question: Quoi de neuf ?>, <Question: Que penses tu d'Halloween?>, <Question: Préfères tu le ski ou la plage?>, <Question: Langage de programmation préféré?>, <Question: Plongée ou Canyoning?>]>

8. [optionnel] Cherchez toutes les questions dont un mot est présent dans le texte de ses
choix, en utilisant la recherche contains. Essayer d'utiliser Recherches traversant les
relations pour obtenir une solution la plus synthétique possible.
(Info : icontains ne respecte pas la casse, contains respecte la casse)

>>> Question.objects.filter(question_text__contains="Halloween")
<QuerySet [<Question: Que penses tu d'Halloween?>]>

>>> Question.objects.filter(choice__choice_text__contains="ski")
<QuerySet [<Question: Préfères tu le ski ou la plage?>]>

from django.db.models import Q

questions = Question.objects.filter(Q(question_text__contains="ski") | Q(choice__choice_text__contains="ski")).distinct()
for question in questions:
	print(question.question_text, question.choice_set.all())


>>> from django.db.models import Q
>>> questions = Question.objects.filter(Q(question_text__contains="ski") | Q(choice__choice_text__contains="ski"))
>>> for question in questions:
...     print(question.question_text, question.choice_set.all())
... 
Préfères tu le ski ou la plage? <QuerySet [<Choice: Le ski !>, <Choice: La plage>, <Choice: Ni l'un ni l'autre>]>
Préfères tu le ski ou la plage? <QuerySet [<Choice: Le ski !>, <Choice: La plage>, <Choice: Ni l'un ni l'autre>]>
Préfères tu le ski ou la plage? <QuerySet [<Choice: Le ski !>, <Choice: La plage>, <Choice: Ni l'un ni l'autre>]>
>>> questions = Question.objects.filter(Q(question_text__contains="ski") | Q(choice__choice_text__contains="ski")).distinct()
>>> for question in questions:
...     print(question.question_text, question.choice_set.all())
... 
Préfères tu le ski ou la plage? <QuerySet [<Choice: Le ski !>, <Choice: La plage>, <Choice: Ni l'un ni l'autre>]>
>>> 

9. Créez une question en utilisant le shell.

>>> from django.utils import timezone
>>> q = Question(question_text="Avez vous un/des chat(s) ou un/des chien(s)?", pub_date=timezone.now())
>>> q.save()

10. Ajoutez 3 choix à cette question en utilisant le shell.

>>> c = Choice(choice_text="Chat(s)", votes=0, question=q)
>>> c.save()
>>> c = Choice(choice_text="Chien(s)", votes=0, question=q)
>>> c.save()
>>> c = Choice(choice_text="Les deux !", votes=0, question=q)
>>> c.save()
>>> c = Choice(choice_text="Aucun des deux...", votes=0, question=q)
>>> c.save()

11. Listez les questions publiées récemment.

>>> from django.utils import timezone
>>> from datetime import timedelta
>>> date_limite = timezone.now() - timedelta(days=3)
>>> Question.objects.filter(pub_date__gte=date_limite)
<QuerySet [<Question: Quoi de neuf ?>, <Question: Avez vous un/des chat(s) ou un/des chien(s)?>]>


En fait on peut utiliser la méthode créée dans le modèle ! 

>>> for question in Question.objects.all():
...     if question.was_published_recently():
...         print(question.question_text)
... 
Quoi de neuf ?
Avez vous un/des chat(s) ou un/des chien(s)?

12. [optionnel] Listez tous les utilisateurs enregistrés sur l'application, en s'inspirant
de Utilisation du système d’authentification de Django > Création d'utilisateurs pour
accéder à tous les objets de la classe User (s'inspirer également du code de la Q1).

>>> from django.contrib.auth.models import User
>>> User.objects.all()
<QuerySet [<User: admin>, <User: seve>]>
>>> for user in User.objects.all():
...     print(user.id, user.username, user.email)
...     print(user.username, user.first_name, user.last_name, user.is_staff, user.is_active)
... 
1 admin admin@example.com
admin   True True
2 seve severine.hori.maitrehut@fms-ea.com
seve severine hm True False



2.2.3 Exercice d'écriture de méthodes du modèle – optionnel

Dans le cours vous avez créé une méthode d'instance de la classe Question
nommée was_published_recently(). Elle s'applique aux objets de la
classe Question et permet de déterminer si la question a été publiée récemment ou non.

1. Sur le même modèle, ajoutez une méthode nommée age() qui calcule l'âge de la
question.

>>> for question in Question.objects.all():
...     print(question.age())
... 
5:10:10.845341
88 days, 4:10:10.845514
3 days, 14:02:16.845593
107 days, 21:30:07.845695
502 days, 22:00:07.845734
0:56:11.694394

2. Vous avez remarqué dans l'exercice précédent que l'affichage d'un objet des
classes Question ou Choix affichait les valeurs des
attributs question_text ou choice_text. Or ces valeurs peuvent être très longues
(max_length=200), ce qui peut encombrer l'affichage. Modifiez ces classes pour
n'afficher que les 20 premiers caractères de ces attributs.
3. Modifiez la classe Question pour ajouter l'affichage de la date de publication lors de
l'affichage d'une de ces instances.

Pour tester 2 et 3 : Question.objects.all()

>>> Question.objects.all()
<QuerySet [<Question: Quoi de neuf ? - 03/11/2026 à 08h52>, <Question: Préfères tu le ski o - 07/08/2026 à 10h52>, <Question: Que penses tu d'Hall - 31/10/2026 à 00h00>, <Question: Langage de programma - 18/07/2026 à 17h32>, <Question: Plongée ou Canyoning - 18/06/2025 à 17h02>, <Question: Avez vous un/des cha - 03/11/2026 à 13h06>]>
>>> 

4. Ajoutez une méthode à la classe Question nommée get_choices() qui retourne les
choix, leur nombre et proportions de votes. Gardez en tête que l'objectif d'une méthode
de classe n'est pas d'afficher un contenu mais de fournir un contenu à une vue pour
traitement ultérieur (par ex. ici une liste de tuples). Indice : remarquer que l'on peut itérer
sur q.choice_set.all() – si q est par ex. Question.objects.get(pk=1)

==>Pas fait complétement j'ai juste voulu renvoyer la liste des choix pour une question, test comme ça : 

>>> q = Question.objects.get(pk=1)
>>> for c in q.get_choices():
...     print(c)
... 
Il fait beau aujourd
La routine !
Je suis malade

