# Combien vaut une voiture d'occasion ?

Projet **Introduction to Data Processing** — MAM3, Université Côte d'Azur, 2025-2026.

Régression **linéaire** sur le dataset **réel** *UK Used Cars* (**72 435** annonces de
voitures d'occasion, 7 marques) pour prédire le **prix** (`price`, en £) à partir des
caractéristiques du véhicule.

## 👥 Équipe
- Hafssa
- Thibaud
- Nathan

## 📦 Données
- Dataset (EDA) : https://www.kaggle.com/code/harishkumardatalab/eda-of-multibrand-used-car-dataset
- CSV utilisé (miroir) : https://github.com/Ajinkya017/Car_Dataset → `cars_dataset.csv`

## ⚙️ Installation & exécution
```bash
python -m venv .venv
# Windows :
.venv\Scripts\activate
# Mac / Linux :
# source .venv/bin/activate

pip install -r requirements.txt
python new_code.py                  # régression : prédiction du prix (+ figures)
python probleme1_mental_health.py   # figure du « Problème 1 » (dataset synthétique)
```
Le script affiche la **performance** du modèle (R², RMSE) et les **coefficients**, et
enregistre les figures dans `figures/`.

## 📁 Fichiers
| Fichier | Contenu |
|---|---|
| `new_code.py` | Régression linéaire : nettoyage → features maison → modèle → **R²/RMSE** → figures |
| `probleme1_mental_health.py` | Régénère la figure du « Problème 1 » (corrélations ≈ 0 du dataset synthétique) |
| `cars_dataset.csv` | Données **réelles** UK Used Cars (72 435 lignes) |
| `Global_Mental_Health_Dataset_2025.csv` | Données **synthétiques** abandonnées (« Problème 1 ») |
| `report.tex` / `report.pdf` | Rapport (LaTeX + PDF) |
| `slides.tex` / `slides.pdf` | Slides de l'oral (Beamer Metropolis + PDF) |
| `report.md` / `slides_storytelling.md` | Versions Markdown (sources du récit) |
| `figures/` | Graphiques générés par les scripts |
| `requirements.txt` | Dépendances Python |

## 📄 Compilation LaTeX (rapport & slides)
Lancer d'abord les scripts Python (les figures doivent exister).

**Le plus simple — [Overleaf](https://www.overleaf.com)** (aucune installation) : créer
un projet, glisser `report.tex`, `slides.tex` et le dossier `figures/`, puis compiler.

**En local** (TeX Live / MiKTeX) :
```bash
pdflatex report.tex && pdflatex report.tex
pdflatex slides.tex && pdflatex slides.tex
```
> Thème des slides : **Metropolis**. Compatible `pdflatex` ; pour le rendu Fira Sans
> d'origine, compiler avec **XeLaTeX** ou **LuaLaTeX**.

## 🧭 Démarche (storytelling)
1. **Problème 1** : un premier dataset « santé mentale » sans aucune corrélation (|r| max ≈ 0.04) → données **synthétiques**, inexploitables.
2. **Pivot** : un **vrai** dataset de voitures d'occasion → de vraies relations.
3. **Résolution** : 2 features maison (`car_age`, `mileage_per_year`) + régression linéaire → on prédit le prix à **~74 %** (R² = 0.735).
