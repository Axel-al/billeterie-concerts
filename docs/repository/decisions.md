# Decisions

Ce journal consigne les decisions structurantes deja prises. Les nouvelles decisions devront etre ajoutees en tete de liste.

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
