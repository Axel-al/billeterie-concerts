# Decisions

Ce journal consigne les decisions structurantes deja prises. Les nouvelles decisions devront etre ajoutees en tete de liste.

## 2026-06-15 - Seuil de couverture local et gates SonarCloud externes

Decision : mesurer uniquement les packages applicatifs declares dans
`pyproject.toml`, avec couverture de branches, precision a une decimale et seuil
global bloquant de 90 %. Le Quality Gate SonarCloud conserve son seuil de
couverture du nouveau code a 80 %.

Motif : un seuil local rend la verification reproductible meme lorsque
SonarCloud n'est pas disponible. La marge entre les 90 % locaux et la couverture
actuelle evite qu'une petite evolution non critique bloque artificiellement le
projet. Ce seuil reste un garde-fou : il ne justifie ni tests artificiels ni
exclusion de code applicatif reel, et les regles metier critiques restent
prioritaires.

Impact : la commande de reference devient
`pytest --cov --cov-report=term-missing --cov-report=xml`. Le workflow conserve
le nom requis `Django checks`, verifie aussi l'absence de migration manquante et
affiche les lignes non couvertes. SonarCloud analyse egalement les templates
Django et les workflows GitHub Actions.

`sonar.qualitygate.wait` n'est pas active : les regles du depot exigent deja les
checks distincts `Django checks` et `SonarCloud Code Analysis`. Attendre le
Quality Gate dans le job Django dupliquerait ce mecanisme et allongerait la CI.
L'analyse reste conditionnelle a `SONAR_TOKEN`; une pull request issue d'un fork
peut donc ne pas lancer le scanner et rester bloquee par le check Sonar requis
jusqu'a une execution dans un contexte de confiance.

## 2026-06-15 - Administration concerts et ventes par permissions Django

Decision : ajouter une synthese admin des ventes et des actions d'annulation/cloture avec des vues Django protegees par permissions, tout en enrichissant l'admin Django existant.

Motif : `EF11`, `EM9` et `RG7` demandent une preuve testable de gestion administrateur. Une page Django template reste coherente avec la stack du projet et plus facile a demontrer/tester que l'admin Django seul. Les permissions explicites `concerts.view_concert`, `orders.view_order` et `concerts.change_concert` permettent de distinguer visiteur anonyme, utilisateur standard et gestionnaire autorise.

Impact : le statut `closed` represente une vente cloturee sans assimiler ce cas a un concert complet. Les concerts annules ou clotures ne sont plus reservables, mais les commandes payees existantes restent visibles a leur proprietaire. Le suivi admin des ventes compte seulement les commandes payees et ne modifie pas la portee de `RG8`, qui reste l'isolation des commandes des utilisateurs standards.

## 2026-06-14 - Parcours panier et paiement simule Django

Decision : exposer le parcours panier, checkout, paiement simule, confirmation et refus avec des vues/templates Django, en reutilisant les services domaine existants.

Motif : les exigences `EF5` a `EF9`, `EF12`, `RG6` et les regles critiques de stock/quantite/paiement doivent etre couvertes sans introduire de frontend separe. La carte `4242424242424242` est acceptee ; toute autre valeur est refusee.

Impact : les URLs `/panier/`, `/panier/validation/` et `/paiement/` sont disponibles. Les commandes payees decrementent le stock et figent les prix. Les commandes refusees restent non finales et ne modifient pas le stock. L'historique complet de commandes (`EF10`) reste hors scope.

## 2026-05-18 - Authentification utilisateur par Django

Decision : implementer l'inscription, la connexion, la deconnexion POST et `Mon espace` avec les mecanismes Django auth et des templates Django en francais.

Motif : les exigences `EF3`, `EF4`, `EM8`, `ENF3` et `ENF4` doivent etre couvertes sans introduire de framework frontend separe ni contourner le hachage et la gestion de session de Django.

Impact : les URLs `/inscription/`, `/connexion/`, `/deconnexion/` et `/mon-espace/` sont disponibles. L'inscription connecte automatiquement l'utilisateur et le redirige vers `Mon espace`. La deconnexion passe par un formulaire POST dans la navigation. `EM9` reste une fondation de role seulement, car les permissions d'administration des concerts sont hors de cette etape.

## 2026-05-06 - Domaine billetterie isole en services testables

Decision : implementer les modeles `Concert`, `SeatCategory`, `Cart`, `CartLine`, `Order`, `OrderLine` et `Payment`, avec des services pour l'ajout panier et le paiement simule.

