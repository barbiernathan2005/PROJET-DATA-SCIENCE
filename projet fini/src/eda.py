"""
eda.py  ---  ETAPE 2 : analyse exploratoire + graphes
=====================================================
Programme 2/3. Pour CHAQUE variable, trace le graphe variable -> prix avec la
REGRESSION LA PLUS ADAPTEE, verifie la PERTINENCE des handcrafted features,
trace les correlations et les distributions. Enregistre tout dans figures/ et
les chiffres dans eda_results.json.

Lancer :   python eda.py
"""
import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preparation import get_data, ROOT          # noqa: E402

FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 110
OUT = {"figures": []}


def save(fig, name, caption):
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, name), bbox_inches="tight")
    plt.close(fig)
    OUT["figures"].append({"file": name, "caption": caption})
    print(f"  [figure] {name}")


def fit_curves(x, y):
    out = {}
    c1 = np.polyfit(x, y, 1)
    out["lineaire"] = (r2_score(y, np.polyval(c1, x)), lambda g, c=c1: np.polyval(c, g))
    c2 = np.polyfit(x, y, 2)
    out["polynomiale"] = (r2_score(y, np.polyval(c2, x)), lambda g, c=c2: np.polyval(c, g))
    if (x > 0).all():
        lx = np.log(x)
        cl = np.polyfit(lx, y, 1)
        out["logarithmique"] = (r2_score(y, np.polyval(cl, lx)),
                                lambda g, c=cl: np.polyval(c, np.log(np.clip(g, 1e-9, None))))
    return out


def plot_numeric(df, col, label, fname):
    x = df[col].to_numpy(float); y = df["price"].to_numpy(float)
    fits = fit_curves(x, y)
    r2_lin = fits["lineaire"][0]
    best = max(fits, key=lambda k: fits[k][0]); r2_best = fits[best][0]
    s = df.sample(min(4000, len(df)), random_state=0)
    grid = np.linspace(x.min(), x.max(), 200)
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.scatter(s[col], s["price"], s=8, alpha=0.25, color="#4C72B0", edgecolor="none")
    ax.plot(grid, fits["lineaire"][1](grid), color="#C44E52", lw=2, label=f"lineaire (R2={r2_lin:.2f})")
    if best != "lineaire":
        ax.plot(grid, fits[best][1](grid), color="#55A868", lw=2.4, ls="--",
                label=f"{best} (R2={r2_best:.2f})")
    ax.set_xlabel(label); ax.set_ylabel("Prix (GBP)")
    ax.set_ylim(0, np.percentile(y, 99))
    ax.set_title(f"Prix en fonction de : {label}")
    ax.legend(loc="upper right", framealpha=0.9)
    save(fig, fname, f"Prix vs {label} ; meilleur ajustement = {best} (R2={r2_best:.2f}).")
    return {"feature": label, "r2_lin": round(r2_lin, 3), "best": best, "r2_best": round(r2_best, 3)}


def plot_categorical(df, col, label, fname, top=None):
    g = df.groupby(col)["price"].agg(["mean", "count"]).sort_values("mean", ascending=False)
    if top:
        g = g.head(top)
    fig, ax = plt.subplots(figsize=(7, max(3.2, 0.34 * len(g) + 1)))
    sns.barplot(x=g["mean"], y=[str(i) for i in g.index], ax=ax, color="#4C72B0")
    for i, (m, c) in enumerate(zip(g["mean"], g["count"])):
        ax.text(m, i, f"  {m:,.0f} (n={c})", va="center", fontsize=8)
    ax.set_xlabel("Prix moyen (GBP)"); ax.set_ylabel(label)
    ax.set_title(f"Prix moyen par {label}")
    save(fig, fname, f"Prix moyen par {label}.")
    pred = df[col].map(df.groupby(col)["price"].mean())
    return {"feature": label, "r2_lin": None, "best": "moyenne/groupe",
            "r2_best": round(r2_score(df["price"], pred), 3)}


