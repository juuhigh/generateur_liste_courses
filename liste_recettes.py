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

st.title("Generateur de listes de courses")

recette_selectionnees = st.multiselect(
    "Choisis tes recettes",
    options=list(dict_recettes.keys())
)

desired_portions = {}

famille_ingredients = {"fruits_et_légumes": ['ananas', 'aubergine', 'basilic frais', 'carottes', 'cernaux de noix', 'champignons de paris', 'citron', 'citron vert', 'concombres', 'coriandre fraiche', 'courgette', 'gingembre frais', "gousses d'ail", 'noix', 'oignons jaune', 'oignons rouge', 'patates douces', 'persil frais', 'poireaux', 'poivron rouge', 'pommes de terre', 'pruneaux', 'salade laitue', 'salade roquette', 'tomates allongées', 'tomates cerise', 'tomates rondes', 'épinards'],
                       "épicerie_salée": ['coulis de tomate', 'croutons', 'cube magique bouillon légumes', 'farine t00', "filets d'anchois", "huile d'olive", 'huile de coco', 'huile de tournesol', 'jus de citron', 'lait de coco', 'lentilles corail', 'moutarde', "moutarde à l'ancienne", 'pâtes farfalle', 'pâtes linguine', 'riz', 'sauce nuoc nam', 'semola di granna duro', 'semoule', 'tomates concassées', 'tomates séchées', 'vermicelles de riz', 'vinaigre de xérès'],
                       "épicerie_sucrée": ['cassonade', 'chocolat noir', 'farine t55', 'farine t65', 'lait', 'levure boulangère', 'levure chimique', 'miel liquide', 'pain de mie', 'pépites de chocolat noir', 'sucre', 'sucre glace', 'sucre vanillé'],
                       "produits_frais": ['beurre', 'buche de chèvre', 'burrata', 'crême fraiche', 'fromage de chêvre à tartiner', 'fromage râpé', 'grana padano râpé', 'jampon cru', 'mini mozzarella', 'mozzarella', 'parmesan copeaux', 'parmesan râpé', 'pate brisée', 'pate feuilletée', 'pate sablée'],
                       "viandes_poissons": ['blanc de poulet', 'lardons', 'morue', 'oeuf', 'thon', 'viande hachée'],
                       "épices": ['chili', 'cumin', 'curry', 'garam masala', 'poivre', 'poudre de poivron doux', 'sel']}

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

texte_liste_courses = build_liste_courses_text(liste_courses, famille_ingredients)
st.text_area("Liste de courses", value=texte_liste_courses, height="content")

