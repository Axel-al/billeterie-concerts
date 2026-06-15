# Plan de test

## Objectif

Prouver progressivement que l'application respecte le cahier des charges, avec des tests reliés aux IDs officiels et exécutables en local puis en CI.

## État actuel

Les premiers tests automatisés sont versionnés dans `tests/`.

- `tests/test_homepage.py` vérifie que la page `/` répond.
- `tests/test_accounts.py` vérifie l'identifiant e-mail, l'unicité e-mail et le hachage des mots de passe.
- `tests/test_authentication_views.py` vérifie les labels français, l'inscription, le rejet d'e-mail dupliqué, le hachage via formulaire, la connexion, l'échec de connexion, la déconnexion POST, la protection de `Mon espace` et la fondation de rôle utilisateur standard.
- `tests/test_concert_views.py` vérifie le filtrage du catalogue, les données affichées sur les fiches, les états non réservables, le CTA de connexion et les réponses HTTP.
- `tests/test_booking_flow.py` vérifie l'ajout au panier via la fiche, les bornes de quantité, les rejets stock/date/statut, le total panier, le paiement accepté/refusé, le décrément de stock, les prix snapshots et le cloisonnement des pages résultat.
- `tests/test_order_history.py` vérifie l'historique des commandes payées, le détail de commande, les redirections de visiteurs, le cloisonnement propriétaire, les liens post-paiement et l'exclusion des commandes refusées.
- `tests/test_admin_concert_management.py` vérifie les permissions d'administration, la synthèse des ventes payées, l'annulation, la clôture, la préservation des commandes payées et la création/modification admin de concerts avec catégories.
- `tests/test_core_domain.py` vérifie les règles domaine : quantités, stock, statut de concert, panier mono-concert, paiement simulé accepté/refusé, prix snapshots et rollback transactionnel si le décrément conditionnel du stock échoue.
- `e2e/test_nominal_booking_flow.py` vérifie en navigateur le parcours nominal : liste, fiche, connexion, ajout au panier, checkout, paiement accepté, confirmation et historique.
- `e2e/test_page_performance.py` mesure en Chromium le LCP de pages standards représentatives pour `ENF2` : accueil, catalogue, fiche concert et historique authentifié.

Ces tests couvrent `EF1` à `EF12`, `EM1` à `EM10`, `ENF1`, `ENF2`, `ENF3`, `ENF4`, `ENF6`, `ENF7`, `RG1` à `RG8`. `EF10` et `RG8` sont couverts par l'historique payé et les pages détail filtrées par propriétaire. `EF11`, `EM9` et `RG7` sont couverts par les vues d'administration, l'admin Django et les tests de permissions. Le suivi admin des ventes ne relève pas de `RG8`, qui reste l'isolation des commandes des utilisateurs standards. `EF8`, `EF9`, `EM6`, `EM7`, `EM10`, `RG4` et `RG5` sont maintenus ou étendus par les tests de navigation et d'affichage, mais leur comportement cœur était déjà implémenté par le parcours checkout/paiement. `EF12`, `EM1`, `EM6`, `ENF4`, `RG2` et `RG5` sont aussi vérifiés lors d'un échec du décrément conditionnel : la transaction est annulée, le stock et le panier restent inchangés, et aucune commande ni aucun paiement ne subsiste. `ENF1` est couvert pour le parcours nominal par Playwright. `ENF2` est couvert par une mesure LCP Chromium reproductible sous conditions contrôlées.

## Types de tests prévus

| Type | Cible | Outils | Exemples d'IDs |
| --- | --- | --- | --- |
| Unitaire | Règles métier pures ou services | pytest | EM1, EM2, EM3, EM6, EM7, RG2, RG3, RG4, RG5 |
| Intégration Django | Modèles, formulaires, vues, permissions | pytest-django | EF1, EF2, EF3, EF4, EF5, EF6, EF7, EF8, EF9, EF10, EF11, EM9, RG1, RG6, RG7, RG8 |
| Fonctionnel | Parcours utilisateur complet | pytest-playwright, live_server | EF1, EF2, EF4, EF5, EF6, EF7, EF8, EF10, EF12, ENF1 |
| Performance navigateur | Pages standards sous conditions contrôlées | pytest-playwright, Chromium, live_server | ENF2 |
| Qualité | Analyse statique et couverture | Ruff, coverage, SonarQube | ENF5, ENF6, ENF7 |

## Jeux de données cibles

- Concert ouvert avec plusieurs catégories de places.
- Concert complet ou stock insuffisant.
- Concert annulé.
- Concert passé.
- Concert ouvert sans stock.
- Concert brouillon non publié.
- Concert clôturé par l'administration.
- Client avec panier vide et panier rempli.
- Client avec commande payée et tentative de paiement refusée.
- Visiteur créant un compte avec e-mail unique ou e-mail déjà utilisé.
- Client connecté puis déconnecté via POST.
- Administrateur.
- Gestionnaire autorisé par permissions Django.
- Paiement simulé accepté avec `4242424242424242` et refusé avec toute autre carte.
- Échec simulé du décrément conditionnel de stock après validation du panier.
- Scénario e2e autonome avec utilisateur, concert ouvert et catégories créés dans la base de test `pytest-django`, sans dépendance à `db.sqlite3`.
- Données performance autonomes avec concert ouvert, catégories, utilisateur et commande payée, mesurées via `live_server` sans dépendance à `db.sqlite3` ni au CDN distant.

## Critères de sortie initiaux

- Toutes les règles critiques ont au moins un test automatisé.
- La matrice de traçabilité relie chaque test à un ID officiel.
- Le pipeline CI exécute les checks principaux.
- Les échecs de paiement et de stock ne modifient pas l'état de façon irréversible.
- Un échec du décrément atomique ne laisse ni commande, ni paiement, ni panier valide partiellement.
- `ENF2` dispose d'une mesure navigateur automatisable avec LCP `<= 2 000 ms`, résultats et limites documentées.

## Commandes vérifiées

```bash
ruff check .
pytest
python manage.py check
python manage.py makemigrations --check --dry-run
pytest --cov --cov-report=term-missing --cov-report=xml
pytest e2e --browser chromium --tracing=retain-on-failure --output=test-results/playwright -rP
```

La couverture mesure uniquement les packages applicatifs déclarés dans
`pyproject.toml`, avec branches et seuil global bloquant de 90 %. Ce seuil reste
un garde-fou et ne remplace pas la priorisation des règles métier critiques.

Résultat observé lors de la dernière vérification complète : voir
`docs/repository/current-state.md`.
