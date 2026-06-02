# 🎤 Oral (5 min) — « Le stress se lit-il dans notre mode de vie ? »
### Squelette des 5 slides + script + Q&A (CHIFFRES RÉELS intégrés)

> Minutage : S1≈45 s · S2≈55 s · S3≈80 s · S4≈80 s · S5≈40 s ≈ **5 min**.

---

## SLIDE 1 — Business goal  *(titre « question »)*
### Titre : « Et si notre mode de vie trahissait notre stress ? »

**Sur la slide :**
- 🎯 Notre question : *quels facteurs du quotidien expliquent le **stress** ?*
- 😕 1er essai : un dataset « santé mentale » qui ne disait **rien** (corrélations ≈ 0 → **synthétique**).
- ✅ Notre choix : une **vraie enquête** bien-être — **15 971 personnes** (Authentic-Happiness).
- 💡 Utile : applis bien-être, prévention santé, qualité de vie au travail.

**À dire :** « On voulait comprendre ce qui stresse les gens. Premier piège : un dataset "santé mentale" parfait en apparence, mais aucune variable n'en expliquait une autre — des données **générées artificiellement**. Pire, tout le thème en est rempli. On a donc pris une **vraie enquête** sur près de 16 000 personnes, pour répondre à : *qu'est-ce qui fait monter notre stress ?* »

---

## SLIDE 2 — Data description  *(titre « descriptif »)*
### Titre : « 15 971 vies, 23 variables, un seul chiffre à expliquer »

**Sur la slide :**
- 📊 Source **réelle** Authentic-Happiness · **15 971 lignes** · **23 variables**.
- 🎯 Cible : `DAILY_STRESS`, score **0 → 5**.
- 🔢 ~20 variables numériques (sommeil, vie sociale, méditation, congés non pris…) + 2 catégorielles (Âge, Genre).
- 🧹 Nettoyage : 1 valeur cassée corrigée, **one-hot** Âge/Genre, **standardisation**.
- 🖼️ *Figure : `figures/01_correlations.png`*

**À dire :** « Données **réelles et auto-déclarées** : chacun a rempli un questionnaire. On explique une seule chose, le **stress de 0 à 5**. Comme toute vraie donnée, elle est imparfaite : une valeur à corriger, des catégories à encoder, des échelles à harmoniser. Premier constat sur la heatmap : **aucune variable seule** ne ressort vraiment. »

---

## SLIDE 3 — Handcrafted features  *(le cœur du projet)*
### Titre : « 4 indices maison — dont un qui nous a surpris »

**Sur la slide :**
| Feature maison | Construction | Corrélation au stress |
|---|---|---|
| **OVERWORK** | congés non pris + irritabilité − passions | **+0.35** ✅ (le + fort !) |
| **HEALTHY_HABITS** | sommeil + activité + méditation + fruits | **−0.22** ✅ |
| **SLEEP × FLOW** | sommeil **×** immersion *(produit, type « Pclass×Age »)* | **−0.16** ✅ |
| **SOCIAL_SUPPORT** | entourage + réseau + entraide | **−0.06** ❌ (raté !) |

- 💡 **Pourquoi l'échec ?** réseau (+0.09) et entraide (+0.06) vont avec **plus** de stress → ils annulent l'effet de l'entourage proche.

**À dire :** « Le vrai travail est ici : on combine les variables en 4 indices. Trois marchent très bien — surtout **OVERWORK, le surmenage, meilleur signal de toute l'étude** (+0.35). Mais le quatrième, le **soutien social**, échoue (−0.06) ! En creusant, on comprend : avoir un grand réseau et beaucoup aider les autres vont avec **plus** de stress, ce qui annule l'effet des proches. Leçon : **une feature combinée ne vaut que si ses composantes vont dans le même sens** — et c'est la vérification qui permet de le voir. »

---

## SLIDE 4 — Regression  *(titre « affirmation »)*
### Titre : « Le stress se lit dans nos habitudes — à 19 % »

**Sur la slide :**
- ⚙️ Régression **linéaire**, split **80-20** + **5-fold**.
- 📈 R² (23 variables) = **0.19** · R² (4 indices) = **0.13** · 5-fold = **0.14 ± 0.01** (stable).
- 🔴 **Montent** le stress : irritabilité **+0.32**, congés non pris **+0.18**.
- 🔵 **Baissent** le stress : méditation **−0.15**, sommeil **−0.13**, revenu suffisant **−0.12**, temps passions **−0.09**.
- 🖼️ *Figure : `figures/02_coefficients_base.png`*

**À dire :** « Le mode de vie explique ~**19 %** du stress — modeste mais réel : le stress est multifactoriel, c'est **honnête**. Le facteur le plus fort, l'irritabilité, est en partie un *symptôme* du stress (prudence). Le plus **actionnable** : ne pas prendre ses congés. À l'inverse, méditer, dormir, un revenu suffisant et du temps pour soi apaisent. Et la validation 5-fold est très stable : pas de surapprentissage. »

---

## SLIDE 5 — Conclusion  *(boucle le récit)*
### Titre : « Des données réelles racontent une histoire — même quand elles nous contredisent »

**Sur la slide :**
- ✅ Leviers **actionnables** : congés, méditation, sommeil, temps pour ses passions.
- 🏆 Notre feature **OVERWORK** = meilleur prédicteur (+0.35).
- 💡 Un **échec** riche : `SOCIAL_SUPPORT` rappelle qu'une hypothèse se **vérifie** (corrélation ≠ intuition).
- ⚠️ Limites : auto-déclaré, échelle 0-5, **corrélation ≠ causalité**.
- 🚀 Pistes : régression ordinale, revoir le soutien social, segmenter par âge.

**À dire :** « On a identifié des leviers concrets, et notre indice de surmenage est le meilleur prédicteur. Mais notre plus belle leçon vient d'un **échec** : le soutien social, pourtant attendu protecteur, n'explique rien ici — il a fallu l'accepter et le comprendre. C'est ça, travailler de vraies données : elles racontent une histoire, même quand elle contredit nos intuitions. Des données fabriquées, elles, ne racontent rien. Merci. »

---

## 🛡️ Q&A anticipé (les 5 min de questions)
- **Pourquoi linéaire et pas logistique ?** → cible 0-5 continue + on veut **interpréter** les coefficients ; la logistique = piste d'amélioration.
- **R² de 0.19, c'est faible, non ?** → le stress est **multifactoriel** et auto-déclaré ; un R² modéré est **honnête**. On vise l'explication, pas la prédiction. La validation 5-fold (±0.01) montre que c'est **stable**.
- **L'irritabilité (+0.32), n'est-ce pas circulaire ?** → si, en partie : crier/bouder est aussi un *symptôme* du stress. C'est pourquoi on met en avant le levier **actionnable** = congés non pris.
- **Pourquoi garder une feature qui a échoué ?** → justement pour montrer la **démarche** : on vérifie la pertinence, et l'échec de `SOCIAL_SUPPORT` nous a appris pourquoi (composantes contradictoires).
- **Données vraiment réelles ?** → enquête identifiée + imperfections du réel ; le 1er dataset avait des corrélations ≈ 0 = signature du synthétique.
- **Circularité du score ?** → on a **retiré** `WORK_LIFE_BALANCE_SCORE` (somme des colonnes → R²=1 trompeur).

---
*Rappel : 5 slides (1 par thème), dépôt **Git** (URL dans le rapport), slides sur Moodle jeudi soir.*