def run():
    df, _ = get_data(verbose=False)
    print("2. EDA - graphes variable -> prix")

    # distribution prix (justifie log)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    sns.histplot(df["price"], bins=60, ax=ax[0], color="#4C72B0"); ax[0].set_title("Distribution du prix")
    sns.histplot(np.log1p(df["price"]), bins=60, ax=ax[1], color="#55A868"); ax[1].set_title("log(prix) ~ symetrique")
    save(fig, "00_distribution_prix.png", "Prix tres asymetrique a droite ; log(prix) quasi symetrique.")

    table = []
    numeric = [("car_age", "Age (annees)"), ("Odometer", "Kilometrage (mi)"),
               ("mileage_per_year", "Km par an"), ("engineSize", "Cylindree (L)"),
               ("mpg", "Consommation (mpg)"), ("tax", "Taxe (GBP)")]
    for i, (c, l) in enumerate(numeric, 1):
        table.append(plot_numeric(df, c, l, f"{i:02d}_num_{c}.png"))

    cats = [("Make", "Marque", None), ("transmission", "Transmission", None),
            ("fuelType", "Carburant", None), ("is_premium", "Premium (0/1)", None),
            ("model", "Modele (top 15)", 15)]
    for j, (c, l, t) in enumerate(cats, 10):
        table.append(plot_categorical(df, c, l, f"{j:02d}_cat_{c}.png", t))
    OUT["univariate"] = table
    print(pd.DataFrame(table).to_string(index=False))

    # PERTINENCE des handcrafted features : R2 univarie (lineaire) de chacune
    feats = ["car_age", "mileage_per_year", "log_mileage", "age_x_mileage",
             "is_premium", "engineSize", "Odometer", "mpg", "tax"]
    rel = []
    y = df["price"].to_numpy(float)
    for f in feats:
        x = df[f].to_numpy(float)
        c = np.polyfit(x, y, 1)
        rel.append({"feature": f, "r2": round(r2_score(y, np.polyval(c, x)), 3),
                    "corr": round(float(np.corrcoef(x, y)[0, 1]), 3)})
    rel = sorted(rel, key=lambda d: -d["r2"])
    OUT["relevance"] = rel
    fig, ax = plt.subplots(figsize=(8, 4.6))
    sns.barplot(x=[r["r2"] for r in rel], y=[r["feature"] for r in rel], ax=ax, color="#55A868")
    for i, r in enumerate(rel):
        ax.text(r["r2"], i, f"  R2={r['r2']}", va="center", fontsize=8)
    ax.set_xlabel("R2 univarie (prix)"); ax.set_title("Pertinence des features (dont handcrafted)")
    save(fig, "20_pertinence_features.png", "R2 univarie de chaque variable (verifie la pertinence des features).")

    # synthese lineaire vs meilleur ajustement (numerique)
    num = [t for t in table if t["r2_lin"] is not None]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    yy = np.arange(len(num))
    ax.barh(yy + 0.2, [t["r2_lin"] for t in num], 0.4, color="#C44E52", label="lineaire")
    ax.barh(yy - 0.2, [t["r2_best"] for t in num], 0.4, color="#55A868", label="meilleur")
    ax.set_yticks(yy); ax.set_yticklabels([t["feature"] for t in num])
    ax.set_xlabel("R2 univarie"); ax.set_title("Le lineaire suffit-il ? lineaire vs meilleur ajustement")
    ax.legend()
    save(fig, "21_lineaire_vs_best.png", "Plusieurs variables : un ajustement non-lineaire bat le lineaire.")

    # correlations
    num_cols = ["price", "car_age", "Odometer", "mileage_per_year", "engineSize", "mpg", "tax", "is_premium"]
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(7.5, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0, ax=ax)
    ax.set_title("Correlations (numeriques)")
    save(fig, "22_correlations.png", "Matrice de correlation.")
    OUT["corr_with_price"] = corr["price"].drop("price").round(3).to_dict()

    with open(os.path.join(ROOT, "eda_results.json"), "w", encoding="utf-8") as f:
        json.dump(OUT, f, indent=2, ensure_ascii=False)
    print("  -> eda_results.json ecrit")


if __name__ == "__main__":
    run()
