# Notes pour la soutenance orale 🎤

> Tout ce qu'il faut **connaître et savoir argumenter** (oral + rapport), classé pour
> coller aux **consignes**. Chiffres exacts dans `RESULTS.md`.

---

## A. Ce qu'on a fait (tâches réalisées — à pouvoir décrire)

1. **Choix du problème & des données** : prédire le **prix** d'une voiture d'occasion
   (valeur continue → régression). Dataset *100 000 UK Used Cars* fusionné, **71 450
   voitures réelles**, 7 marques. Données **antérieures à l'IA** (condition du sujet).
2. **Tri / nettoyage** (`src/preparation.py`) : suppression des **années aberrantes**
   (1970, 2060), des **doublons**, des **prix et kilométrages extrêmes** ; **imputation**
   de la cylindrée `=0` (médiane par carburant) ; **regroupement** des carburants rares ;
   **tri** final. → dataset propre `data/cars_clean.csv`.
3. **Handcrafted features** (5 + un encodage) — voir §C.
4. **Visualisation** (`src/eda.py`) : pour **chaque variable**, graphe variable→prix avec la
   **régression la plus adaptée** ; distributions ; corrélations ; pertinence des features.
5. **Modélisation** (`src/modeles.py`) : **4 modèles** comparés en **validation croisée 5
   plis** ; importance des variables ; vrai vs prédit.
6. **Livrables** : `report/rapport.md` (7 sections), `slides/main.tex` (Overleaf),
   ce document, dépôt **Git**.

