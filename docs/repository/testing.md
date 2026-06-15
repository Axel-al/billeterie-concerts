# Stratégie de test

## État actuel

Les dépendances de test sont déclarées dans `requirements-dev.txt` et pytest est configuré dans `pyproject.toml` avec `DJANGO_SETTINGS_MODULE = config.settings`.

Tests automatisés versionnés :

- `tests/test_homepage.py` : smoke test de la page `/`.
- `tests/test_accounts.py` : e-mail comme identifiant, unicité e-mail, hachage du mot de passe, authentification par e-mail et branches du manager utilisateur.
- `tests/test_authentication_views.py` : labels français, inscription, rejet d'e-mail dupliqué, hachage via formulaire, connexion, échec de connexion, déconnexion POST, accès protégé à `Mon espace` et fondation rôle utilisateur standard.
- `tests/test_concert_views.py` : filtrage du catalogue, informations des fiches, prix et stocks, CTA de connexion, motifs d'indisponibilité et réponses `404`.
- `tests/test_booking_flow.py` : ajout au panier via la fiche, bornes de quantité, rejet stock/date/statut, affichage du total, paiement accepté/refusé, décrément de stock, prix snapshots et cloisonnement utilisateur des pages panier/checkout/résultat.
- `tests/test_order_history.py` : historique des commandes payées, détail de commande, redirection des visiteurs, cloisonnement propriétaire, exclusion des commandes refusées et liens post-paiement.
- `tests/test_admin_concert_management.py` : permissions d'administration, synthèse des ventes payées, annulation, clôture, préservation des commandes payées et création/modification admin de concerts avec catégories.
- `tests/test_settings.py` : helpers de configuration d'environnement pour booléens et listes.
- `tests/test_template_quality.py` : empreintes SRI des ressources Bootstrap et absence de rôles `status` sur les messages statiques.
- `tests/test_core_domain.py` : règles de quantité, stock, concert réservable, panier mono-concert, panier vide/inactif, paiement simulé accepté/refusé, prix snapshots et rollback si le décrément conditionnel du stock échoue.
- `e2e/test_nominal_booking_flow.py` : scénario Playwright nominal avec `live_server`, connexion, ajout de 2 billets, panier, checkout, paiement accepté, confirmation, historique et assertions ORM dans la base de test.
- `e2e/test_page_performance.py` : mesure Playwright Chromium de `ENF2` sur l'accueil, le catalogue, une fiche concert et l'historique authentifié, avec LCP `<= 2 000 ms` et durée de chargement en diagnostic.

Couverture officielle revendiquée dans cette étape :

- `EF3` : création de compte avec e-mail unique et mot de passe.
- `EF4` : connexion, déconnexion et accès à un espace personnel protégé.
- `EF1` : catalogue limité aux concerts ouverts, futurs et avec stock.
- `EF2` : fiche avec titre, artiste, date, lieu, catégories, prix et stock restant.
- `EM8` : e-mail utilisateur unique, y compris rejet formulaire.
- `ENF3` : mot de passe géré par le hachage Django.
- `ENF4` : rejet propre d'un e-mail déjà utilisé pendant l'inscription.
- `EM1` à `EM7`, `EM10`, `RG1` à `RG5` et `RG7` : couverture domaine/service, complétée par les vues pour les états de concert, le parcours panier/paiement, l'administration et l'affichage des commandes.
- `EF5`, `EF6`, `EF7`, `EF8`, `EF9` : couverture par services et vues Django.
- `EF12` : décrément de stock après paiement accepté au niveau service.
- `EF12`, `EM1`, `EM6`, `ENF4`, `RG2`, `RG5` : rollback complet si le décrément conditionnel du stock ne peut pas être appliqué.
- `RG6` : checkout et paiement protégés par authentification.
- `EF10` et `RG8` : couverture par l'historique des commandes payées et le détail de commande filtrés par utilisateur.
- `EF11` et `EM9` : couverture par les vues admin protégées par permissions et l'admin Django.
- `ENF6` : tests automatisés executables sur la fondation technique et domaine.
- `EF1`, `EF2`, `EF4`, `EF5`, `EF6`, `EF7`, `EF8`, `EF10`, `EF12`, `EM1`, `EM2`, `EM3`, `EM6`, `EM7`, `EM10`, `RG1`, `RG2`, `RG3`, `RG5`, `ENF1`, `ENF6` et `ENF7` : preuve Playwright de bout en bout pour le parcours nominal.
- `ENF2` : preuve Playwright Chromium reproductible sur quatre pages standards sous conditions contrôlées.

Le suivi admin des ventes ne relève pas de `RG8`; `RG8` reste limité à l'accès des utilisateurs standards à leurs propres commandes.
`ENF1` est couvert pour le parcours nominal fiche -> panier -> paiement -> commandes par le scénario Playwright.

## Couches prévues

