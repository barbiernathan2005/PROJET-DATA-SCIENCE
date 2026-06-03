# Resultats (genere par tout_lancer.py)

Annee de reference (age) : 2021


## 1. Pertinence des variables (R2 univarie avec le prix)

| Variable | R2 | correlation |
|---|---|---|
| engineSize | 0.401 | +0.63 |
| car_age | 0.282 | -0.53 |
| log_mileage | 0.206 | -0.45 |
| is_premium | 0.192 | +0.44 |
| Odometer | 0.188 | -0.43 |
| age_x_mileage | 0.154 | -0.39 |
| tax | 0.132 | +0.36 |
| mileage_per_year | 0.124 | -0.35 |
| mpg | 0.111 | -0.33 |

## 2. Graphe variable -> prix : le lineaire suffit-il ?

| Variable | R2 lineaire | meilleur ajustement | R2 meilleur |
|---|---|---|---|
| Age (annees) | 0.282 | logarithmique | 0.345 |
| Kilometrage (mi) | 0.188 | polynomiale | 0.227 |
| Km par an | 0.124 | polynomiale | 0.154 |
| Cylindree (L) | 0.401 | polynomiale | 0.402 |
| Consommation (mpg) | 0.111 | logarithmique | 0.26 |
| Taxe (GBP) | 0.132 | polynomiale | 0.146 |
| Marque | - | moyenne/groupe | 0.226 |
| Transmission | - | moyenne/groupe | 0.291 |
| Carburant | - | moyenne/groupe | 0.054 |
| Premium (0/1) | - | moyenne/groupe | 0.192 |
| Modele (top 15) | - | moyenne/groupe | 0.621 |

## 3. Comparaison des modeles (validation croisee 5 plis)

| Modele | R2 (CV) | R2 (test) | RMSE test (GBP) | MAE test (GBP) |
|---|---|---|---|---|
| Lineaire (brut) | 0.887 | 0.888 | 2,980 | 2,097 |
| Lineaire + log(prix) | 0.907 | 0.905 | 2,745 | 1,772 |
| Lineaire + polynome (deg2) | 0.918 | 0.919 | 2,541 | 1,770 |
| Random Forest | 0.961 | 0.963 | 1,704 | 1,123 |

**Meilleur modele : Random Forest.**


## 4. Variables les plus importantes (Random Forest)

- model : 0.589
- age_x_mileage : 0.195
- car_age : 0.088
- engineSize : 0.059
- mpg : 0.031
- transmission_Manual : 0.007
- mileage_per_year : 0.005
- Odometer : 0.004

## 5. Correlation avec le prix

- engineSize : +0.63
- car_age : -0.53
- is_premium : +0.44
- Odometer : -0.43
- tax : +0.36
- mileage_per_year : -0.35
- mpg : -0.33