> **Pipeline modulaire** (argument d'ingénieur) : *préparation → EDA → modélisation*, chacun
> exécutable seul, le tout relancé par `src/tout_lancer.py`.

## B. Le fil narratif (storytelling) — à raconter

1. *« On veut estimer le prix d'une voiture d'occasion. »*
2. *« En regardant les données, le **prix est très asymétrique** et la relation **prix–âge
   n'est pas linéaire** (décote rapide les premières années). »*
3. *« Donc une régression linéaire **brute sous-ajuste**. On a construit des **features**
   (log du kilométrage, interaction âge×km, encodage du modèle) et **transformé** la cible
   en `log(prix)`. »*
4. *« Résultat : la régression linéaire **transformée** devient bien meilleure et **reste
   interprétable**. Un **Random Forest** fait encore un peu mieux, mais moins interprétable
   → on le garde comme piste d'amélioration. »*

## C. Les features (consigne « Handcrafted features ») — savoir les justifier

| Feature | Pourquoi (à dire) |
|---|---|
| `car_age = 2021 − year` | l'âge est le **1er facteur de décote** (exponentielle) |
| `mileage_per_year = km/(âge+1)` | **intensité d'usage** : 10 ans à 40k mi ≠ 10 ans à 180k mi |
| `log_mileage`$^\star$ | km **très asymétrique** → le log **linéarise** (R²=0.21 > Odometer brut 0.19) |
| `age_x_mileage`$^\star$ | **interaction** : vieux **et** très roulé se cumulent |
| `is_premium`$^\star$ | Audi/BMW **tiennent mieux la cote** (domaine) |
| **target encoding `model`** | le **modèle** explique **R²≈0.62** à lui seul → on remplace chaque modèle par son **prix moyen** (calculé **sur le train** = pas de fuite) ; mieux que `LabelEncoder` (faux ordre) |

> $\star$ = nos ajouts. **Vérif. de pertinence** : R² univarié de chaque feature
> (fig. `20_pertinence_features.png`) → `log_mileage` et `is_premium` sont bien pertinentes.

## D. La régression (consigne « quelle régression ? pourquoi ? fiable ? »)

- **Quelle ?** **Linéaire**, car la cible (prix) est **continue**. (Logistique = binaire,
  softmax = K classes ; il faudrait découper le prix en tranches → perte d'info.)
- **Le linéaire suffit-il ?** Pas en brut : plusieurs relations sont **courbées** (âge :
  R² 0.28→0.34 avec une courbe ; mpg : 0.11→0.26). On le corrige en **restant linéaire**
  (log(prix), features polynomiales/log).
- **Fiabilité ?** **Validation croisée 5 plis** + jeu de test : R²(CV) ≈ R²(test) → pas de
  sur-apprentissage manifeste. RMSE/MAE en £ = erreur moyenne interprétable.
- **Modèles comparés** : Linéaire brut / Linéaire+log / Linéaire+polynôme / Random Forest.
  **Chiffres réels :** Linéaire brut R²=0.89 (RMSE £2 980) → +log(prix) 0.91 → +polynôme
  0.92 (RMSE £2 541) → **Random Forest 0.96 (RMSE £1 704)**. On **retient la linéaire
  transformée** (interprétable, R²≈0.92), RF = piste d'amélioration.

## E. Variables les plus importantes (à citer)

- Univarié : **`engineSize` 0.40**, **`car_age` 0.28**, **`model` encodé 0.62** (le plus fort).
- Random Forest (multivarié) : **`model` 0.59, `age_x_mileage` 0.20, `car_age` 0.09,
  `engineSize` 0.06** → les **2 variables les plus importantes sont des features construites**
  (argument fort pour la slide « handcrafted features »).

## F. Questions probables + réponses

- *« Pourquoi pas de la classification / logistique ? »* → le prix est un **nombre continu**,
  c'est une régression ; la logistique servirait à prédire une **catégorie**.
- *« Pourquoi pas du deep learning ? »* → sur des **données tabulaires**, les arbres
  (RF/Gradient Boosting) battent le DL ; et le projet est noté sur les **features faites
  main**, que le DL apprendrait tout seul. (« pas d'IA » = **données** non générées par IA.)
- *« Pourquoi le R² univarié est faible (0.1–0.6) ? »* → c'est **une variable à la fois** ;
  le modèle **multivarié** combine tout et monte beaucoup plus haut (voir `RESULTS.md`).
- *« LabelEncoder ou one-hot ? »* → **one-hot** pour les catégorielles à peu de valeurs
  (faux ordre sinon), **target encoding** pour `model` (trop de valeurs).
- *« Fuite de données ? »* → le target encoding et la standardisation sont **dans un
  Pipeline**, donc appris **sur le train uniquement** à chaque pli de la validation croisée.
- *« Pourquoi avoir imputé la cylindrée à 0 ? »* → un `engineSize=0` est une **valeur
  manquante déguisée** (électriques / erreurs) ; on la remplace par la médiane du même
  carburant (imputation simple, vue en cours).

## G. Mapping consignes → où c'est traité

| Consigne (slide / rapport) | Où |
|---|---|
| 1. Business goal | rapport §1, slide 1 |
| 2. Data description / Team management | rapport §1-2, slide 2 |
| 3. Data visualisation | rapport §3, `figures/`, slide 2-3 |
| 4. Handcrafted features | rapport §4, slide 3, §C ci-dessus |
| 5. Régression (laquelle, pourquoi, fiable) | rapport §5, slide 4, §D ci-dessus |
| 6. Conclusion (améliorer ?) | rapport §6, slide 5 |
| 7. Références + **dépôt Git** | rapport §7 + URL à coller |
| Storytelling | §B ci-dessus |

## H. À NE PAS oublier avant la soutenance

- [ ] Mettre les **vrais noms** des 3 membres (rapport §2, slides).
- [ ] **Pousser** le dépôt sur GitHub et **coller l'URL** dans le rapport (consigne).
- [ ] Déposer les **slides** (PDF) sur Moodle **jeudi soir**.
- [ ] (Idéal) Relancer `python src/tout_lancer.py` sur **votre** `CARS.csv` pour des
      chiffres identiques aux vôtres (sinon ceux de la version publique suffisent).
