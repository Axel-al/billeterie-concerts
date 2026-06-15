# État courant du dépôt

Dernière mise à jour : 2026-06-15

## Synthèse

Le dépôt contient une application Django exécutable avec :

- un modèle utilisateur personnalisé basé sur l'e-mail ;
- des pages françaises d'inscription, connexion, déconnexion et espace personnel ;
- un catalogue public de concerts et des fiches détaillées ;
- un parcours panier, checkout, paiement simulé, confirmation et refus ;
- un historique des commandes payées et un détail de commande filtrés par utilisateur ;
- des vues d'administration protégées par permissions pour le suivi des ventes, l'annulation et la clôture des ventes ;
- un noyau domaine testé pour la billetterie de concerts ;
- une documentation de validation et de traçabilité mise à jour.

Éléments livrés dans cette étape :

- routes `/concerts/` et `/concerts/<id>/` ;
- catalogue limité aux concerts ouverts, futurs et possédant du stock ;
- fiches avec titre, artiste, date, lieu, description, catégories, prix et stock restant ;
- explications françaises pour les concerts annulés, passés, complets ou fermés à la vente ;
- lien de connexion avec retour vers la fiche pour les visiteurs d'un concert réservable ;
- formulaire catégorie/quantité sur les fiches réservables pour les utilisateurs connectés ;
- route `/panier/` avec lignes, sous-totaux et total ;
- route `/panier/validation/` protégée par authentification et limitée au panier actif de l'utilisateur ;
- route `/paiement/` avec paiement simulé ;
- carte `4242424242424242` acceptée et toute autre carte refusée, sans stockage du numéro ;
- création d'une commande `paid`, prix snapshots et décrément du stock après paiement accepté ;
- création d'une commande `refused` non finale et stock inchangé après paiement refusé ;
- pages de confirmation et refus filtrées par utilisateur connecté ;
- routes `/commandes/` et `/commandes/<id>/` protégées par authentification ;
- historique `Mes commandes` limité aux commandes payées du client connecté ;
- détail de commande affichant date, statut, total, concert, catégorie, quantité et prix payé ;
- commandes refusées exclues de l'historique des achats payés ;
- navigation post-paiement vers le détail de commande et l'historique ;
- statut de concert `closed` pour les ventes clôturées ;
- route `/concerts/administration/ventes/` protégée par `concerts.view_concert` et `orders.view_order` ;
- actions POST d'administration pour annuler un concert ou clôturer ses ventes, protégées par `concerts.change_concert` ;
- synthèse des ventes par concert limitée aux commandes payées : commandes, billets vendus, chiffre d'affaires, stock initial et stock restant ;
- lien de navigation `Administration ventes` visible seulement pour les utilisateurs ayant les permissions de consultation requises ;
- admin Django enrichi pour les concerts et catégories, avec indicateurs de stock/ventes et actions d'annulation/clôture ;
- commandes et paiements consultables en admin comme surfaces de lecture plutôt que de modification métier ;
- navigation et accueil orientés vers la consultation des concerts ;
- tests d'intégration Django pour le filtrage, les affichages, les CTA, les motifs d'indisponibilité, les réponses HTTP, le parcours panier/paiement et l'historique de commandes ;
- tests d'intégration Django pour les permissions d'administration, l'annulation, la clôture, le suivi des ventes et la création/modification admin de concerts avec catégories ;
- scénario Playwright `e2e/test_nominal_booking_flow.py` pour le parcours nominal catalogue -> fiche -> connexion -> panier -> checkout -> paiement accepté -> confirmation -> historique ;
- test Playwright Chromium `e2e/test_page_performance.py` pour `ENF2` sur accueil, catalogue, fiche concert et historique authentifié ;
- mesure ENF2 par Largest Contentful Paint avec seuil `<= 2 000 ms` et durée `PerformanceNavigationTiming` en diagnostic ;
- fixtures e2e basées sur `pytest-django`, `transactional_db` et `live_server`, sans dépendance à `db.sqlite3` ni aux données démo locales ;
- fixtures locales Bootstrap 5.3.3 conformes aux empreintes SRI du template pour rejouer les ressources jsDelivr sans latence CDN pendant la mesure ;
- sélecteurs stables `data-testid` sur les contrôles et liens du parcours nominal ;
- routes `/inscription/`, `/connexion/`, `/deconnexion/` et `/mon-espace/` ;
- formulaire d'inscription avec e-mail unique, mot de passe Django et rejet explicite des doublons ;
- formulaire de connexion en français et déconnexion par requête POST ;
- navigation différenciée entre visiteurs et utilisateurs connectés ;
- page protégée `Mon espace` ;
- tests d'intégration Django pour labels français, inscription, connexion, échec de connexion, déconnexion POST, protection d'accès et rôle utilisateur standard ;
- test de rollback transactionnel si le décrément conditionnel du stock échoue ;
- couverture applicative de branches avec seuil global de 90 % et rapport XML ;
- CI avec Ruff, checks Django, contrôle de migrations, tests, Playwright et SonarCloud ;
- CI Playwright cible explicitement Chromium et affiche les diagnostics des tests passés avec `-rP` ;
- analyse SonarCloud étendue aux templates Django et workflows GitHub Actions ;
- actions GitHub épinglées par SHA et dépendances CI verrouillées dans `requirements-ci.txt` ;
- mise à jour des documents `docs/repository/` et `docs/validation/`.

