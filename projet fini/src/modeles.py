"""
modeles.py  ---  ETAPE 3 : regression + comparaison de modeles
==============================================================
Programme 3/3. Compare 4 modeles en VALIDATION CROISEE 5 plis :
  1. Lineaire (brut)            - reference
  2. Lineaire + log(prix)       - gere la decote exponentielle / l'asymetrie
  3. Lineaire + polynome (deg2) - courbure + interactions
  4. Random Forest              - reference non-lineaire (le "plafond")
Encodage : one-hot (transmission/fuelType/Make), target encoding (model).
Sorties : figures de comparaison + model_results.json.

Lancer :   python modeles.py
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

from sklearn.model_selection import train_test_split, cross_validate
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preparation import get_data, ROOT          # noqa: E402

try:
    from sklearn.preprocessing import TargetEncoder
    HAS_TE = True
except Exception:
    HAS_TE = False

FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 110

NUMERIC = ["car_age", "Odometer", "mileage_per_year", "engineSize", "mpg", "tax",
           "log_mileage", "age_x_mileage", "is_premium"]
ONEHOT = ["transmission", "fuelType", "Make"]


def save(fig, name):
    fig.tight_layout(); fig.savefig(os.path.join(FIG, name), bbox_inches="tight"); plt.close(fig)
    print(f"  [figure] {name}")


def pre(poly=False):
    steps = [("scale", StandardScaler())]
    if poly:
        steps = [("poly", PolynomialFeatures(degree=2, include_bias=False)), ("scale", StandardScaler())]
    tr = [("num", Pipeline(steps), NUMERIC),
          ("ohe", OneHotEncoder(handle_unknown="ignore", drop="first"), ONEHOT)]
    if HAS_TE:
        # target_type="continuous" : sinon sklearn prend les prix (entiers) pour des
        # milliers de classes -> encodage multiclasse, tres lent (et faux ici).
        tr.append(("te", TargetEncoder(target_type="continuous"), ["model"]))
    return ColumnTransformer(tr, remainder="drop")


def run():
    df, _ = get_data(verbose=False)
    print("3. MODELES - validation croisee 5 plis")
    cols = NUMERIC + ONEHOT + (["model"] if HAS_TE else [])
    X = df[cols]; y = df["price"].to_numpy(float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Lineaire (brut)": Pipeline([("pre", pre()), ("reg", LinearRegression())]),
        "Lineaire + log(prix)": TransformedTargetRegressor(
            regressor=Pipeline([("pre", pre()), ("reg", LinearRegression())]),
            func=np.log1p, inverse_func=np.expm1),
        "Lineaire + polynome (deg2)": Pipeline([("pre", pre(poly=True)), ("reg", LinearRegression())]),
        "Random Forest": Pipeline([("pre", pre()),
                                   ("reg", RandomForestRegressor(n_estimators=60, n_jobs=-1,
                                                                 max_depth=20, random_state=42))]),
    }

    rows, preds = [], {}
    for name, m in models.items():
        cv = cross_validate(m, Xtr, ytr, cv=5, n_jobs=1,
                            scoring=["r2", "neg_root_mean_squared_error", "neg_mean_absolute_error"])
        m.fit(Xtr, ytr); p = m.predict(Xte); preds[name] = p
        rows.append({"modele": name,
                     "R2_cv": round(cv["test_r2"].mean(), 3),
                     "R2_test": round(r2_score(yte, p), 3),
                     "RMSE_test": round(float(np.sqrt(mean_squared_error(yte, p))), 0),
                     "MAE_test": round(float(mean_absolute_error(yte, p)), 0)})
        print(f"   {name:28s} R2_cv={rows[-1]['R2_cv']:.3f}  RMSE={rows[-1]['RMSE_test']:,.0f}  MAE={rows[-1]['MAE_test']:,.0f}")
    res = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(data=res, x="R2_test", y="modele", ax=ax, color="#4C72B0")
    for i, v in enumerate(res["R2_test"]):
        ax.text(v, i, f"  {v:.3f}", va="center")
    ax.set_xlabel("R2 (test)"); ax.set_ylabel(""); ax.set_title("Comparaison des modeles")
    save(fig, "30_comparaison_modeles.png")

    best = res.loc[res["R2_test"].idxmax(), "modele"]; p = preds[best]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(yte, p, s=8, alpha=0.25, color="#4C72B0", edgecolor="none")
    lims = [0, np.percentile(yte, 99.5)]; ax.plot(lims, lims, "r--", lw=2)
    ax.set_xlim(lims); ax.set_ylim(lims)
    ax.set_xlabel("Prix reel"); ax.set_ylabel("Prix predit"); ax.set_title(f"Vrai vs predit - {best}")
    save(fig, "31_vrai_vs_predit.png")

    rf = models["Random Forest"]
    names = rf.named_steps["pre"].get_feature_names_out()
    imp = rf.named_steps["reg"].feature_importances_
    idx = np.argsort(imp)[::-1][:12]
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=imp[idx], y=[names[i].split("__")[-1] for i in idx], ax=ax, color="#55A868")
    ax.set_xlabel("Importance (Random Forest)"); ax.set_title("Variables les plus importantes")
    save(fig, "32_importance_variables.png")

    out = {"models": rows, "best_model": best,
           "rf_top": [{"feature": names[i].split("__")[-1], "importance": round(float(imp[i]), 3)} for i in idx]}
    with open(os.path.join(ROOT, "model_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"  -> meilleur modele : {best} ; model_results.json ecrit")


if __name__ == "__main__":
    run()
