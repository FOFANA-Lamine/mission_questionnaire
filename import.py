# Passer le nom du fichier en ligne de commande
# argv



import requests
import json
import random
import unicodedata
import time

"""L'erreur 429 indique que vous avez dépassé le nombre de requêtes autorisées vers l'API dans un certain laps de temps, 
ce qui est souvent le cas avec des API publiques. Voici quelques stratégies pour gérer cette situation"""

open_quizz_data = (
    ("Science", "La nature", "https://opentdb.com/api.php?amount=20&category=17&difficulty=medium&type=multiple"),
    ("Sports", "Sport", "https://opentdb.com/api.php?amount=10&category=21&difficulty=medium&type=multiple")
)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    return (strip_accents(categorie).lower().replace(" ", "") +
         "_" + strip_accents(titre).lower().replace(" ","") +
        "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json")


def generate_json_file(categorie, titre, url):
    out_questions = []

    for attempt in range(5):  # Essai jusqu'à 5 fois
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            if 'results' not in data:
                print("La clé 'results' n'existe pas dans la réponse.")
                return

            results = data['results']
            break  # Sortir de la boucle si la requête a réussi
        elif response.status_code == 429:
            wait_time = 2 ** attempt     # Temps d'attente exponentiel
            print(f"Erreur 429 : Trop de requêtes. Attente de {wait_time} secondes avant de réessayer.")
            time.sleep(wait_time)  # Attendre avant de réessayer
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
            return

    # Si on est sorti de la boucle sans succès, on peut arrêter ici
    if response.status_code != 200:
        return

    for index, question in enumerate(results):
        dict_sortie_questionnaire = {}
        dict_sortie_questionnaire["infos"] = [ question['category'] , titre , question['difficulty'] ]
        dict_sortie_questionnaire["numero_question"] = index + 1
        dict_sortie_questionnaire["titre_question"] = question['question']
        bonne_reponse = question['correct_answer']
        dict_sortie_questionnaire["bonne_reponse"] = bonne_reponse
        listes_des_choix = [ bonne_reponse] + question['incorrect_answers']
        random.shuffle(listes_des_choix)


        dict_sortie_questionnaire["choix"] = listes_des_choix

        out_questions.append(dict_sortie_questionnaire)

    difficulty = results[0]['difficulty']
    out_filename = get_quizz_filename(categorie, titre, difficulty)

    out_json = json.dumps(out_questions, ensure_ascii=False, indent=4)
    with open(out_filename, "w", encoding='utf-8') as file:
        file.write(out_json)


for quizz_data in open_quizz_data:
    generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])