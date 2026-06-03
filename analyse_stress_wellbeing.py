# -*- coding: utf-8 -*-
"""
analyse_stress_wellbeing.py
============================
Projet « Introduction to Data Processing » — MAM3, Université Côte d'Azur, 2025-2026.
Équipe : Haffsa, Thibaud, Nathan.

    « Le stress se lit-il dans notre mode de vie ? »

Régression LINÉAIRE sur le dataset RÉEL *Lifestyle & Wellbeing* (enquête
Authentic-Happiness, ~16 000 réponses) pour expliquer le stress quotidien
(`DAILY_STRESS`, 0-5) à partir du mode de vie.

Pipeline :
    chargement -> nettoyage -> visualisation -> features maison -> régression -> validation.

Exécution :
    python analyse_stress_wellbeing.py

Sorties :
    * figures/00_probleme1_synthetique.png  (si le dataset synthétique est présent)
    * figures/01_correlations.png
    * figures/02_coefficients_base.png
    * figures/03_coefficients_indices.png
    * un « RÉCAP » des chiffres clés affiché en fin d'exécution (prêt à coller
      dans les slides / le rapport).

Tous les chiffres du rapport sont reproductibles : graine fixée (RANDOM_STATE = 42).
"""

import sys
from pathlib import Path

# Console Windows : forcer UTF-8 pour les caractères « é », « ≈ », « ↑ »… (sinon cp1252 plante)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # backend sans fenêtre : on enregistre les figures sur disque
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
RANDOM_STATE = 42          # reproductibilité : même split, mêmes chiffres
TEST_SIZE = 0.20           # découpage train / test 80-20
N_FOLDS = 5                # validation croisée 5-fold

HERE = Path(__file__).resolve().parent
DATA = HERE / "wellbeing.csv"
SYNTH = HERE / "Global_Mental_Health_Dataset_2025.csv"  # dataset abandonné (Problème 1)
FIGDIR = HERE / "figures"
FIGDIR.mkdir(exist_ok=True)

TARGET = "DAILY_STRESS"
# Couleurs : rouge = fait MONTER le stress, bleu = fait BAISSER (palette à 2 couleurs,
# l'œil compare mieux des longueurs que des angles — cf. cours data-visualisation).
RED, BLUE = "#d1495b", "#3a6ea5"


def signed_colors(values):
    """Rouge pour les valeurs positives (aggravantes), bleu pour les négatives."""
    return [RED if v >= 0 else BLUE for v in values]


# --------------------------------------------------------------------------- #
# 1. Chargement + nettoyage (data wrangling)
# --------------------------------------------------------------------------- #
def load_and_clean():
    """Charge le CSV, corrige la valeur cassée de la cible, encode et renvoie (df, X, y).

    Détails du nettoyage :
      * `Timestamp` : retiré (identifiant, non explicatif).
      * `DAILY_STRESS` : une ligne contient une date ('1/1/00') glissée dans la
        colonne -> forcée en NaN puis retirée (15 971 lignes conservées).
      * `AGE`, `GENDER` : encodage one-hot (drop_first) pour éviter un faux ordre.
      * `WORK_LIFE_BALANCE_SCORE` : EXCLU des explicatives — c'est une combinaison
        des autres colonnes (fuite d'information -> R² artificiellement parfait).
    """
    df = pd.read_csv(DATA)
    df = df.drop(columns=["Timestamp"])

    n_before = len(df)
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    n_broken = int(df[TARGET].isna().sum())
    df = df.dropna(subset=[TARGET]).reset_index(drop=True)

    print(f"[nettoyage] lignes : {n_before} -> {len(df)} "
          f"({n_broken} valeur(s) cassée(s) retirée(s) dans {TARGET})")
    print(f"[nettoyage] cible {TARGET} : min={df[TARGET].min():.0f} "
          f"max={df[TARGET].max():.0f} (traitée comme continue)")

    y = df[TARGET].astype(float)
    X = df.drop(columns=[TARGET, "WORK_LIFE_BALANCE_SCORE"])
    X = pd.get_dummies(X, columns=["AGE", "GENDER"], drop_first=True).astype(float)
    print(f"[nettoyage] design matrix : {X.shape[1]} variables explicatives "
          f"(one-hot AGE/GENDER, hors fuite WLB)")
    return df, X, y


