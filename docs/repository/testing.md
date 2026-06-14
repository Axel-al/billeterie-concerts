# Strategie de test

## Etat actuel

Les dependances de test sont declarees dans `requirements-dev.txt` et pytest est configure dans `pyproject.toml` avec `DJANGO_SETTINGS_MODULE = config.settings`.

Tests automatises versionnes :

- `tests/test_homepage.py` : smoke test de la page `/`.
- `tests/test_accounts.py` : email comme identifiant, unicite email, hachage du mot de passe, authentification par email et branches du manager utilisateur.
- `tests/test_authentication_views.py` : labels francais, inscription, rejet email duplique, hachage via formulaire, connexion, echec de connexion, deconnexion POST, acces protege a `Mon espace` et fondation role utilisateur standard.
- `tests/test_concert_views.py` : filtrage du catalogue, informations des fiches, prix et stocks, CTA de connexion, motifs d'indisponibilite et reponses `404`.
- `tests/test_booking_flow.py` : ajout au panier via la fiche, bornes de quantite, rejet stock/date/statut, affichage du total, paiement accepte/refuse, decrement de stock, prix snapshots et cloisonnement utilisateur des pages panier/checkout/resultat.
- `tests/test_order_history.py` : historique des commandes payees, detail de commande, redirection des visiteurs, cloisonnement proprietaire, exclusion des commandes refusees et liens post-paiement.
- `tests/test_admin_concert_management.py` : permissions d'administration, synthese des ventes payees, annulation, cloture, preservation des commandes payees et creation/modification admin de concerts avec categories.
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
- `EM1` a `EM7`, `EM10`, `RG1` a `RG5` et `RG7` : couverture domaine/service, completee par les vues pour les etats de concert, le parcours panier/paiement, l'administration et l'affichage des commandes.
- `EF5`, `EF6`, `EF7`, `EF8`, `EF9` : couverture par services et vues Django.
- `EF12` : decrement de stock apres paiement accepte au niveau service.
- `RG6` : checkout et paiement proteges par authentification.
- `EF10` et `RG8` : couverture par l'historique des commandes payees et le detail de commande filtres par utilisateur.
- `EF11` et `EM9` : couverture par les vues admin protegees par permissions et l'admin Django.
- `ENF6` : tests automatises executables sur la fondation technique et domaine.

Le suivi admin des ventes ne releve pas de `RG8`; `RG8` reste limite a l'acces des utilisateurs standards a leurs propres commandes.
`ENF1` est partiellement couvert pour la consultation directe et le parcours fiche -> panier -> paiement -> commandes.

## Couches prevues

| Couche | Objectif | Exemples cibles |
| --- | --- | --- |
| Tests unitaires | Valider les regles metier isolees. | quantite 1 a 6, stock disponible, prix fige a la validation |
| Tests d'integration Django | Valider modeles, vues, formulaires, ORM et permissions. | creation de compte unique, ajout panier, paiement accepte/refuse, pages resultat, historique filtre et administration concerts/ventes |
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

Resultat observe : OK, 103 tests passent et `coverage.xml` est genere. La couverture locale affiche 98 % sur les chemins mesures, avec `cart/services.py`, `cart/views.py`, `concerts/services.py`, `orders/views.py`, `payments/views.py`, `tests/test_admin_concert_management.py`, `tests/test_booking_flow.py` et `tests/test_order_history.py` a 100 %.

## Exclusions de couverture

Les fichiers `config/asgi.py` et `config/wsgi.py` sont exclus de la couverture coverage.py et SonarCloud. Ce sont des entrypoints Django generes par `startproject`, sans logique applicative propre.

Les migrations restent exclues comme artefacts generes. Les fichiers applicatifs reels (`accounts`, `concerts`, `cart`, `orders`, `payments`, `config/settings.py`, `config/urls.py`) restent mesures.

## Regles de priorisation

Les premiers tests devront couvrir les exigences qui portent le plus de risque metier :

- EM1 / RG2 : ne jamais vendre plus que le stock.
- EM2 / EM3 / RG3 : quantite entre 1 et 6.
- EM6 / RG4 / RG5 : commande definitive seulement apres paiement accepte.
- RG8 : un utilisateur ne consulte que ses propres commandes ou pages de resultat.
- EF11 / EM9 / RG7 : seules les permissions admin adaptees permettent de gerer ou annuler un concert.
- ENF3 : mots de passe jamais stockes en clair.
- EF3 / EF4 : parcours inscription, connexion, deconnexion et acces protege.

## Documentation des tests

Chaque test automatise devra etre relie a un ou plusieurs IDs officiels dans `docs/validation/matrice_tracabilite.md`.

Pour l'historique, `EF10` et `RG8` sont couverts par les pages de commandes payees et detail filtrees par proprietaire. Pour l'administration, `EF11`, `EM9` et `RG7` sont couverts par `tests/test_admin_concert_management.py`. `EF8`, `EF9`, `EM6`, `EM7`, `EM10`, `RG4` et `RG5` sont maintenus ou etendus par les tests de navigation et d'affichage, mais leur comportement coeur reste porte par le parcours checkout/paiement.
