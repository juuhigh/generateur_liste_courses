import json
import subprocess
import streamlit as st
import requests


def build_liste_courses_text(liste_courses, famille_ingredients):
    lignes = []
    for famille, ingredients in famille_ingredients.items():
        lignes.append(f"{famille.replace('_', ' ').capitalize()}:")
        for articles, [quantite, unite] in sorted(liste_courses.items()):
            if articles in ingredients:
                lignes.append(f"- {articles}: {quantite} {unite}")
        lignes.append("")
    
    liste_finale = lignes
    return "\n".join(liste_finale).strip()


def get_recette_data(recette_name):
    for value in dict_recettes.values():
        if isinstance(value, dict) and recette_name in value:
            return value[recette_name]
    raise KeyError(f"Recette introuvable: {recette_name}")


# FILE_ID = "1m6tYhr7uXdt_-eowYhjBJlEz8f1rTnx2"
# URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
# https://drive.google.com/file/d/1m6tYhr7uXdt_-eowYhjBJlEz8f1rTnx2/view?usp=drive_link

# try:
#     response = requests.get(URL)
#     response.raise_for_status()

#     st.success("Données récupérées avec succès depuis Google Drive.")
# except requests.exceptions.RequestException as e:
#     st.error(f"Erreur lors de la récupération des données : {e}")
# except ValueError:
#     st.error("Erreur lors de l'analyse des données JSON.")


# dict_recettes = requests.get(URL).json()

with open("recettes_cuisine.json", "r", encoding="utf-8") as f:
    dict_recettes = json.load(f)

famille_ingredients = dict_recettes["famille_ingrédients"]

st.title("Générateur de listes de courses")

recette_salees_selectionnees = st.multiselect(
    "Choisis tes recettes salées",
    options=sorted(list(dict_recettes["recettes_salées"].keys()))
)

recette_sucrees_selectionnees = st.multiselect(
    "Choisis tes recettes sucrées",
    options=sorted(list(dict_recettes["recettes_sucrées"].keys()))
)

recette_selectionnees = recette_salees_selectionnees + recette_sucrees_selectionnees
desired_portions = {}

for recette in recette_selectionnees:
    recette_data = get_recette_data(recette)
    base = recette_data["nb_portions"]

    desired_portions[recette] = st.number_input(
        f"{recette} - portions",
        min_value=1,
        value=base,
        step=1,
        key=recette
    )

recettes_choisies = {recette: desired_portions[recette] for recette in recette_selectionnees}

liste_courses = {}

for recette, portion in recettes_choisies.items():
    recette_data = get_recette_data(recette)
    for dict_ingredient in recette_data["ingredients"]:
        ingredient = dict_ingredient["nom"]
        quantite = dict_ingredient["quantite"]
        unite = dict_ingredient["unite"]
        scaled_quantite = float(quantite) * portion / recette_data["nb_portions"]

        if ingredient in liste_courses:
            liste_courses[ingredient][0] += scaled_quantite
            if liste_courses[ingredient][1] != unite:
                print(f"Unité différente pour {ingredient}: {liste_courses[ingredient][1]} vs {unite}")
                break
        else:
            liste_courses[ingredient] = [scaled_quantite, unite]

st.header("Liste des courses")

quantite_blanc = 0
quantite_jaune = 0

for articles, [quantite, unite] in sorted(liste_courses.items()):
    if articles == "oeufs, blanc":
        quantite_blanc = quantite
        liste_courses.pop(articles, None)
    if articles == "oeufs, jaune":
        quantite_jaune = quantite
        liste_courses.pop(articles, None)

if "oeufs" in liste_courses:
    liste_courses["oeufs"] = [liste_courses["oeufs"][0] + max(quantite_blanc, quantite_jaune), ""]
else:
    if quantite_blanc > 0 or quantite_jaune > 0:
        liste_courses["oeufs"] = [max(quantite_blanc, quantite_jaune), ""]

texte_liste_courses = build_liste_courses_text(liste_courses, famille_ingredients)
st.text_area("Liste de courses", value=texte_liste_courses, height="content")

