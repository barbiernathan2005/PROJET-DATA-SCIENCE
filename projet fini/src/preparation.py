"""
preparation.py  ---  ETAPE 1 : tri des donnees + handcrafted features
=====================================================================
Programme 1/3 du pipeline. Il :
  - charge le dataset brut,
  - TRIE / NETTOYE / COMPLETE les donnees (doublons, valeurs manquantes,
    annees aberrantes, prix et kilometrages extremes, cylindree=0 imputee,
    carburants rares regroupes, tri final),
  - cree plusieurs HANDCRAFTED FEATURES de qualite (justifiees dans le rapport),
  - enregistre le dataset propre dans data/cars_clean.csv,
  - imprime un RAPPORT DE NETTOYAGE (chiffres a citer a l'oral).

Lancer seul :   python preparation.py
Importer    :   from preparation import get_data
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "cars_dataset.csv")
CLEAN = os.path.join(ROOT, "data", "cars_clean.csv")

REFERENCE_YEAR = 2021                      # annee de collecte du dataset (UK ~2020)
PREMIUM_BRANDS = {"Audi", "Bmw"}           # marques premium presentes dans le dataset


# --------------------------------------------------------------------- charge
def load_raw(path=RAW):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype(str).str.strip()
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    df = df.rename(columns={"mileage": "Odometer"})
    df["Make"] = df["Make"].str.title()        # 'audi' -> 'Audi'
    return df


# --------------------------------------------------------------------- nettoie
def clean(df, verbose=True):
    rep = {"lignes_depart": int(len(df))}

    # 1) doublons
    rep["doublons"] = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # 2) valeurs manquantes (avant)
    rep["valeurs_manquantes"] = int(df.isnull().sum().sum())

    # 3) annees aberrantes (le dataset contient des 1970 / 2060)
    rep["annees_aberrantes"] = int(((df.year < 1990) | (df.year > REFERENCE_YEAR)).sum())
    df = df[(df.year >= 1990) & (df.year <= REFERENCE_YEAR)]

    # 4) prix : positifs + on coupe les 0.1% extremes (erreurs / hypercars)
    df = df[df.price > 0]
    lo, hi = df.price.quantile([0.001, 0.999])
    rep["prix_extremes"] = int(((df.price < lo) | (df.price > hi)).sum())
    df = df[(df.price >= lo) & (df.price <= hi)]

    # 5) kilometrage irrealiste (> 300 000 miles)
    rep["km_irrealistes"] = int((df.Odometer > 300000).sum())
    df = df[df.Odometer <= 300000]

    # 6) cylindree == 0 -> IMPUTATION par la mediane du meme carburant
    mask0 = df.engineSize == 0
    rep["cylindree_imputee"] = int(mask0.sum())
    med = df.loc[df.engineSize > 0].groupby("fuelType")["engineSize"].median()
    glob = df.loc[df.engineSize > 0, "engineSize"].median()
    df.loc[mask0, "engineSize"] = df.loc[mask0, "fuelType"].map(med).fillna(glob)

    # 7) regrouper les carburants rares (< 100 occurrences) dans "Other"
    vc = df.fuelType.value_counts()
    keep = vc[vc >= 100].index
    rep["carburants_regroupes"] = int((~df.fuelType.isin(keep)).sum())
    df["fuelType"] = df.fuelType.where(df.fuelType.isin(keep), "Other")

    # 8) NaN / inf residuels
    df = df.replace([np.inf, -np.inf], np.nan).dropna()

    # 9) tri final (lisibilite du CSV)
    df = df.sort_values(["Make", "model", "year", "price"]).reset_index(drop=True)

    rep["lignes_finales"] = int(len(df))
    rep["lignes_supprimees"] = rep["lignes_depart"] - rep["lignes_finales"]
    if verbose:
        print("--- RAPPORT DE NETTOYAGE ---")
        for k, v in rep.items():
            print(f"  {k:22s}: {v:,}")
    return df, rep


# ----------------------------------------------------------------- features
def add_features(df):
    """Cree les handcrafted features (justifiees dans le rapport)."""
    df = df.copy()
    # 1. age : 1er facteur de decote
    df["car_age"] = (REFERENCE_YEAR - df.year).clip(lower=0)
    # 2. intensite d'usage : separe age et usure
    df["mileage_per_year"] = df.Odometer / (df.car_age + 1)
    # 3. log du kilometrage : variable tres asymetrique -> linearise
    df["log_mileage"] = np.log1p(df.Odometer)
    # 4. interaction age x kilometrage : vieux ET tres roule se cumulent
    df["age_x_mileage"] = df.car_age * df.Odometer
    # 5. marque premium (domaine) : Audi / BMW tiennent mieux la cote
    df["is_premium"] = df.Make.isin(PREMIUM_BRANDS).astype(int)
    return df.replace([np.inf, -np.inf], np.nan).dropna()


# --------------------------------------------------------------------- public
def get_data(path=RAW, save=True, verbose=True):
    df = load_raw(path)
    df, rep = clean(df, verbose=verbose)
    df = add_features(df)
    if save:
        df.to_csv(CLEAN, index=False)
        if verbose:
            print(f"  -> dataset propre enregistre : {CLEAN}  ({len(df):,} lignes)")
    return df, rep


if __name__ == "__main__":
    get_data()