Le cahier des charges officiel reste conservé dans `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Exigences couvertes dans cette étape

Couverture revendiquée pour le périmètre comptes :

- `EF3` : création de compte avec e-mail unique et mot de passe ;
- `EF4` : connexion, déconnexion et accès à un espace personnel protégé ;
- `EM8` : deux comptes ne peuvent pas partager le même e-mail ;
- `ENF3` : mots de passe gérés par le hachage Django ;
- `ENF4` : rejet propre des e-mails déjà utilisés et des identifiants invalides.

Couverture revendiquée pour le catalogue :

- `EF1` : liste des concerts ouverts, futurs et avec stock ;
- `EF2` : fiche détaillée avec informations, catégories, prix et stock restant ;
- `EM4`, `EM5` et `RG1` : états non réservables appliqués dans les vues ;
- `RG7` : annulation visible sans nouvelle action de réservation, hors action admin ;
- `ENF1` : couverture partielle par la navigation accueil, catalogue et fiche.

Couverture revendiquée pour l'administration :

- `EF11` : création, modification, annulation et clôture de concerts via administration ;
- `EM9` : les vues d'administration exigent les permissions Django adaptées ;
- `RG7` : l'annulation admin rend le concert non réservable.

Couverture existante conservée :

- `EF5` : ajout de billets au panier depuis une fiche concert réservable pour un utilisateur connecté ;
- `EF6` : total du panier affiche et calculé à partir des lignes ;
- `EF7` : validation du panier par paiement simulé ;
- `EF8` : paiement accepté, commande payée et confirmation affichée ;
- `EF9` : paiement refusé, aucune commande validée et message explicite ;
- `EF12` : stock décrémenté après paiement accepté ;
- `EM1` à `EM7` et `EM10` : règles couvertes au niveau domaine/service et parcours UI ;
- `RG1` à `RG6` : règles couvertes au niveau domaine/service et parcours UI ;
- `EF10` et `RG8` : historique des commandes payées et détail de commande filtrés par propriétaire ;
- `EF12`, `EM1`, `EM6`, `ENF4`, `RG2` et `RG5` : rollback complet si le décrément conditionnel du stock échoue ;
- `ENF5`, `ENF6` et `ENF7` : Ruff, tests automatisés, couverture avec seuil, GitHub Actions et Quality Gate SonarCloud.

Couverture e2e ajoutée :

- `EF1`, `EF2`, `EF4`, `EF5`, `EF6`, `EF7`, `EF8`, `EF10` et `EF12` sont couverts de bout en bout par le scénario Playwright nominal.
- `EM1`, `EM2`, `EM3`, `EM6`, `EM7`, `EM10`, `RG1`, `RG2`, `RG3` et `RG5` sont vérifiés dans ce scénario par le choix d'un concert réservable, une quantité valide, le paiement accepté, les snapshots de prix et le décrément du stock.
- `ENF1`, `ENF6` et `ENF7` sont renforcés par un parcours fonctionnel automatisé et exécuté en CI.
- `ENF2` est couvert par une mesure Playwright Chromium reproductible sur des pages standards avec LCP `<= 2 000 ms` sous conditions contrôlées.

Traçabilité de cette étape :

- `ENF2` est tracée dans `docs/validation/matrice_tracabilite.md` avec le test, les pages mesurées, le seuil, le navigateur, les résultats et les limites.
- `EF10` et `RG8` sont couverts par le nouvel historique payé et les pages détail filtrées par propriétaire.
- `EF11`, `EM9` et `RG7` sont couverts par les vues d'administration, les actions de statut et les tests de permissions.
- `EF8`, `EF9`, `EM6`, `EM7`, `EM10`, `RG4` et `RG5` sont maintenus ou étendus par les tests de navigation et d'affichage, mais leur comportement cœur était déjà implémenté par le parcours checkout/paiement.
- Le scénario Playwright nominal ajoute une preuve fonctionnelle de bout en bout pour le parcours attendu du cahier des charges, sans couvrir les parcours d'erreur optionnels.

Non couvert volontairement dans ce lot :

- `RG8` ne couvre pas le suivi de ventes administrateur : il reste limité au cloisonnement des commandes des utilisateurs standards.

## Structure applicative

- `config/` : settings, URLs racines, redirections d'authentification, ASGI et WSGI.
- `accounts/` : modèle utilisateur personnalisé, manager, admin Django, formulaires, vues et URLs d'authentification.
- `concerts/` : concerts, catégories de places, statuts, stock, vues publiques, vues d'administration, services de gestion, admin Django et commande `seed_demo_data`.
- `cart/` : panier actif mono-concert, lignes de panier, services de validation/ajout, vues panier et checkout.
- `orders/` : commandes, lignes de commandes et prix snapshots.
- `payments/` : paiement simulé, règle de carte, service transactionnel et vues paiement/résultat.
- `templates/` : layout, accueil, catalogue, fiches concerts, comptes, panier, paiement, commandes et synthèse admin des ventes.
- `tests/` : tests de smoke homepage, settings, utilisateur, authentification, vues concerts, domaine billetterie, parcours panier/paiement, historique de commandes et administration concerts/ventes.
- `e2e/` : scénario Playwright nominal et mesure ENF2 avec fixtures `pytest-django`, `live_server` et Bootstrap local rejoué pour la mesure.

## Comportement catalogue

- Le catalogue public n'affiche que les concerts strictement futurs, `open` et avec au moins une catégorie en stock.
- Les fiches annulées, clôturées, passées, terminées ou complètes restent consultables avec un motif explicite et sans CTA de réservation.
- Les fiches brouillon et les identifiants inconnus renvoient `404`.
- Toutes les catégories sont affichées sur la fiche, y compris les catégories épuisées.
- Un visiteur voit `Se connecter pour réserver` seulement pour un concert réservable ; le paramètre `next` conserve l'URL de la fiche.
- Un utilisateur connecté voit un formulaire d'ajout au panier sur les fiches réservables.

## Comportement panier et paiement

- Un utilisateur connecté peut ajouter une catégorie et une quantité de billets depuis la fiche d'un concert réservable.
- La quantité est rejetée si elle n'est pas comprise entre 1 et 6.
- Les concerts passés, annulés, fermés à la vente ou sans stock ne peuvent pas être ajoutés au panier.
- Le panier actif affiche les lignes, les sous-totaux et le total.
- Le checkout et le paiement exigent une session authentifiée et utilisent uniquement le panier actif de l'utilisateur courant.
- Le paiement simulé accepte la carte `4242424242424242` et refuse toute autre valeur.
- En cas de paiement accepté, une commande `paid` est créée, les prix de lignes sont figés, le stock est décrémenté et le panier passe à `checked_out`.
- En cas de paiement refusé, une commande `refused` non finale est créée, le stock ne change pas et le panier reste actif.
- Les pages de confirmation et de refus ne sont accessibles qu'au propriétaire de la commande.
- La confirmation de paiement propose un accès au détail de commande et à `Mes commandes`.

## Comportement commandes

- `Mes commandes` exige une session authentifiée et redirige les visiteurs vers `/connexion/?next=/commandes/`.
- L'historique affiche uniquement les commandes `paid` du client connecté.
- Le détail `/commandes/<id>/` exige une session authentifiée, filtre par propriétaire et par statut `paid`, et renvoie `404` pour la commande payée d'un autre utilisateur ou une commande refusée.
- Le détail affiche la date, le statut, le montant total, le concert, la catégorie achetée, la quantité, le prix payé et le total de ligne.
- Les commandes refusées restent tracées comme non finales, ne décrémentent pas le stock et sont exclues de l'historique des achats payés.

## Comportement administration

- Le statut `closed` représente une vente clôturée manuellement par l'administration.
- La synthèse `/concerts/administration/ventes/` exige `concerts.view_concert` et `orders.view_order`.
- Les actions POST d'annulation et de clôture exigent `concerts.change_concert`.
- Un visiteur anonyme est redirigé vers `/connexion/` avec le paramètre `next`.
- Un utilisateur authentifié sans permission reçoit une réponse `403`.
- Un utilisateur ayant les permissions requises peut consulter les ventes et changer le statut d'un concert.
- L'annulation admin met le concert en `cancelled` et bloque toute nouvelle réservation.
- La clôture admin met le concert en `closed` et bloque toute nouvelle réservation.
- L'annulation ou la clôture ne modifie pas le stock restant et ne supprime pas les commandes payées existantes.
- La synthèse des ventes compte uniquement les commandes `paid`; les commandes `refused` restent hors chiffre d'affaires et hors billets vendus.

## Comportement authentification

- Un visiteur peut créer un compte avec e-mail, nom, prénom et mot de passe.
- Une inscription réussie connecte automatiquement l'utilisateur et redirige vers `Mon espace`.
- Un e-mail déjà utilisé est refusé avec le message `Un compte existe déjà avec cette adresse e-mail.`
- Un utilisateur peut se connecter avec son e-mail et son mot de passe.
- Une erreur de connexion affiche un message français explicite.
- La déconnexion utilise un formulaire POST dans la navigation.
- `Mon espace` exige une session authentifiée et redirige les visiteurs vers `/connexion/?next=/mon-espace/`.
- `Mon espace` et la navigation authentifiée donnent accès à `Mes commandes`.
- Un utilisateur standard créé par le parcours public n'a pas les droits `is_staff` ni `is_superuser`.

## Règles domaine implémentées

- Un concert est réservable seulement s'il est strictement futur, `open` et avec au moins une catégorie en stock.
- Les concerts passés, annulés ou clôturés ne sont pas réservables.
- Une quantité doit être un entier entre 1 et 6.
- Le plafond de 6 billets est appliqué au total du panier/commande pour un seul concert, pas seulement par ligne.
- Un panier actif et une commande sont limités à un seul concert.
- Le stock restant ne peut pas devenir négatif.
- Un paiement accepté crée une commande `paid`, crée un paiement `accepted`, fige les prix et décrémente le stock.
- Un paiement refusé crée une commande `refused`, crée un paiement `refused`, ne décrémente pas le stock et laisse le panier actif.
- Un utilisateur ne peut consulter que ses propres commandes payées dans l'historique et le détail de commande.

## Données démo

La commande `python manage.py seed_demo_data` crée ou met à jour :

- un concert futur ouvert ;
- un concert futur annulé ;
- un concert passé/terminé ;
- plusieurs catégories de places avec prix et stocks différents.

## Qualité et CI

Le workflow conserve le job requis `Django checks` et exécute Ruff, les checks
Django, le contrôle des migrations, pytest avec couverture, puis Playwright
Chromium pour le scénario nominal et la mesure `ENF2`. Les traces Playwright
sont publiées en cas d'échec.

Coverage mesure uniquement les packages applicatifs déclarés avec
`source_pkgs` dans `pyproject.toml`, avec branches, chemins relatifs non ambigus,
précision à une décimale, rapport terminal, `coverage.xml` et seuil global
bloquant de 90 %. Le workflow valide chaque chemin du XML avant SonarCloud. Le
seuil reste un garde-fou et ne justifie ni tests artificiels ni exclusion de
code applicatif.

SonarCloud analyse les packages Python, les templates Django et les workflows
GitHub Actions. Les tests `tests/` et `e2e/` sont déclarés comme sources de test.
Les ressources Bootstrap distantes portent leurs empreintes SRI et les messages
statiques n'utilisent pas de rôle ARIA live inutile. Ces règles sont vérifiées
dans `tests/test_template_quality.py`.
Les actions GitHub sont épinglées par SHA immuable, dont
`SonarSource/sonarqube-scan-action` v8.2.0. `requirements-ci.txt` verrouille les
versions directes et transitives ainsi que les empreintes SHA-256. La CI impose
`--require-hashes` et installe uniquement des distributions binaires.

`sonar.qualitygate.wait` n'est pas activé : les règles du dépôt exigent déjà les
checks distincts `Django checks` et `SonarCloud Code Analysis`. L'analyse reste
conditionnelle à `SONAR_TOKEN`; les pull requests de forks peuvent donc ne pas
exécuter le scanner et rester bloquées par le check Sonar requis.

Le détail de la stratégie et des limites est maintenu dans
`docs/repository/quality-ci.md`, `docs/repository/testing.md` et
`docs/validation/rapport_qualite.md`.

## Correction rédactionnelle française

Branche de travail : `docs/french-text-consistency`.

Cette étape corrige les accents, apostrophes et formulations françaises dans
les textes visibles de l'interface, les libellés Django/admin et la
documentation maintenue du projet. Les migrations ajoutées sont uniquement
typographiques : elles mettent à jour des `verbose_name` et des labels
d'affichage de `TextChoices`. Elles ne changent ni les valeurs stockées, ni les
clés d'énumération, ni les règles métier.

## Vérification locale

Contrôles exécutés pour cette étape :

```bash
python manage.py makemigrations --check --dry-run
python manage.py migrate --plan
python manage.py check
ruff check .
pytest
pytest e2e --browser chromium --tracing=retain-on-failure --output=test-results/playwright
git diff --check
```

- `python manage.py makemigrations --check --dry-run` : OK, aucune migration manquante.
- `python manage.py migrate --plan` : OK, plan limité à des `AlterField` de libellés d'affichage.
- `python manage.py check` : OK.
- `ruff check .` : OK.
- `pytest` : OK, 108 tests passent.
- Playwright Chromium : OK, 5 tests passent.
- `git diff --check` : OK.

## Vérification navigateur

Aucun contrôle manuel navigateur supplémentaire n'a été réalisé. Les textes du
parcours nominal ayant changé, le scénario Playwright Chromium complet a été
relancé.

Le Quality Gate SonarCloud a initialement signalé une duplication entre le
détail de commande et la confirmation de paiement. Le tableau commun des lignes
de commande est maintenant rendu par le partial
`templates/orders/_order_lines_table.html`, sans modifier les titres, actions
ou attributs `data-testid` propres à chaque page.
