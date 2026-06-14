# Plan de test

## Objectif

Prouver progressivement que l'application respecte le cahier des charges, avec des tests relies aux IDs officiels et executables en local puis en CI.

## Etat actuel

Les premiers tests automatises sont versionnes dans `tests/`.

- `tests/test_homepage.py` verifie que la page `/` repond.
- `tests/test_accounts.py` verifie l'identifiant email, l'unicite email et le hachage des mots de passe.
- `tests/test_authentication_views.py` verifie les labels francais, l'inscription, le rejet d'email duplique, le hachage via formulaire, la connexion, l'echec de connexion, la deconnexion POST, la protection de `Mon espace` et la fondation de role utilisateur standard.
- `tests/test_concert_views.py` verifie le filtrage du catalogue, les donnees affichees sur les fiches, les etats non reservables, le CTA de connexion et les reponses HTTP.
- `tests/test_booking_flow.py` verifie l'ajout au panier via la fiche, les bornes de quantite, les rejets stock/date/statut, le total panier, le paiement accepte/refuse, le decrement de stock, les prix snapshots et le cloisonnement des pages resultat.
- `tests/test_order_history.py` verifie l'historique des commandes payees, le detail de commande, les redirections de visiteurs, le cloisonnement proprietaire, les liens post-paiement et l'exclusion des commandes refusees.
- `tests/test_admin_concert_management.py` verifie les permissions d'administration, la synthese des ventes payees, l'annulation, la cloture, la preservation des commandes payees et la creation/modification admin de concerts avec categories.
- `tests/test_core_domain.py` verifie les premieres regles domaine : quantites, stock, statut de concert, panier mono-concert, paiement simule accepte/refuse et prix snapshots.
- `e2e/test_nominal_booking_flow.py` verifie en navigateur le parcours nominal : liste, fiche, connexion, ajout au panier, checkout, paiement accepte, confirmation et historique.

Ces tests couvrent `EF1` a `EF12`, `EM1` a `EM10`, `ENF1`, `ENF3`, `ENF4`, `ENF6`, `ENF7`, `RG1` a `RG8`. `EF10` et `RG8` sont couverts par l'historique paye et les pages detail filtrees par proprietaire. `EF11`, `EM9` et `RG7` sont couverts par les vues d'administration, l'admin Django et les tests de permissions. Le suivi admin des ventes ne releve pas de `RG8`, qui reste l'isolation des commandes des utilisateurs standards. `EF8`, `EF9`, `EM6`, `EM7`, `EM10`, `RG4` et `RG5` sont maintenus ou etendus par les tests de navigation et d'affichage, mais leur comportement coeur etait deja implemente par le parcours checkout/paiement. `ENF1` est couvert pour le parcours nominal par Playwright.

## Types de tests prevus

| Type | Cible | Outils | Exemples d'IDs |
| --- | --- | --- | --- |
| Unitaire | Regles metier pures ou services | pytest | EM1, EM2, EM3, EM6, EM7, RG2, RG3, RG4, RG5 |
| Integration Django | Modeles, formulaires, vues, permissions | pytest-django | EF1, EF2, EF3, EF4, EF5, EF6, EF7, EF8, EF9, EF10, EF11, EM9, RG1, RG6, RG7, RG8 |
| Fonctionnel | Parcours utilisateur complet | pytest-playwright, live_server | EF1, EF2, EF4, EF5, EF6, EF7, EF8, EF10, EF12, ENF1 |
| Qualite | Analyse statique et couverture | Ruff, coverage, SonarQube | ENF5, ENF6, ENF7 |

## Jeux de donnees cibles

- Concert ouvert avec plusieurs categories de places.
- Concert complet ou stock insuffisant.
- Concert annule.
- Concert passe.
- Concert ouvert sans stock.
- Concert brouillon non publie.
- Concert cloture par l'administration.
- Client avec panier vide et panier rempli.
- Client avec commande payee et tentative de paiement refusee.
- Visiteur creant un compte avec email unique ou email deja utilise.
- Client connecte puis deconnecte via POST.
- Administrateur.
- Gestionnaire autorise par permissions Django.
- Paiement simule accepte avec `4242424242424242` et refuse avec toute autre carte.
- Scenario e2e autonome avec utilisateur, concert ouvert et categories crees dans la base de test `pytest-django`, sans dependance a `db.sqlite3`.

## Criteres de sortie initiaux

- Toutes les regles critiques ont au moins un test automatise.
- La matrice de tracabilite relie chaque test a un ID officiel.
- Le pipeline CI execute les checks principaux.
- Les echecs de paiement et de stock ne modifient pas l'etat de facon irreversible.

## Commandes verifiees

```bash
ruff check .
pytest
python manage.py check
python manage.py makemigrations --check --dry-run
pytest --cov=. --cov-report=xml
pytest e2e --tracing=retain-on-failure --output=test-results/playwright
```

Resultat observe lors de la derniere verification complete : voir `docs/repository/current-state.md`.
