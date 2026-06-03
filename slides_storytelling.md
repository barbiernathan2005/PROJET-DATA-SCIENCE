# 🎤 Oral (5 min) — « Combien vaut une voiture d'occasion ? »
### Squelette des 5 slides + script + Q&A (CHIFFRES RÉELS intégrés)

> Minutage : S1≈45 s · S2≈55 s · S3≈70 s · S4≈90 s · S5≈40 s ≈ **5 min**.

---

## SLIDE 1 — Business goal  *(titre « question »)*
### Titre : « Combien vaut votre voiture d'occasion ? »

**Sur la slide :**
- 🎯 Notre question : *peut-on **prédire le prix** d'une voiture d'occasion ?*
- 😕 1er essai : un dataset « santé mentale » (2 500 lignes) qui ne disait **rien** (|r| max ≈ 0.04 → **synthétique**).
- ✅ Notre choix : un **vrai dataset** — **72 000 voitures** d'occasion au Royaume-Uni (7 marques).
- 💡 Utile : estimer un prix juste, repérer les bonnes affaires, alimenter les sites d'annonces.
- 🖼️ *Figure : `figures/00_probleme1_synthetique.png`*

**À dire :** « On voulait prédire quelque chose d'utile. Premier piège : un dataset "santé mentale" parfait en apparence, mais **aucune variable n'en expliquait une autre** — des données **générées artificiellement**. On a donc changé pour un **vrai dataset** : 72 000 annonces de voitures d'occasion, pour répondre à : *combien vaut une voiture ?* »

---

## SLIDE 2 — Data description  *(titre « descriptif »)*
### Titre : « 72 000 voitures, 10 variables, un prix à prédire »

**Sur la slide :**
- 📊 Source **réelle** UK Used Cars · **72 435 lignes** · **10 variables**.
- 🎯 Cible : `price`, le prix en **livres £**.
- 🔢 Numériques : année, kilométrage, taxe, consommation, **cylindrée** + catégorielles : modèle, boîte, carburant, marque.
- 🧹 Nettoyage : années aberrantes (**2060**, **1970**) + doublons retirés → **71 593 lignes**.
- 🖼️ *Figure : `figures/01_heatmap_correlations.png`*

**À dire :** « Données **réelles** : de vraies annonces. On veut prédire le **prix**. Comme toute vraie donnée, elle est imparfaite : on a trouvé une voiture datée de **2060**, une de 1970, et des doublons — qu'on a nettoyés. Premier constat sur la heatmap : la **cylindrée** et l'**année** ressortent. »

---

## SLIDE 3 — Handcrafted features  *(le cœur du projet)*
### Titre : « 2 indices maison à partir de l'année »

**Sur la slide :**
| Feature maison | Construction | Corrélation au prix |
|---|---|---|
| **car_age** | 2026 − année | **−0.52** ✅ (usure) |
| **mileage_per_year** | kilométrage ÷ (âge + 1) | **−0.40** ✅ |

- 💡 `car_age` : plus une voiture est vieille, moins elle vaut.
- 💡 `mileage_per_year` : distingue une **vieille voiture peu roulée** d'une **récente très roulée**.

**À dire :** « Plutôt que l'année brute, on construit deux indices plus parlants. **car_age**, l'âge de la voiture, est notre signal négatif le plus fort (−0.52). Et **le kilométrage par an** : 100 000 km, ça n'a pas le même sens sur une voiture de 2 ans ou de 10 ans. Ces deux indices simples portent l'effet du temps sur le prix. »

---

## SLIDE 4 — Regression  *(titre « affirmation »)*
### Titre : « On prédit le prix à 74 % — et on corrige un vrai bug »

**Sur la slide :**
- ⚙️ Régression **linéaire**, 5 variables, split **80-20**.
- 📈 **R² (test) = 0.735** · R² (train) = 0.725 (pas de surapprentissage) · **RMSE ≈ 4 800 £**.
- 🔴 **Monte** le prix : cylindrée **+10 862 £/L**, boîte +480 £.
- 🔵 **Baisse** le prix : **âge −1 695 £/an**, kilométrage/an −1.3 £.
- 🐞 **Bug corrigé** : le code **importait** R²/RMSE mais ne les **calculait jamais** → ajout de l'évaluation (+ chemin de fichier relatif).
- 🖼️ *Figures : `figures/03_actual_vs_predicted.png`, `figures/04_coefficients.png`*

**À dire :** « Le modèle explique **74 %** du prix — et train ≈ test, donc pas de surapprentissage. En moyenne on se trompe de ~4 800 £. Le levier le plus fort, c'est la **cylindrée** ; à l'inverse, chaque **année** d'âge coûte ~1 700 £. Surtout : le code de départ **importait** le R² et l'erreur mais ne les affichait jamais — une régression qui ne se mesure pas ! On a **corrigé** ça. »

---

## SLIDE 5 — Conclusion  *(boucle le récit)*
### Titre : « Des données réelles racontent une histoire — pas des données fabriquées »

**Sur la slide :**
- ✅ Un modèle **simple** explique déjà **~74 %** du prix ; leviers clairs (cylindrée ↑, âge ↓).
- 🏆 Nos features **car_age** / **mileage_per_year** portent l'effet du temps.
- 💡 Leçon : notre 1er dataset (santé mentale) n'expliquait rien car **synthétique** (corrélations ≈ 0).
- ⚠️ Limites : catégories encodées en nombres (faux ordre), prix brut, marque/carburant non utilisés.
- 🚀 Pistes : one-hot, modéliser **log(prix)**, ajouter marque & carburant, Ridge/Lasso.

**À dire :** « En résumé : un modèle simple, mais qui prédit le prix à 74 % avec des leviers de bon sens. Notre plus belle leçon vient de l'échec du début : un dataset **fabriqué** ne raconte **rien** (corrélations nulles), un dataset **réel**, si. Savoir faire la différence, c'est la première compétence du data scientist. Merci. »

---

## 🛡️ Q&A anticipé
- **Pourquoi linéaire ?** → la cible (prix) est **continue** et on veut **interpréter** les coefficients (en £). Simple et lisible.
- **R² de 0.74, c'est bon ?** → oui, honnête pour un modèle simple ; et **train ≈ test** → pas de surapprentissage.
- **Pourquoi encoder `model` en nombre ?** → solution **simple** pour un premier modèle ; limite assumée (faux ordre) → piste = one-hot.
- **Pourquoi la dispersion sur les voitures chères ?** → la variance du prix augmente avec sa valeur ; piste = modéliser **log(prix)**.
- **Le vrai bug du code ?** → il **importait** `r2_score`/`mean_squared_error` mais ne les utilisait jamais → la régression ne s'évaluait pas. Corrigé.
- **Données vraiment réelles ?** → vraies annonces UK ; imperfections du réel (année 2060, doublons). Le 1er dataset, lui, avait des corrélations ≈ 0 = signature du synthétique.

---
*Rappel : 5 slides (1 par thème), dépôt **Git** (URL dans le rapport), slides sur Moodle jeudi soir.*
