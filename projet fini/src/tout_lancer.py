"""
tout_lancer.py  ---  lance TOUT le pipeline et ecrit RESULTS.md
===============================================================
    python tout_lancer.py
Execute : preparation -> eda (graphes) -> modeles (comparaison), puis
fusionne les chiffres dans ../RESULTS.md (pret pour le rapport et les slides).
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preparation import get_data, ROOT, REFERENCE_YEAR     # noqa: E402
import eda          # noqa: E402
import modeles      # noqa: E402


def write_results_md():
    eda_r = json.load(open(os.path.join(ROOT, "eda_results.json"), encoding="utf-8"))
    mod_r = json.load(open(os.path.join(ROOT, "model_results.json"), encoding="utf-8"))
    L = ["# Resultats (genere par tout_lancer.py)\n",
         f"Annee de reference (age) : {REFERENCE_YEAR}\n",
         "\n## 1. Pertinence des variables (R2 univarie avec le prix)\n",
         "| Variable | R2 | correlation |", "|---|---|---|"]
    for r in eda_r["relevance"]:
        L.append(f"| {r['feature']} | {r['r2']} | {r['corr']:+.2f} |")

    L += ["\n## 2. Graphe variable -> prix : le lineaire suffit-il ?\n",
          "| Variable | R2 lineaire | meilleur ajustement | R2 meilleur |", "|---|---|---|---|"]
    for r in eda_r["univariate"]:
        rl = "-" if r["r2_lin"] is None else f"{r['r2_lin']}"
        L.append(f"| {r['feature']} | {rl} | {r['best']} | {r['r2_best']} |")

    L += ["\n## 3. Comparaison des modeles (validation croisee 5 plis)\n",
          "| Modele | R2 (CV) | R2 (test) | RMSE test (GBP) | MAE test (GBP) |", "|---|---|---|---|---|"]
    for r in mod_r["models"]:
        L.append(f"| {r['modele']} | {r['R2_cv']} | {r['R2_test']} | {r['RMSE_test']:,.0f} | {r['MAE_test']:,.0f} |")
    L.append(f"\n**Meilleur modele : {mod_r['best_model']}.**\n")

    L.append("\n## 4. Variables les plus importantes (Random Forest)\n")
    for r in mod_r["rf_top"][:8]:
        L.append(f"- {r['feature']} : {r['importance']}")

    L.append("\n## 5. Correlation avec le prix\n")
    for k, v in sorted(eda_r["corr_with_price"].items(), key=lambda kv: -abs(kv[1])):
        L.append(f"- {k} : {v:+.2f}")

    open(os.path.join(ROOT, "RESULTS.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n=> RESULTS.md ecrit")


if __name__ == "__main__":
    print("=" * 60); print("PIPELINE COMPLET"); print("=" * 60)
    get_data()          # etape 1 (imprime le rapport de nettoyage)
    eda.run()           # etape 2
    modeles.run()       # etape 3
    write_results_md()
    print("\nTERMINE. Figures dans figures/ , chiffres dans RESULTS.md")