# --------------------------------------------------------------------------- #
# 2. Visualisation — corrélation de chaque variable brute avec le stress
# --------------------------------------------------------------------------- #
def figure_correlations(df):
    """Figure 1 : barres horizontales triées des corrélations brutes au stress."""
    num = df.select_dtypes("number").drop(columns=["WORK_LIFE_BALANCE_SCORE"])
    corr = num.corr()[TARGET].drop(TARGET).sort_values()

    plt.figure(figsize=(8, 7))
    plt.barh(corr.index, corr.values, color=signed_colors(corr.values))
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Corrélation de chaque variable avec le stress quotidien")
    plt.xlabel("corrélation de Pearson avec DAILY_STRESS")
    plt.tight_layout()
    out = FIGDIR / "01_correlations.png"
    plt.savefig(out, dpi=130)
    plt.close()
    print(f"[figure] {out.name}")
    return corr


# --------------------------------------------------------------------------- #
# 3. Régression de base (toutes les variables brutes)
# --------------------------------------------------------------------------- #
def base_regression(X, y):
    """Régression linéaire sur toutes les variables brutes.

    Renvoie (coefficients standardisés, R² test). Les coefficients d'affichage
    sont estimés sur l'ensemble des données (interprétation la plus stable) ;
    le R² « honnête » provient du jeu de test 80-20 jamais vu à l'entraînement.
    """
    # R² honnête : standardisation apprise sur le train uniquement (pas de fuite)
    Xtr, Xte, ytr, yte = train_test_split(
        X.values, y.values, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    pipe = make_pipeline(StandardScaler(), LinearRegression()).fit(Xtr, ytr)
    r2_test = pipe.score(Xte, yte)

    # Coefficients pour l'interprétation : fit sur tout, variables standardisées
    Xz = StandardScaler().fit_transform(X.values)
    coef = pd.Series(
        LinearRegression().fit(Xz, y.values).coef_, index=X.columns
    ).sort_values()

    plt.figure(figsize=(8, 7))
    plt.barh(coef.index, coef.values, color=signed_colors(coef.values))
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Coefficients du modèle de régression (variables standardisées)")
    plt.xlabel("poids dans la régression (rouge = ↑ stress, bleu = ↓ stress)")
    plt.tight_layout()
    out = FIGDIR / "02_coefficients_base.png"
    plt.savefig(out, dpi=130)
    plt.close()
    print(f"[figure] {out.name}")
    print(f"[régression base] R² (test 80-20) = {r2_test:.3f}")
    return coef, r2_test


# --------------------------------------------------------------------------- #
# 4. Features maison (handcrafted features)
# --------------------------------------------------------------------------- #
def build_handcrafted(df):
    """Construit 4 indices maison + renvoie (DataFrame des features, corrélations).

    Hypothèses :
      * SOCIAL_SUPPORT : le soutien social amortit le stress (Cohen & Wills, 1985).
      * HEALTHY_HABITS : les bons comportements d'hygiène de vie se cumulent.
      * OVERWORK : proxy de surmenage (congés non pris + irritabilité − temps pour soi).
      * SLEEP_x_FLOW : INTERACTION (produit, type « Pclass × Age ») — bien dormir ET
        être souvent absorbé aurait un effet protecteur combiné.
    """
    f = pd.DataFrame(index=df.index)
    f["SOCIAL_SUPPORT"] = df["CORE_CIRCLE"] + df["SOCIAL_NETWORK"] + df["SUPPORTING_OTHERS"]
    f["HEALTHY_HABITS"] = (
        df["SLEEP_HOURS"] + df["DAILY_STEPS"] + df["WEEKLY_MEDITATION"] + df["FRUITS_VEGGIES"]
    )
    f["OVERWORK"] = df["LOST_VACATION"] + df["DAILY_SHOUTING"] - df["TIME_FOR_PASSION"]
    f["SLEEP_x_FLOW"] = df["SLEEP_HOURS"] * df["FLOW"]

    corr = f.apply(lambda c: c.corr(df[TARGET])).sort_values()
    print("[features maison] corrélation avec le stress :")
    for name, val in corr.items():
        verdict = "OK" if abs(val) >= 0.10 else "ÉCHEC (quasi nul)"
        print(f"    {name:16s} {val:+.3f}   {verdict}")
    return f, corr


def features_regression(features, y):
    """Régression sur les 4 indices maison : R² test, R² 5-fold, coefficients."""
    X = features.values
    Xtr, Xte, ytr, yte = train_test_split(
        X, y.values, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    pipe = make_pipeline(StandardScaler(), LinearRegression()).fit(Xtr, ytr)
    r2_test = pipe.score(Xte, yte)

    cv_pipe = make_pipeline(StandardScaler(), LinearRegression())
    cv = cross_val_score(cv_pipe, X, y.values, cv=N_FOLDS, scoring="r2")

    Xz = StandardScaler().fit_transform(X)
    coef = pd.Series(
        LinearRegression().fit(Xz, y.values).coef_, index=features.columns
    ).sort_values()

    plt.figure(figsize=(7, 4))
    plt.barh(coef.index, coef.values, color=signed_colors(coef.values))
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Poids des 4 indices maison (coefficients standardisés)")
    plt.xlabel("poids dans la régression (rouge = ↑ stress, bleu = ↓ stress)")
    plt.tight_layout()
    out = FIGDIR / "03_coefficients_indices.png"
    plt.savefig(out, dpi=130)
    plt.close()
    print(f"[figure] {out.name}")
    print(f"[régression indices] R² (test 80-20) = {r2_test:.3f}")
    print(f"[régression indices] R² ({N_FOLDS}-fold) = {cv.mean():.3f} ± {cv.std():.3f}")
    return coef, r2_test, cv


# --------------------------------------------------------------------------- #
# 0. Problème 1 — preuve que le dataset synthétique ne dit rien (corrélations ≈ 0)
# --------------------------------------------------------------------------- #
def figure_probleme1():
    """Figure 0 (optionnelle) : matrice de corrélation du dataset SYNTHÉTIQUE abandonné.

    Ne s'exécute que si `Global_Mental_Health_Dataset_2025.csv` est présent. Montre
    que toutes les corrélations sont ≈ 0 : la signature de données fabriquées, et la
    raison pour laquelle l'équipe a changé de jeu de données (cf. storytelling).
    """
    if not SYNTH.exists():
        print("[problème 1] dataset synthétique absent -> figure 00 ignorée")
        return None

    df = pd.read_csv(SYNTH)
    order = {"Low": 0, "Medium": 1, "Moderate": 1, "High": 2, "Severe": 3}
    df["Stress_num"] = df["Stress_Level"].map(order)
    cols = ["Age", "Depression_Score", "Anxiety_Score", "Sleep_Hours",
            "Days_of_Treatment", "Stress_num"]
    corr = df[cols].corr()
    off = corr.where(~np.eye(len(cols), dtype=bool)).abs()
    cmax = float(np.nanmax(off.values))

    plt.figure(figsize=(6, 5))
    plt.imshow(corr.values, vmin=-1, vmax=1, cmap="coolwarm")
    plt.colorbar(label="corrélation de Pearson")
    plt.xticks(range(len(cols)), cols, rotation=45, ha="right")
    plt.yticks(range(len(cols)), cols)
    for i in range(len(cols)):
        for j in range(len(cols)):
            plt.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center",
                     color="black", fontsize=8)
    plt.title(f"Dataset synthétique : corrélations ≈ 0 (|r| max hors diag. = {cmax:.2f})")
    plt.tight_layout()
    out = FIGDIR / "00_probleme1_synthetique.png"
    plt.savefig(out, dpi=130)
    plt.close()
    print(f"[figure] {out.name}  (|r| max hors diagonale = {cmax:.3f})")
    return cmax


# --------------------------------------------------------------------------- #
# Programme principal
# --------------------------------------------------------------------------- #
def main():
    print("=" * 70)
    print("LE STRESS SE LIT-IL DANS NOTRE MODE DE VIE ?  —  analyse")
    print("=" * 70)

    cmax_synth = figure_probleme1()

    df, X, y = load_and_clean()
    corr_brut = figure_correlations(df)
    coef_base, r2_base = base_regression(X, y)
    features, corr_feat = build_handcrafted(df)
    coef_feat, r2_feat, cv = features_regression(features, y)

    # ------------------------------------------------------------------- #
    # RÉCAP — chiffres clés prêts à coller dans les slides / le rapport
    # ------------------------------------------------------------------- #
    top_up = coef_base.sort_values(ascending=False).head(4)
    top_down = coef_base.sort_values().head(4)
    print("\n" + "=" * 70)
    print("RÉCAP  (chiffres clés)")
    print("=" * 70)
    print(f"Dataset : {len(df)} lignes, {X.shape[1]} variables explicatives, cible 0-5.")
    if cmax_synth is not None:
        print(f"Problème 1 (synthétique) : |r| max ≈ {cmax_synth:.2f}  -> données fabriquées.")
    print(f"\nR² régression brute (test)      = {r2_base:.3f}")
    print(f"R² régression 4 indices (test)  = {r2_feat:.3f}")
    print(f"R² régression 4 indices (5-fold)= {cv.mean():.3f} ± {cv.std():.3f}")
    print("\nFeatures maison (corrélation au stress) :")
    for name, val in corr_feat.sort_values(ascending=False).items():
        print(f"    {name:16s} {val:+.3f}")
    print("\nFont MONTER le stress (coef. standardisés) :")
    for name, val in top_up.items():
        print(f"    {name:20s} {val:+.2f}")
    print("Font BAISSER le stress (coef. standardisés) :")
    for name, val in top_down.items():
        print(f"    {name:20s} {val:+.2f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
