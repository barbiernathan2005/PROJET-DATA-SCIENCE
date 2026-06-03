# Le stress se lit-il dans notre mode de vie ?

Projet **Introduction to Data Processing** — MAM3, Université Côte d'Azur, 2025-2026.

Régression **linéaire** sur le dataset **réel** *Lifestyle & Wellbeing* (**15 971**
réponses, enquête Authentic-Happiness) pour expliquer le **stress quotidien**
(`DAILY_STRESS`, 0-5) à partir du mode de vie.

## 👥 Équipe
- Hafssa
- Thibaud
- Nathan

## 📦 Données
Dataset : https://www.kaggle.com/ydalat/lifestyle-and-wellbeing-data

## ⚙️ Installation & exécution
```bash
python -m venv .venv
# Windows :
.venv\Scripts\activate
# Mac / Linux :
# source .venv/bin/activate

pip install -r requirements.txt
python analyse_stress_wellbeing.py
```
Les figures sont enregistrées dans `figures/` et les **chiffres clés** (R², facteurs
les plus liés au stress…) sont affichés à la fin (« RÉCAP »), prêts à coller dans les
slides et le rapport.

## 📁 Fichiers
| Fichier | Contenu |
|---|---|
| `analyse_stress_wellbeing.py` | Analyse complète : nettoyage → visualisation → régression → features maison → validation |
| `report.tex` | **Rapport LaTeX** (classe `article`) — version compilable du rapport |
| `slides.tex` | **Slides LaTeX/Beamer** (thème Metropolis) — version compilable de l'oral |
| `slides_storytelling.md` | Contenu des 5 slides + script oral + Q&A anticipé (source du `.tex`) |
| `report.md` | Rapport écrit, 7 sections (source du `.tex`) |
| `figures/` | Graphiques générés par le script (dont `00_probleme1_synthetique.png`) |
| `requirements.txt` | Dépendances Python |
| `wellbeing.csv` | Données **réelles** *Lifestyle & Wellbeing* (15 972 lignes brutes) |
| `Global_Mental_Health_Dataset_2025.csv` | Données **synthétiques** abandonnées (preuve du « Problème 1 », corrélations ≈ 0) |

## 📄 Compilation LaTeX (rapport & slides)
Les figures doivent exister avant la compilation (lancer le script Python une fois).

**Le plus simple — [Overleaf](https://www.overleaf.com)** (aucune installation) : créer
un projet, glisser `report.tex`, `slides.tex` et le dossier `figures/`, puis compiler.

**En local** (TeX Live / MiKTeX) :
```bash
pdflatex report.tex && pdflatex report.tex   # 2 passes (sommaire + références)
pdflatex slides.tex && pdflatex slides.tex
```
> Thème des slides : **Metropolis**. Compatible `pdflatex` ; pour le rendu Fira Sans
> d'origine, compiler avec **XeLaTeX** ou **LuaLaTeX**. Le script oral est dans les
> `\note{}` (afficher avec `\setbeameroption{show notes}`).

## 🧭 Démarche (storytelling)
1. **Problème 1** : un premier dataset « santé mentale » sans aucune corrélation → données **synthétiques**.
2. **Problème 2** : sur de vraies données, aucune variable seule n'explique le stress.
3. **Résolution** : des **features maison** (soutien social, habitudes saines, surmenage, sommeil×flow) rendent le modèle simple et interprétable.
