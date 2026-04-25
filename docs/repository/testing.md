# Strategie de test

## Etat actuel

Les dependances de test sont declarees dans `requirements-dev.txt` et pytest est configure dans `pyproject.toml` avec `DJANGO_SETTINGS_MODULE = config.settings`.

Tests automatises versionnes :

- `tests/test_homepage.py` : smoke test de la page `/`.
- `tests/test_accounts.py` : email comme identifiant, unicite email et mot de passe hashe.

Couverture officielle revendiquee dans cette etape :

- `EM8` : email utilisateur unique.
- `ENF3` : mot de passe gere par le hachage Django.
- `ENF6` : tests automatises executables sur la fondation.

`EF3` reste partiellement couvert seulement cote modele utilisateur ; il n'existe pas encore de parcours d'inscription.

## Couches prevues

| Couche | Objectif | Exemples cibles |
| --- | --- | --- |
| Tests unitaires | Valider les regles metier isolees. | quantite 1 a 6, stock disponible, prix fige a la validation |
| Tests d'integration Django | Valider modeles, vues, formulaires, ORM et permissions. | creation de compte unique, ajout panier, paiement accepte/refuse |
| Tests fonctionnels Playwright | Valider un parcours utilisateur complet. | consultation, connexion, ajout panier, paiement accepte, historique |
| Couverture | Mesurer la part du code exercee. | rapport XML pour CI et SonarQube |
| Analyse statique | Detecter les erreurs et problemes de style. | `ruff check .` |

## Commandes cibles

```bash
ruff check .
pytest
pytest --cov=. --cov-report=xml
pytest e2e
```

La commande `pytest e2e` reste cible future. La CI installe Chromium pour Playwright, mais saute proprement les tests e2e tant que le dossier `e2e/` n'existe pas.

## Commandes verifiees localement

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
ruff check .
pytest
pytest --cov=. --cov-report=xml
```

Resultat observe : OK, 4 tests passent et `coverage.xml` est genere.

## Regles de priorisation

Les premiers tests devront couvrir les exigences qui portent le plus de risque metier :

- EM1 / RG2 : ne jamais vendre plus que le stock.
- EM2 / EM3 / RG3 : quantite entre 1 et 6.
- EM6 / RG4 / RG5 : commande definitive seulement apres paiement accepte.
- RG8 : un utilisateur ne consulte que ses propres commandes.
- ENF3 : mots de passe jamais stockes en clair.

## Documentation des tests

Chaque test automatise devra etre relie a un ou plusieurs IDs officiels dans `docs/validation/matrice_tracabilite.md`.
