# Estimer le prix d'une voiture d'occasion 🚗

Projet du cours *Introduction to Data Processing* (MAM3, Université Côte d'Azur — Pr. L.
Fillatre). Groupe de 3. **Problème** : prédire le **prix** d'une voiture d'occasion à partir
de ses caractéristiques, et identifier les facteurs déterminants.

**Données** : *100 000 UK Used Cars* fusionné (7 marques), **71 450 voitures réelles**.

## Arborescence

```
projet fini/
├── src/
│   ├── preparation.py   # 1) tri/nettoyage des données + handcrafted features
│   ├── eda.py           # 2) graphes variable→prix + pertinence des features
│   ├── modeles.py       # 3) 4 modèles comparés en validation croisée
│   └── tout_lancer.py   # lance tout + écrit RESULTS.md
├── data/                # cars_dataset.csv (public) + cars_clean.csv (généré)
├── figures/             # tous les graphes (.png) générés
├── report/rapport.md    # le rapport (7 sections, consignes)
├── slides/main.tex      # présentation Beamer (Overleaf)
├── RESULTS.md           # tous les chiffres (généré)
├── NOTES_ORAL.md        # tâches faites + arguments pour la soutenance
├── requirements.txt
└── README.md
```

## Lancer

```bash
pip install -r requirements.txt
python src/tout_lancer.py                       # version publique
python src/tout_lancer.py "C:/chemin/CARS.csv"   # (préparation accepte aussi un chemin)
```

Tout est régénéré : `data/cars_clean.csv`, `figures/*.png`, `RESULTS.md`.

## Démarche (résumé)

1. **Tri/nettoyage** : années aberrantes, doublons, prix/km extrêmes, cylindrée 0 imputée,
   carburants rares regroupés, tri.
2. **Features** : `car_age`, `mileage_per_year`, `log_mileage`, `age_x_mileage`,
   `is_premium` + **target encoding** de `model`.
3. **Graphes** variable→prix avec la régression la plus adaptée + pertinence des features.
4. **4 modèles** en validation croisée 5 plis : linéaire brut / + log(prix) / + polynôme /
   Random Forest.
5. **Conclusion** : la régression linéaire (transformée) est adaptée et interprétable ;
   le Random Forest est la piste d'amélioration.

> Données réelles (antérieures à l'IA générative). Source publique :
> [Ajinkya017/Car_Dataset](https://github.com/Ajinkya017/Car_Dataset).
