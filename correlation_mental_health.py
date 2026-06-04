import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)
df = pd.read_csv("Global_Mental_Health_Dataset_2025.csv")

# --- Encodage du niveau de stress (ordinal -> numérique) ---
order = {"Low": 0, "Medium": 1, "Moderate": 1, "High": 2, "Severe": 3}

# Garde-fou 1 : toutes les étiquettes sont-elles couvertes ?
# Sinon .map() renvoie des NaN SILENCIEUX qui faussent les corrélations.
uniques = df["Stress_Level"].dropna().unique()
non_mappees = [v for v in uniques if v not in order]
if non_mappees:
    raise ValueError(f"Étiquettes non prévues dans `order` : {non_mappees}")

df["Stress_num"] = df["Stress_Level"].map(order)

cols = ["Age", "Depression_Score", "Anxiety_Score", "Sleep_Hours",
        "Days_of_Treatment", "Stress_num"]

# Garde-fou 2 : combien de NaN ? (.corr() les supprime en pairwise, en silence)
print("NaN par colonne :\n", df[cols].isna().sum(), sep="")
print("Lignes complètes :", df[cols].dropna().shape[0], "/", len(df))

# Garde-fou 3 : Pearson (linéaire) ET Spearman (monotone).
# Pearson ≈ 0 ne prouve QUE l'absence de relation linéaire.
corr   = df[cols].corr(method="pearson")
corr_s = df[cols].corr(method="spearman")

print("\nMatrice de Pearson :\n", corr.round(2), sep="")
print("\nMatrice de Spearman :\n", corr_s.round(2), sep="")
print("Sommeil vs stress (Pearson) :", round(corr.loc["Sleep_Hours", "Stress_num"], 3))

# Garde-fou 4 : on regarde AUSSI toutes les colonnes numériques (anti cherry-pick)
num = df.select_dtypes(include=[np.number])
full_off = num.corr().where(~np.eye(num.shape[1], dtype=bool)).abs()
print("Sur TOUTES les colonnes numériques, |r| max :",
      round(float(np.nanmax(full_off.values)), 3))


def plot_corr(corr, titre, chemin, label_cbar):
    """Heatmap triangle inférieur strict (diagonale + triangle sup. masqués)."""
    cmax = float(np.nanmax(corr.where(~np.eye(len(corr), dtype=bool)).abs().values))

    mask = np.triu(np.ones_like(corr.values, dtype=bool))   # diag + triangle sup.
    corr_plot = np.ma.masked_array(corr.values, mask=mask)

    cmap = plt.cm.coolwarm.copy()
    cmap.set_bad("white")                                   # cases masquées en blanc

    plt.figure(figsize=(6.5, 5))
    plt.imshow(corr_plot, vmin=-1, vmax=1, cmap=cmap)
    plt.colorbar(label=label_cbar)
    plt.xticks(range(len(corr)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr)), corr.columns)

    for i in range(len(corr)):
        for j in range(len(corr)):
            if i > j:                                       # triangle inférieur strict
                plt.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center",
                         color="black", fontsize=8)

    plt.title(f"{titre}\n(|r| max = {cmax:.2f})", fontsize=10, pad=10)
    plt.tight_layout()
    plt.savefig(chemin, dpi=130)
    plt.close()
    return cmax


cmax = plot_corr(corr, "Dataset synthétique : corrélations ≈ 0 (Pearson)",
                 "figures/00_probleme1_synthetique.png",
                 "corrélation de Pearson")
cmax_s = plot_corr(corr_s, "Dataset synthétique : corrélations ≈ 0 (Spearman)",
                   "figures/00_probleme1_spearman.png",
                   "corrélation de Spearman (rho)")

print("\nPearson  |r|   max (hors diag.) :", round(cmax, 3))
print("Spearman |rho| max (hors diag.) :", round(cmax_s, 3))
print("Figures enregistrées :")
print("  figures/00_probleme1_synthetique.png")
print("  figures/00_probleme1_spearman.png")
