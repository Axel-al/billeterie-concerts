# Plan de test

## Objectif

Prouver progressivement que l'application respecte le cahier des charges, avec des tests relies aux IDs officiels et executables en local puis en CI.

## Etat actuel

Les premiers tests automatises sont versionnes dans `tests/`.

- `tests/test_homepage.py` verifie que la page `/` repond.
- `tests/test_accounts.py` verifie l'identifiant email, l'unicite email et le hachage des mots de passe.

Ces tests couvrent la fondation `EF3` partielle, `EM8`, `ENF3`, `ENF6` et alimentent la CI `ENF7`.

## Types de tests prevus

| Type | Cible | Outils | Exemples d'IDs |
| --- | --- | --- | --- |
| Unitaire | Regles metier pures ou services | pytest | EM1, EM2, EM3, EM6, EM7, RG2, RG3, RG4, RG5 |
| Integration Django | Modeles, formulaires, vues, permissions | pytest-django | EF3, EF4, EF5, EF8, EF9, EF10, EF11, RG6, RG8 |
| Fonctionnel | Parcours utilisateur complet | pytest-playwright | EF1, EF2, EF5, EF7, EF8, EF10, ENF1 |
| Qualite | Analyse statique et couverture | Ruff, coverage, SonarQube | ENF5, ENF6, ENF7 |

## Jeux de donnees cibles

- Concert ouvert avec plusieurs categories de places.
- Concert complet.
- Concert annule.
- Concert passe.
- Client avec panier vide et panier rempli.
- Administrateur.
- Paiement simule accepte et refuse.

## Criteres de sortie initiaux

- Toutes les regles critiques ont au moins un test automatise.
- La matrice de tracabilite relie chaque test a un ID officiel.
- Le pipeline CI execute les checks principaux.
- Les echecs de paiement et de stock ne modifient pas l'etat de facon irreversible.

## Commandes verifiees

```bash
pytest
pytest --cov=. --cov-report=xml
```

Resultat observe : OK, 4 tests passent.
