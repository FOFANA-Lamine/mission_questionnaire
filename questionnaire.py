import json


class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def poser(self, num_question, nb_question):
        self.num_question = num_question
        self.nb_question = nb_question
        print(f"QUESTION {self.num_question} / {self.nb_question}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte



    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)


class Questionnaire:
    def __init__(self, questions, categorie, titre, difficulte):
        self.questions = questions
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte


    def lancer(self):
        nb_questions = len(self.questions)
        score = 0

        print("----------")
        print(f"QUESTIONNAIRE : {self.titre}")
        print(f"    Catégorie : {self.categorie}")
        print(f"    Difficulté : {self.difficulte}")
        print(f"    Nombre de question : {nb_questions}")
        print("----------")

        for i in range(nb_questions):
            question = self.questions[i]
            if question.poser(i+1 , nb_questions):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score

"""
Questionnaire(
    (
    Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"), 
    Question("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
    Question("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
    )
).lancer()
"""

# Chargement de fichier
filename = "sports_sport_medium.json"
file = open(filename, "r")
json_data = file.read()
file.close()

# Déseraialisation
questionnaire_data = json.loads(json_data)

# LANCER NOTRE QUESTIONNAIRE

dict_questions = [ question for question in questionnaire_data]

# Extraire les infos avec la première question par exmeple
premiere_question = dict_questions[0]
categorie , titre, difficulte = premiere_question['infos'][0] , premiere_question['infos'][1] , premiere_question['infos'][2]


listes_questions = []
for question in dict_questions:
    q = Question( question['titre_question'], question['choix'], question['bonne_reponse'])
    listes_questions.append(q)

Questionnaire( listes_questions , categorie, titre, difficulte  ).lancer()


















