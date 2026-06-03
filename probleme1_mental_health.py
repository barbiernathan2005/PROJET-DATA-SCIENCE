# -*- coding: utf-8 -*-
"""
probleme1_mental_health.py
==========================
Génère la figure du « Problème 1 » : la matrice de corrélation du dataset
SYNTHÉTIQUE de santé mentale (`Global_Mental_Health_Dataset_2025.csv`).

But : montrer que toutes les corrélations sont ≈ 0 — la signature de données
fabriquées, et la raison pour laquelle nous avons changé de sujet (voir le rapport).

    python probleme1_mental_health.py   ->   figures/00_probleme1_synthetique.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

df = pd.read_csv("Global_Mental_Health_Dataset_2025.csv")

# On encode le niveau de stress en nombre pour pouvoir le corréler aux autres variables.
order = {"Low": 0, "Medium": 1, "Moderate": 1, "High": 2, "Severe": 3}
df["Stress_num"] = df["Stress_Level"].map(order)

cols = ["Age", "Depression_Score", "Anxiety_Score", "Sleep_Hours",
        "Days_of_Treatment", "Stress_num"]
corr = df[cols].corr()

# Corrélation maximale (hors diagonale) : doit être proche de 0.
off = corr.where(~np.eye(len(cols), dtype=bool)).abs()
cmax = float(np.nanmax(off.values))
print("Corrélation |r| max (hors diagonale) :", round(cmax, 3))
print("Sommeil vs stress :", round(corr.loc["Sleep_Hours", "Stress_num"], 3))

plt.figure(figsize=(6, 5))
plt.imshow(corr.values, vmin=-1, vmax=1, cmap="coolwarm")
plt.colorbar(label="corrélation de Pearson")
plt.xticks(range(len(cols)), cols, rotation=45, ha="right")
plt.yticks(range(len(cols)), cols)
for i in range(len(cols)):
    for j in range(len(cols)):
        plt.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center",
                 color="black", fontsize=8)
plt.title(f"Dataset synthétique : corrélations ≈ 0 (|r| max = {cmax:.2f})")
plt.tight_layout()
plt.savefig("figures/00_probleme1_synthetique.png", dpi=130)
plt.close()
print("Figure enregistrée : figures/00_probleme1_synthetique.png")
