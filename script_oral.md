# 🎤 Script oral — « Combien vaut une voiture d'occasion ? »

**Équipe :** Hafssa El Hdour · Thibaud Crotta · Nathan Barbier
**Cours :** Introduction to Data Processing — MAM3, Université Côte d'Azur
**Durée visée :** ~5 minutes (équipe) + 5 minutes de questions

> **Légende :** le texte en noir est **ce qu'on dit à l'oral**.
> Le texte <span style="color:#1565C0">*en bleu entre parenthèses*</span> est une **explication pour nous** (à ne pas lire à voix haute) : il dit *pourquoi* on présente les choses ainsi.
> *(Remarque : GitHub n'affiche pas toujours la couleur dans le `.md` ; les explications restent reconnaissables car elles sont en italique et entre parenthèses.)*

---

## 🎬 Diapo de titre

Bonjour à tous. Notre projet s'intitule **« Combien vaut une voiture d'occasion ? »**. Nous sommes Hafssa, Thibaud et Nathan, et nous allons vous montrer comment, à partir de simples caractéristiques d'une voiture, on peut **prédire son prix de revente**.

<span style="color:#1565C0">*(On annonce tout de suite le sujet et l'équipe : une accroche courte et claire pour que le jury sache où on va.)*</span>

---

## 🎬 Slide 1 — Notre but : mettre un prix juste sur une voiture d'occasion

Notre point de départ est une question très concrète : **peut-on estimer le prix de revente d'une voiture d'occasion** à partir de ses caractéristiques — son âge, son kilométrage, sa cylindrée ?

<span style="color:#1565C0">*(C'est le « business goal » demandé dans les consignes : on commence toujours par le problème métier, pas par la technique.)*</span>

C'est exactement ce que fait un site d'annonces quand il vous dit si une offre est une bonne affaire.

<span style="color:#1565C0">*(On donne l'utilité concrète : ça rend le projet crédible et utile, pas juste un exercice scolaire.)*</span>

Point important pour la suite : la chose qu'on veut prédire, le prix, est une **grandeur continue** — sur le graphique de droite, on voit qu'elle s'étale de quelques centaines à plus de cent mille euros. Et c'est précisément parce que la cible est continue qu'on utilise une **régression linéaire**, et pas une régression logistique, qui sert pour du oui/non, ni une softmax, qui sert pour des catégories.

<span style="color:#1565C0">*(On justifie le choix du modèle DÈS le début, en s'appuyant sur le graphe : le prix est continu → régression linéaire. C'est un point que les profs attendent explicitement.)*</span>

---

## 🎬 Slide 2 — 71 593 voitures réelles, 10 variables, un prix à prédire

Passons aux données. Après nettoyage, on travaille sur **71 593 voitures** décrites par **10 variables** — ce sont de **vraies annonces** d'occasion du marché britannique, sur 7 marques.

<span style="color:#1565C0">*(On insiste sur « réelles » : des données du monde réel, imparfaites, par opposition à des données fabriquées — c'est un fil rouge de notre présentation.)*</span>

Ce qu'on veut prédire, le prix, vaut en moyenne **16 580 euros**, mais s'étale de **495 à 145 000** : c'est très asymétrique. On a cinq variables numériques — âge, kilométrage, cylindrée, consommation, taxe — et quatre catégorielles — marque, modèle, boîte, carburant.

<span style="color:#1565C0">*(On décrit les données comme demandé : combien de variables, de quels types. On glisse l'asymétrie du prix, qui resservira à la fin pour justifier une amélioration.)*</span>

Comme toute vraie donnée, elle est imparfaite : on a retiré **842 doublons** et fusionné les cinq voitures électriques, trop rares, dans « Other ».

<span style="color:#1565C0">*(C'est le « data wrangling » : on montre qu'on a nettoyé proprement, et qu'on a su gérer une catégorie trop rare.)*</span>

Enfin, les catégories n'ont pas d'ordre naturel — une boîte manuelle n'est pas « plus grande » qu'une automatique — donc on les encode en **One-Hot**, pour ne pas inventer un faux ordre que le modèle prendrait pour vrai.

<span style="color:#1565C0">*(On justifie l'encodage One-Hot : sans ça, le modèle croirait qu'une catégorie est « supérieure » à une autre, ce qui serait faux.)*</span>

---

## 🎬 Slide 3 — Une feature maison qui change tout : cylindrée ÷ âge

Voici le cœur de notre travail : les **caractéristiques qu'on a créées nous-mêmes**.

<span style="color:#1565C0">*(Les « handcrafted features » : c'est l'étape la plus valorisée du projet, on le souligne.)*</span>

En regardant les nuages de points, on a remarqué que certaines variables n'ont d'effet **qu'ensemble**. On a donc construit **`cylindree_sur_age`** : la cylindrée divisée par l'âge. Elle capte une **interaction** — un gros moteur **sur une voiture récente** se vend très cher, ce que ni la cylindrée seule ni l'âge seul ne voient.

<span style="color:#1565C0">*(On explique POURQUOI cette feature a un sens métier : c'est la combinaison « grosse motorisation » + « voiture jeune » qui fait grimper le prix.)*</span>

Point de méthode important : pour juger si une feature est bonne, on ne regarde pas la taille de son coefficient — qui dépend juste de l'échelle de la variable — mais le **vrai gain de performance en validation croisée**.

<span style="color:#1565C0">*(On montre qu'on sait évaluer une feature rigoureusement, pas « au pif ». C'est un argument méthodo fort.)*</span>

Et là, sur le graphe, `cylindree_sur_age` écrase les autres : elle explique **64 % du prix à elle seule** et fait gagner **0,07 de R²** au modèle. À l'inverse, on a écarté une autre idée, le kilométrage par an, parce qu'elle était corrélée à **0,96** au kilométrage : redondante, elle n'apportait rien.

<span style="color:#1565C0">*(On montre les deux côtés : une feature qu'on garde car elle apporte beaucoup, et une qu'on jette car redondante. C'est de la vraie sélection de variables.)*</span>

---

## 🎬 Slide 4 — On prédit le prix à 80 % — et c'est stable

On arrive au modèle. On a choisi une **régression linéaire multiple**, pour deux raisons : la cible est continue, et surtout ses coefficients se lisent directement **en euros**, ce qui nous permet d'**expliquer** le prix, pas seulement de le prédire.

<span style="color:#1565C0">*(On justifie le choix du modèle — attendu explicite des consignes — en insistant sur l'interprétabilité : on peut dire « +X euros par litre de cylindrée ».)*</span>

Pour être sûrs qu'il est fiable, on ne se contente pas d'un seul découpage des données : on fait un **holdout 80/20** ET une **validation croisée en 5 blocs**.

<span style="color:#1565C0">*(On répond à la question « les résultats sont-ils fiables ? » : on valide de deux manières, pas une seule.)*</span>

Résultat : le modèle explique **80 % de la variance** du prix sur des voitures qu'il n'a jamais vues, avec une erreur moyenne d'environ **2 760 euros**. Et comme la validation croisée donne **0,72 à plus ou moins 0,04** — très proche — on sait qu'il n'y a **pas de surapprentissage**.

<span style="color:#1565C0">*(Surapprentissage = un modèle qui apprend « par cœur » et se trompe sur de nouvelles données. Ici, test et validation croisée sont proches → le modèle généralise bien.)*</span>

Sur le graphe, chaque point est une voiture : plus il est près de la diagonale, mieux on l'a prédite. On voit aussi que le modèle peine sur les voitures les plus chères — ce qui nous amène à la conclusion.

<span style="color:#1565C0">*(On prépare la transition : la limite visible sur le graphe (voitures chères mal prédites) sera justement une de nos pistes d'amélioration.)*</span>

---

## 🎬 Slide 5 — Ce qu'on retient — et comment aller plus loin

Pour conclure. Avec un modèle **simple**, on explique déjà **80 % du prix**, avec des leviers de **bon sens** : la cylindrée fait **monter** le prix, l'âge et le kilométrage le font **baisser**. Concrètement, ça suffit à estimer un prix juste et repérer une bonne affaire.

<span style="color:#1565C0">*(On rappelle le bénéfice métier : le modèle est utile et ses conclusions sont logiques, ce qui le rend crédible.)*</span>

On a aussi identifié **trois pistes** pour faire mieux : modéliser le **logarithme du prix**, pour corriger l'asymétrie qu'on a vue et éviter les prédictions négatives ; **standardiser** les variables, pour que les coefficients soient comparables entre eux ; et **ajouter la marque**, pour distinguer le premium du généraliste.

<span style="color:#1565C0">*(Les améliorations demandées en conclusion — mais chacune est JUSTIFIÉE par quelque chose qu'on a observé : l'asymétrie du prix, l'interprétation des coefficients, etc. On ne les sort pas du chapeau.)*</span>

Et notre plus belle leçon vient du début : notre tout premier dataset, sur la santé mentale, **n'expliquait rien** — corrélations quasi nulles — parce qu'il était **synthétique**, fabriqué. Un dataset réel, lui, raconte une histoire. Savoir faire la différence, c'est la première compétence du data scientist.

<span style="color:#1565C0">*(On valorise notre esprit critique : on a su repérer qu'un premier jeu de données ne valait rien et changer. C'est exactement le genre de recul que le jury apprécie.)*</span>

---

## 🎬 Diapo « Merci »

Merci de votre attention. Nous sommes prêts à répondre à vos questions.

<span style="color:#1565C0">*(Phrase de clôture courte ; on enchaîne directement sur les 5 minutes de questions.)*</span>

---

## 💬 Bonus — Questions anticipées (à garder en tête pour le Q&A)

- **Pourquoi la régression linéaire ?** <span style="color:#1565C0">*(la cible « prix » est continue, et on veut interpréter les coefficients en euros.)*</span>
- **80 % de R², c'est bon ?** <span style="color:#1565C0">*(honnête pour un modèle simple, et test ≈ validation croisée → pas de surapprentissage.)*</span>
- **Pourquoi `cylindree_sur_age` et pas la cylindrée brute ?** <span style="color:#1565C0">*(elle capte l'interaction motorisation × jeunesse et apporte le plus gros gain de R².)*</span>
- **Pourquoi le modèle se trompe sur les voitures chères ?** <span style="color:#1565C0">*(le prix est très asymétrique ; piste = modéliser log(prix).)*</span>
- **Pourquoi ne pas avoir gardé `km_par_an` ?** <span style="color:#1565C0">*(corrélée à 0,96 au kilométrage → redondante, elle n'ajoute rien.)*</span>
- **Vos données sont-elles vraiment réelles ?** <span style="color:#1565C0">*(vraies annonces UK ; notre 1er dataset, lui, était synthétique — corrélations ≈ 0.)*</span>