| Couche | Objectif | Exemples cibles |
| --- | --- | --- |
| Tests unitaires | Valider les règles métier isolées. | quantité 1 à 6, stock disponible, prix fige à la validation |
| Tests d'intégration Django | Valider modèles, vues, formulaires, ORM et permissions. | création de compte unique, ajout panier, paiement accepté/refusé, pages résultat, historique filtré et administration concerts/ventes |
| Tests fonctionnels Playwright | Valider un parcours utilisateur complet. | consultation, connexion, ajout panier, paiement accepté, historique |
| Performance Playwright | Mesurer le rendu navigateur de pages standards sous conditions contrôlées. | LCP accueil, catalogue, fiche concert, historique authentifié |
| Couverture | Mesurer les packages applicatifs et bloquer une regression importante. | rapport terminal, XML et seuil global de 90 % |
| Analyse statique | Détecter les erreurs et problèmes de style. | `ruff check .` |

## Commandes cibles

```bash
ruff check .
pytest
pytest --cov --cov-report=term-missing --cov-report=xml
pytest e2e --browser chromium --tracing=retain-on-failure --output=test-results/playwright -rP
```

La commande e2e utilise `pytest-django` et `live_server`. Les fixtures créent leurs données dans la base de test transactionnelle ; elles ne ne dépendent pas de `db.sqlite3`.
Le test `ENF2` utilise un contexte Chromium froid par page, un viewport desktop
1366x768, aucune limitation CPU/réseau et des ressources Bootstrap rejouées
depuis des fixtures locales correspondant aux empreintes SRI du template. Cette
mesure attend l'entrée LCP après la visibilité du contenu principal, dans la
limite du seuil officiel de 2 000 ms. Elle valide le rendu navigateur sous
conditions CI contrôlées, pas la performance de production sur tous les
appareils, états CDN ou réseaux.

## Commandes vérifiées localement

```bash
pytest e2e --browser chromium --tracing=retain-on-failure --output=test-results/playwright -rP
python manage.py check
python manage.py makemigrations --check --dry-run
ruff check .
pytest
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
coverage report
test -s coverage.xml
```

Résultat final observé : 108 tests Django passent, `coverage.xml` est généré,
non vide (37 553 octets), et la couverture applicative avec branches atteint
99,6 % (813 instructions, 2 non couvertes, 102 branches), au-dessus du seuil
obligatoire de 90 %. Les 35 chemins mesurés sont relatifs et résolvables. Les
tests ne sont pas inclus dans le dénominateur. Le scénario Playwright nominal
et les mesures `ENF2` passent également.

Le rapport XML conserve les chemins complets relatifs aux packages
(`accounts/admin.py`, `cart/admin.py`, etc.). Le validateur CI refuse les
chemins absolus ou non résolvables afin d'éviter que SonarCloud ignore des
mesures de couverture à cause de noms ambigus.

## Exclusions de couverture

Les fichiers `config/asgi.py` et `config/wsgi.py` sont exclus de la couverture coverage.py et SonarCloud. Ce sont des entrypoints Django générés par `startproject`, sans logique applicative propre.

Les migrations restent exclues comme artefacts générés. Les fichiers applicatifs réels (`accounts`, `concerts`, `cart`, `orders`, `payments`, `config/settings.py`, `config/urls.py`) restent mesurés.

Le seuil de 90 % constitue une alerte de régression. Il ne justifie ni tests
artificiels ni nouvelles exclusions. Les deux lignes défensives restantes dans
`payments/services.py` concernent des incohérences entre les données validées et
les catégories verrouillées ; elles ne sont pas forcées par des fixtures
incohérentes uniquement pour atteindre 100 %.

## Règles de priorisation

Les premiers tests devront couvrir les exigences qui portent le plus de risque métier :

- EM1 / RG2 : ne jamais vendre plus que le stock.
- EF12 / EM1 / EM6 / RG5 : annuler toute la transaction si le décrément atomique échoue.
- EM2 / EM3 / RG3 : quantité entre 1 et 6.
- EM6 / RG4 / RG5 : commande définitive seulement après paiement accepté.
- RG8 : un utilisateur ne consulte que ses propres commandes ou pages de résultat.
- EF11 / EM9 / RG7 : seules les permissions admin adaptées permettent de gérer ou annuler un concert.
- ENF3 : mots de passe jamais stockés en clair.
- EF3 / EF4 : parcours inscription, connexion, déconnexion et accès protégé.
- EF1 / EF2 / EF5 / EF7 / EF8 / EF10 / ENF1 : parcours fonctionnel Playwright nominal.
- ENF2 : affichage de pages standards en moins de deux secondes sous conditions normales documentees.

## Documentation des tests

Chaque test automatisé devra être relié à un ou plusieurs IDs officiels dans `docs/validation/matrice_tracabilite.md`.

Pour l'historique, `EF10` et `RG8` sont couverts par les pages de commandes payées et détail filtrées par propriétaire. Pour l'administration, `EF11`, `EM9` et `RG7` sont couverts par `tests/test_admin_concert_management.py`. `EF8`, `EF9`, `EM6`, `EM7`, `EM10`, `RG4` et `RG5` sont maintenus ou étendus par les tests de navigation et d'affichage, mais leur comportement cœur reste porté par le parcours checkout/paiement. Le scénario Playwright nominal est tracé dans `docs/validation/matrice_tracabilite.md` et documenté dans `docs/validation/scenario_fonctionnel.md`. La mesure `ENF2` est tracée dans `docs/validation/matrice_tracabilite.md` avec ses pages, son seuil, son navigateur et ses limites.
