# Le stress se lit-il dans notre mode de vie ?

Projet **Introduction to Data Processing** — MAM3, Université Côte d'Azur, 2025-2026.

Régression **linéaire** sur le dataset **réel** *Lifestyle & Wellbeing* (~12 700
réponses, enquête Authentic-Happiness) pour expliquer le **stress quotidien**
(`DAILY_STRESS`, 0-5) à partir du mode de vie.

## 👥 Équipe
- [Prénom 1]
- [Prénom 2]
- [Prénom 3]

## 📦 Données
Dataset : https://www.kaggle.com/ydalat/lifestyle-and-wellbeing-data
1. Télécharge le CSV depuis Kaggle (connexion requise).
2. Place-le dans ce dossier sous le nom **`wellbeing.csv`** (ou adapte la variable
   `CSV` en haut de `analyse_stress_wellbeing.py`).

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
| `slides_storytelling.md` | Contenu des 5 slides de l'oral + script + Q&A anticipé |
| `report.md` | Rapport écrit (7 sections) |
| `figures/` | Graphiques générés par le script |
| `requirements.txt` | Dépendances Python |

## 🧭 Démarche (storytelling)
1. **Problème 1** : un premier dataset « santé mentale » sans aucune corrélation → données **synthétiques**.
2. **Problème 2** : sur de vraies données, aucune variable seule n'explique le stress.
3. **Résolution** : des **features maison** (soutien social, habitudes saines, surmenage, sommeil×flow) rendent le modèle simple et interprétable.
