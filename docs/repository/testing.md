# Strategie de test

## Etat actuel

Les dependances de test sont declarees dans `requirements-dev.txt` et pytest est configure dans `pyproject.toml` avec `DJANGO_SETTINGS_MODULE = config.settings`.

Tests automatises versionnes :

- `tests/test_homepage.py` : smoke test de la page `/`.
- `tests/test_accounts.py` : email comme identifiant, unicite email, hachage du mot de passe, authentification par email et branches du manager utilisateur.
- `tests/test_authentication_views.py` : labels francais, inscription, rejet email duplique, hachage via formulaire, connexion, echec de connexion, deconnexion POST, acces protege a `Mon espace` et fondation role utilisateur standard.
- `tests/test_concert_views.py` : filtrage du catalogue, informations des fiches, prix et stocks, CTA de connexion, motifs d'indisponibilite et reponses `404`.
- `tests/test_settings.py` : helpers de configuration d'environnement pour booleens et listes.
- `tests/test_core_domain.py` : regles de quantite, stock, concert reservable, panier mono-concert, panier vide/inactif, paiement simule accepte/refuse et prix snapshots.

Couverture officielle revendiquee dans cette etape :

- `EF3` : creation de compte avec email unique et mot de passe.
- `EF4` : connexion, deconnexion et acces a un espace personnel protege.
- `EF1` : catalogue limite aux concerts ouverts, futurs et avec stock.
- `EF2` : fiche avec titre, artiste, date, lieu, categories, prix et stock restant.
- `EM8` : email utilisateur unique, y compris rejet formulaire.
- `ENF3` : mot de passe gere par le hachage Django.
- `ENF4` : rejet propre d'un email deja utilise pendant l'inscription.
- `EM1` a `EM7`, `EM10`, `RG1` a `RG5` et `RG7` : couverture domaine/service, completee par les vues pour les etats de concert.
- `EF5`, `EF7`, `EF8`, `EF9` : couverture partielle domaine/service uniquement.
- `EF12` : decrement de stock apres paiement accepte au niveau service.
- `ENF6` : tests automatises executables sur la fondation technique et domaine.

`EM9` reste une fondation de role via `is_staff` / `is_superuser`, sans couverture revendiquee des permissions de gestion des concerts.
`ENF1` est partiellement couvert pour la consultation directe. Les confirmations, messages explicites de paiement, vues panier/paiement et historique restent hors couverture.

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
coverage report
```

Resultat observe : OK, 69 tests passent et `coverage.xml` est genere. La couverture locale affiche 99 % sur les chemins mesures, avec `concerts/views.py`, `concerts/urls.py` et `tests/test_concert_views.py` a 100 %.

## Exclusions de couverture

Les fichiers `config/asgi.py` et `config/wsgi.py` sont exclus de la couverture coverage.py et SonarCloud. Ce sont des entrypoints Django generes par `startproject`, sans logique applicative propre.

Les migrations restent exclues comme artefacts generes. Les fichiers applicatifs reels (`accounts`, `concerts`, `cart`, `orders`, `payments`, `config/settings.py`, `config/urls.py`) restent mesures.

## Regles de priorisation

Les premiers tests devront couvrir les exigences qui portent le plus de risque metier :

- EM1 / RG2 : ne jamais vendre plus que le stock.
- EM2 / EM3 / RG3 : quantite entre 1 et 6.
- EM6 / RG4 / RG5 : commande definitive seulement apres paiement accepte.
- RG8 : un utilisateur ne consulte que ses propres commandes.
- ENF3 : mots de passe jamais stockes en clair.
- EF3 / EF4 : parcours inscription, connexion, deconnexion et acces protege.

## Documentation des tests

Chaque test automatise devra etre relie a un ou plusieurs IDs officiels dans `docs/validation/matrice_tracabilite.md`.
