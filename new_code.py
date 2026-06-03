# -*- coding: utf-8 -*-
"""
new_code.py
===========
Projet « Introduction to Data Processing » — MAM3, Université Côte d'Azur, 2025-2026.
Équipe : Hafssa, Thibaud, Nathan.

    « Combien vaut une voiture d'occasion ? »

Régression LINÉAIRE sur le dataset RÉEL des voitures d'occasion du Royaume-Uni
(7 marques, ~72 000 annonces) pour prédire le PRIX (`price`) à partir des
caractéristiques du véhicule.

Exécution :
    python new_code.py

Sorties :
    figures/01_heatmap_correlations.png
    figures/02_prix_par_categorie.png
    figures/03_actual_vs_predicted.png
    figures/04_coefficients.png
"""

import matplotlib
matplotlib.use("Agg")  # backend sans fenêtre : on enregistre les figures sur disque

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

FIG = "figures"
os.makedirs(FIG, exist_ok=True)

# ==========================
# 1. Loading dataset
# ==========================

# CORRIGÉ : chemin relatif (le fichier est dans le dossier du projet) au lieu du
# chemin codé en dur "C:\Users\AzComputer\Downloads\projet\CARS.csv".
cars = pd.read_csv("cars_dataset.csv")

cars = cars.rename(columns={'mileage': 'Odometer'})

if 'Unnamed: 0' in cars.columns:
    cars.drop(['Unnamed: 0'], axis=1, inplace=True)

print(cars.head())
print(cars.shape)
print(cars.info())
print(cars.describe().T)
print(cars.isnull().sum())

for col in cars.columns:
    print(col, ':', cars[col].nunique())

# ==========================
# 2. Cleaning
# ==========================

print(cars.year.value_counts().sort_index())

# Erreurs de saisie évidentes sur l'année -> on retire ces lignes.
cars.drop(cars[cars.year == 2060].index, inplace=True)
cars.drop(cars[cars.year == 1970].index, inplace=True)

cars = cars.drop_duplicates()

print("Duplicated rows:", cars.duplicated().sum())

print(cars.transmission.value_counts())
print(cars.fuelType.value_counts())

# Très peu d'électriques -> regroupées dans "Other" pour ne pas créer une catégorie rare.
cars['fuelType'] = cars['fuelType'].replace('Electric', 'Other')

print(cars.fuelType.value_counts())
print("Shape after cleaning:", cars.shape)

# ==========================
# 3. Handcrafted Features
# ==========================

# Âge de la voiture (en 2026) : un proxy d'usure attendu négativement lié au prix.
cars['car_age'] = 2026 - cars['year']

# Kilométrage moyen par an : distingue une vieille voiture peu roulée d'une récente
# très roulée. (+1 pour éviter une division par zéro sur les voitures de l'année.)
cars['mileage_per_year'] = cars['Odometer'] / (cars['car_age'] + 1)

print(cars[['year', 'Odometer', 'car_age', 'mileage_per_year']].head())

# ==========================
# 4. Numerical / Categorical Features
# ==========================

categorical_features = list(cars.select_dtypes(include="object").columns)
numerical_features = list(cars.select_dtypes(include=["int64", "float64"]).columns)

print("Categorical features:")
print(categorical_features)

print("Numerical features:")
print(numerical_features)

cars_num = cars[numerical_features]

# ==========================
# 5. Mean price by categories
# ==========================

mp_transmission = (
    cars.groupby('transmission')['price']
    .mean()
    .sort_values(ascending=False)
    .round(2)
)

print("\nMean price by transmission:")
print(mp_transmission)

mp_fueltype = (
    cars.groupby('fuelType')['price']
    .mean()
    .sort_values(ascending=False)
    .round(2)
)

print("\nMean price by fuel type:")
print(mp_fueltype)

# ==========================
# 6. Correlation Heatmap
# ==========================

corr = cars_num.corr()

print("\nCorrelation matrix:")
print(corr)

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='RdYlGn', fmt='.2f')
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(FIG, "01_heatmap_correlations.png"), dpi=130)  # CORRIGÉ : enregistre au lieu de plt.show()
plt.close()

corr_with_price = (
    corr['price']
    .drop('price')
    .sort_values(ascending=False)
)

print("\nCorrelation with price:")
print(corr_with_price)

# ==========================
# 7. Categorical features vs Price
# ==========================

plt.figure(figsize=(18, 12))
plt.suptitle('Categorical features vs Price')

plt.subplot(2, 2, 1)
sns.boxplot(x='transmission', y='price', data=cars)

plt.subplot(2, 2, 2)
sns.boxplot(x='fuelType', y='price', data=cars)

plt.subplot(2, 1, 2)
sns.boxplot(x='Make', y='price', data=cars)

plt.tight_layout()
plt.savefig(os.path.join(FIG, "02_prix_par_categorie.png"), dpi=130)
plt.close()

# ==========================
# 8. Regression Preparation
# Keep only selected variables
# ==========================

cars_reg = cars.copy()

# Encodage simple des deux variables catégorielles utilisées dans le modèle.
le_model = LabelEncoder()
le_transmission = LabelEncoder()

cars_reg['model'] = le_model.fit_transform(cars_reg['model'])
cars_reg['transmission'] = le_transmission.fit_transform(cars_reg['transmission'])
print("\n===== BEFORE ENCODING =====")
print(cars[['model', 'transmission']].head(10))
print("\n===== AFTER ENCODING =====")
print(cars_reg[['model', 'transmission']].head(10))

cars_model = cars_reg[
    [
        'car_age',
        'mileage_per_year',
        'engineSize',
        'transmission',
        'model',
        'price'
    ]
]

print(cars_model.head())

X = cars_model.drop('price', axis=1)
y = cars_model['price']

# ==========================
# 9. Train / Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================
# 10. Linear Regression
# ==========================

model = LinearRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)

# CORRIGÉ : le code importait r2_score et mean_squared_error mais ne les utilisait
# jamais -> une régression n'affichait NI R² NI erreur. On évalue maintenant le modèle.
r2_train = r2_score(y_train, model.predict(X_train))
r2_test = r2_score(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))

print("\n===== PERFORMANCE DU MODELE =====")
print("R2 (train) :", round(r2_train, 3))
print("R2 (test)  :", round(r2_test, 3))
print("RMSE (test):", round(rmse, 2), "GBP")

# ==========================
# 11. Actual vs Predicted Plot # Validation
# ==========================

plt.figure(figsize=(8, 6))
plt.scatter(y_test, pred, alpha=0.5)

plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    'r--'
)

plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Prices (R2 = %.2f)" % r2_test)
plt.tight_layout()
plt.savefig(os.path.join(FIG, "03_actual_vs_predicted.png"), dpi=130)
plt.close()

# ==========================
# 12. Feature Importance
# ==========================

coef_df = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_
})

coef_df = coef_df.sort_values(by='Coefficient', ascending=False)

print("\nRegression Coefficients:")
print(coef_df)

plt.figure(figsize=(8, 5))
sns.barplot(data=coef_df, x='Coefficient', y='Feature')
plt.title("Feature Importance")
plt.xlabel("Coefficient Value")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig(os.path.join(FIG, "04_coefficients.png"), dpi=130)
plt.close()

print("\nFigures enregistrées dans le dossier '%s/'." % FIG)
