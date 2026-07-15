import json
import streamlit as st

with open("recettes_cuisine.json", "r", encoding="utf-8") as f:
    dict_recettes = json.load(f)

st.title("Generateur de listes de courses")

recette_selectionnees = st.multiselect(
    "Choisis tes recettes",
    options=list(dict_recettes.keys())
)

desired_portions = {}

famille_ingredients = {"fruits_légumes": ["basilic frais", "persil frais", "pruneaux", "carottes", "champignons de paris", "courgettes", "épinards", "tomates", "citron vert", "citrons", "oignons", "gousses d'ail", "gingembre frais", "coriandre fraiche", "noix", "patates douces", "pommes de terre", "poivrons"],
                       "épicerie_salée": ["riz", "vermicelles de riz", "coulis de tomates", "lentilles corail", "tomates concassées", "huile d'olive", "huile de coco", "huile de tournesol", "moutarde à l'ancienne", "cube magique bouillon légumes", "lait de coco", "semoule", "linguine", "sauce nuoc nam"],
                       "épicerie_sucrée": ["pépites de chocolat noir", "chocolat noir", "cassonade", "sucre", "sucre glace", "farine t55", "farine t65", "lait", "levure boulangère", "levure chimique", "sucre vanillé"],
                       "produits_frais": ["beurre", "buche de chèvre", "crême fraiche", "grana padano rapé", "mozzarella", "pate feuilletée", "pate brisée", "pate sablée"],
                       "viandes_poissons": ["blanc de poulet", "lardons", "morue", "thon", "oeufs", "viande hachée"],
                       "épices": ["chili", "cumin", "curry", "garam masala", "poivre", "poudre de poivron doux", "sel"]}

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

for famille, ingredients in famille_ingredients.items():
    st.write(f"\n{famille.replace('_', ' ').capitalize()}:")
    for articles, [quantite, unite] in sorted(liste_courses.items()):
        if articles in ingredients:
            st.write(f"- {articles}: {quantite} {unite}")

