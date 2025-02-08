
import requests
import json
import random
import unicodedata
import time

open_quizz_data = (
    ("Histoires", "Les histoires", "https://opentdb.com/api.php?amount=30&category=23&difficulty=hard&type=multiple"),
    ("Sports", "Sport", "https://opentdb.com/api.php?amount=10&category=21&difficulty=medium&type=multiple"),
    ("Science", "La nature", "https://opentdb.com/api.php?amount=20&category=17&difficulty=medium&type=multiple")
)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ",
                                                                                                          "") + "_" + strip_accents(
        difficulte).lower().replace(" ", "") + ".json"


def generate_json_file(categorie, titre, url):
    out_questions = []
    response = requests.get(url)
    # Vérifiez si la requête a réussi
    if response.status_code != 200:
        print(f"Erreur lors de la requête : {response.status_code}")
        return

    data = json.loads(response.text)
    # Ajoutez ceci pour voir la réponse de l'API
    print(json.dumps(data, ensure_ascii=False, indent=4))  # Affiche la réponse de l'API

    try:
        results = data['results']
    except:
        print(f"la clef results n'existe pas pour la categorie :{categorie}")


    for index, question in enumerate(results):
        dict_sortie_questionnaire = {}   # Créer un nouveau dictionnaire pour chaque question
        dict_sortie_questionnaire["numero_question"] = index + 1
        dict_sortie_questionnaire["titre_question"] = question['question']

        listes_des_choix = [ question['correct_answer'] ] + question['incorrect_answers']  # Ajouter la bonne réponse et les réponses incorrectes
        random.shuffle(listes_des_choix)  # Mélanger les choix

        dict_sortie_questionnaire["choix"] = listes_des_choix  # Assigner les choix mélangés

        out_questions.append(dict_sortie_questionnaire)

    difficulty = results[0]['difficulty']  # Obtenir la difficulté après avoir récupéré les questions
    out_filename = get_quizz_filename(categorie, titre, difficulty)

    out_json = json.dumps( out_questions, ensure_ascii=False, indent=4)  # ensure_ascii=False pour garder les accents
    with open(out_filename, "w", encoding='utf-8') as file:  # Écriture avec encodage UTF-8
        file.write(out_json)


for quizz_data in open_quizz_data:
    generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])
