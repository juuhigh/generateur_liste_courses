import json
import streamlit as st

dict_recettes = json.load(open("recettes_cuisine.json", "r"))

st.title("Generateur de listes de courses")

recette_selectionnees = st.multiselect(
    "Choisis tes recettes",
    options=list(dict_recettes.keys())
)

desired_portions = {}

for recette in recette_selectionnees:
    base = dict_recettes[recette]["nb_portions"]

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
    for dict_ingredient in dict_recettes[recette]["ingredients"]:
        ingredient = dict_ingredient["nom"]
        quantite = dict_ingredient["quantite"]
        unite = dict_ingredient["unite"]

        if ingredient in liste_courses.keys():
            liste_courses[ingredient][0] += float(quantite) * portion / dict_recettes[recette]["nb_portions"]
            if liste_courses[ingredient][1] != unite:
                print(f"Unité différente pour {ingredient}: {liste_courses[ingredient][1]} vs {unite}")
                break
        else:
            liste_courses[ingredient] = [float(quantite) * portion / dict_recettes[recette]["nb_portions"], unite]

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

for articles, [quantite, unite] in sorted(liste_courses.items()):
    st.write(f"- {articles}: {quantite} {unite}")