Motif : les regles de quantite, stock, date, statut de concert, paiement accepte/refuse et prix snapshots doivent etre testables sans attendre les vues.

Impact : `EF5`, `EF7`, `EF8` et `EF9` sont documentees comme couvertures partielles domaine/service. Les confirmations, messages d'erreur visibles et parcours utilisateur restent a implementer plus tard.

## 2026-05-06 - Applications `cart` et `payments` separees

Decision : creer des applications Django dediees `cart` et `payments` plutot que de placer tout le domaine dans `orders`.

Motif : ce decoupage correspond a l'architecture cible deja documentee et garde les responsabilites lisibles.

Impact : `config.settings.INSTALLED_APPS` inclut maintenant `cart` et `payments` ; la couverture inclut aussi ces packages.

## 2026-05-06 - Panier et commande limites a un concert

Decision : un panier actif et une commande ne peuvent contenir qu'un seul concert.

Motif : la regle `EM3` limite a 6 billets pour un meme concert et une meme commande. Cette limite rend la premiere implementation plus simple et explicite.

Impact : les services refusent les paniers multi-concerts et appliquent le plafond de 6 billets sur la quantite agregee de toutes les categories du concert.

## 2026-04-25 - Fondation Django technique

Decision : initialiser Django avec le module `config`, les apps `accounts`, `concerts` et `orders`, une page d'accueil minimale, pytest, coverage, Ruff, GitHub Actions et SonarCloud.

Motif : la demande courante porte sur une fondation technique executable et testable, pas sur les parcours metier complets.

Impact : les exigences couvertes restent limitees a la fondation utilisateur et qualite (`EF3` partiel, `EM8`, `ENF3`, `ENF5`, `ENF6`, `ENF7`). Les exigences de concerts, panier, paiement, stock et commandes restent non couvertes.

## 2026-04-25 - CustomUser email des le depart

Decision : creer `accounts.User` comme modele utilisateur personnalise avec email unique comme identifiant.

Motif : le cahier des charges impose l'unicite email (`EM8`) et l'utilisateur principal est defini autour de l'email. Le faire avant les premieres migrations evite une migration tardive complexe.

Impact : `AUTH_USER_MODEL = "accounts.User"` est configure. Les mots de passe restent geres par le hachage Django (`ENF3`). Les roles specifiques ne sont pas ajoutes ; les premiers droits administrateur utilisent `is_staff` et `is_superuser`.

## 2026-04-25 - SonarCloud conditionnel

Decision : enrichir `sonar-project.properties` avec les chemins existants et declencher l'analyse CI seulement si `SONAR_TOKEN` est disponible.

Motif : la configuration SonarCloud doit etre versionnee sans exposer de secret et ne doit pas referencer de chemins absents comme `e2e/`.

Impact : la CI ne doit pas echouer uniquement parce que le secret SonarCloud est absent.

## 2026-04-25 - Baseline documentaire avant initialisation Django

Decision : creer la documentation de depot et de validation avant d'initialiser le projet Django.

Motif : le prompt demande explicitement de completer la structure documentaire sans initialiser Django sauf s'il est deja present. Le depot ne contient actuellement aucun projet Django.

Impact : les documents de validation indiquent les exigences officielles et les tests prevus, mais ne revendiquent aucune couverture fonctionnelle deja implementee.

## 2026-04-25 - Stack principale Django

Decision : utiliser Python, Django, SQLite en developpement, templates Django et Bootstrap via CDN.

Motif : ce choix est coherent avec le besoin, limite la complexite frontend et permet de concentrer l'effort sur les exigences, les tests et la qualite.

Impact : React, Vite, TypeScript, Node.js et une application frontend separee ne sont pas prevus.

## 2026-04-25 - Strategie de validation

Decision : preparer une validation multi-couches avec tests unitaires, tests d'integration, couverture, Ruff et scenarios fonctionnels Playwright.

Motif : le cahier des charges demande des preuves de qualite, une tracabilite exigences-tests, de l'analyse statique et de l'integration continue.

Impact : les dependances de developpement incluent deja `pytest`, `pytest-django`, `pytest-cov`, `coverage`, `ruff`, `freezegun`, `factory-boy` et `pytest-playwright`.

## 2026-04-25 - CI et SonarQube planifies

Decision : documenter CI et SonarQube comme objectifs planifies, pas comme fonctionnalites deja livrees.

Motif : aucun workflow GitHub Actions ni fichier SonarQube n'est versionne pour l'instant.

Impact : `quality-ci.md` decrit les commandes et seuils cibles sans pretendre qu'ils sont actifs.
