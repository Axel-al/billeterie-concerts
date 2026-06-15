# Décisions

Ce journal consigne les décisions structurantes déjà prises. Les nouvelles décisions devront être ajoutées en tête de liste.

## 2026-06-15 - Validation française côté serveur

Décision : utiliser `novalidate` sur les formulaires de réservation et de
paiement afin que Django produise les messages d'erreur de référence en
français. Conserver les attributs HTML utiles, notamment `required`, `min`,
`max`, les types de champs, `maxlength` et `inputmode`.

Motif : les messages de validation natifs varient selon la langue du
navigateur et peuvent apparaître en anglais pendant la soutenance. Les
attributs HTML restent néanmoins utiles à la sémantique, à l'accessibilité et
aux claviers adaptés.

Impact : les mêmes contraintes sont vérifiées dans les formulaires Django, les
validateurs de modèles et les services métier. Des tests Django contrôlent le
HTML et les erreurs, et un test Playwright vérifie la borne supérieure avec un
message français.

## 2026-06-15 - Mesure ENF2 en navigateur contrôlé

Décision : valider `ENF2` avec un test Playwright Chromium dédié qui mesure le
Largest Contentful Paint sur des pages standards représentatives, avec un seuil
strict de 2 000 ms.

Motif : l'exigence demande un affichage en moins de deux secondes dans des
conditions normales. Le test doit mesurer un vrai rendu navigateur, mais rester
reproductible en local et en CI. Les ressources Bootstrap restent chargées par
le template depuis jsDelivr en production ; pendant la mesure, Playwright
intercepte ces URLs et renvoie des fixtures locales contenant les vrais fichiers
Bootstrap 5.3.3 dont les empreintes SHA-384 correspondent aux attributs SRI du
template.

Impact : la mesure utilise `live_server`, une base de test créée par
`pytest-django`, une navigation locale loopback, un viewport desktop 1366x768,
Chromium sans throttling CPU ou réseau et un contexte navigateur froid par page.
Elle valide le rendu sous conditions CI contrôlées, pas la performance de
production sur tous les appareils, états CDN ou réseaux.

## 2026-06-15 - Intégrité CDN et messages HTML statiques

Décision : conserver Bootstrap 5.3.3 via jsDelivr avec les empreintes SRI
officielles et `crossorigin="anonymous"`. Retirer `rôle="status"` des messages
statiques rendus par Django.

Motif : SonarCloud signale les ressources distantes sans contrôle d'intégrité.
Les quatre messages concernés ne sont pas injectés dynamiquement et n'ont donc
pas besoin d'une zone live ARIA ; leur texte et leur présentation Bootstrap
restent inchangés.

Impact : un test statique parse les templates pour vérifier les métadonnées des
deux ressources Bootstrap et l'absence de nouveau `rôle="status"`. Toute mise à
jour de Bootstrap devra mettre à jour simultanément les URL et empreintes.

## 2026-06-15 - Chemins de couverture relatifs et non ambigus

Décision : déclarer les applications Django avec `coverage.py source_pkgs`,
activer `relative_files` et valider le rapport XML avant l'analyse SonarCloud.

Motif : une liste de répertoires dans `source` produisait des noms raccourcis
comme `admin.py`, présents dans plusieurs applications. SonarCloud ne pouvait
pas choisir le fichier correspondant et ignorait les mesures de sept familles
de chemins, puis attribuait 0 % de couverture aux fichiers concernés.

Impact : `coverage.xml` utilise des chemins tels que `accounts/admin.py` sans
inclure les tests dans le dénominateur. La CI exécute
`.github/scripts/validate_coverage_xml.py` après pytest. La définition SonarCloud
du nouveau code reste inchangée.

## 2026-06-15 - Seuil de couverture local et gates SonarCloud externes

Décision : mesurer uniquement les packages applicatifs déclarés dans
`pyproject.toml`, avec couverture de branches, précision à une décimale et seuil
global bloquant de 90 %. Le Quality Gate SonarCloud conserve son seuil de
couverture du nouveau code à 80 %.

Motif : un seuil local rend la vérification reproductible même lorsque
SonarCloud n'est pas disponible. La marge entre les 90 % locaux et la couverture
actuelle évite qu'une petite évolution non critique bloque artificiellement le
projet. Ce seuil reste un garde-fou : il ne justifie ni tests artificiels ni
exclusion de code applicatif réel, et les règles métier critiques restent
prioritaires.

Impact : la commande de référence devient
`pytest --cov --cov-report=term-missing --cov-report=xml`. Le workflow conserve
le nom requis `Django checks`, vérifie aussi l'absence de migration manquante et
affiche les lignes non couvertes. SonarCloud analyse également les templates
Django et les workflows GitHub Actions.

L'analyse étendue a détecté des risques de chaîne d'approvisionnement dans le
workflow. Les actions GitHub sont donc référencées par SHA immuable avec leur
version lisible en commentaire. `requirements-ci.txt`, généré par `pip-compile`,
verrouille les versions directes et transitives ainsi que les empreintes SHA-256
utilisées sous Python 3.12. La CI impose `--require-hashes` et installe uniquement
des distributions binaires. `requirements.txt` et `requirements-dev.txt` restent
les manifests de plages supportées pour le développement.

`sonar.qualitygate.wait` n'est pas activé : les règles du dépôt exigent déjà les
checks distincts `Django checks` et `SonarCloud Code Analysis`. Attendre le
Quality Gate dans le job Django dupliquerait ce mécanisme et allongerait la CI.
L'analyse reste conditionnelle à `SONAR_TOKEN`; une pull request issue d'un fork
peut donc ne pas lancer le scanner et rester bloquée par le check Sonar requis
jusqu'à une exécution dans un contexte de confiance.

## 2026-06-15 - Administration concerts et ventes par permissions Django

Décision : ajouter une synthèse admin des ventes et des actions d'annulation/clôture avec des vues Django protégées par permissions, tout en enrichissant l'admin Django existant.

Motif : `EF11`, `EM9` et `RG7` demandent une preuve testable de gestion administrateur. Une page Django template reste cohérente avec la stack du projet et plus facile à démontrer/tester que l'admin Django seul. Les permissions explicites `concerts.view_concert`, `orders.view_order` et `concerts.change_concert` permettent de distinguer visiteur anonyme, utilisateur standard et gestionnaire autorisé.

Impact : le statut `closed` représente une vente clôturée sans assimiler ce cas à un concert complet. Les concerts annulés ou clôturés ne sont plus réservables, mais les commandes payées existantes restent visibles à leur propriétaire. Le suivi admin des ventes compte seulement les commandes payées et ne modifie pas la portée de `RG8`, qui reste l'isolation des commandes des utilisateurs standards.

## 2026-06-14 - Parcours panier et paiement simulé Django

Décision : exposer le parcours panier, checkout, paiement simulé, confirmation et refus avec des vues/templates Django, en réutilisant les services domaine existants.

Motif : les exigences `EF5` à `EF9`, `EF12`, `RG6` et les règles critiques de stock/quantité/paiement doivent être couvertes sans introduire de frontend séparé. La carte `4242424242424242` est acceptée ; toute autre valeur est refusée.

Impact : les URLs `/panier/`, `/panier/validation/` et `/paiement/` sont disponibles. Les commandes payées décrémentent le stock et figent les prix. Les commandes refusées restent non finales et ne modifient pas le stock. L'historique complet de commandes (`EF10`) reste hors scope.

## 2026-05-18 - Authentification utilisateur par Django

Décision : implémenter l'inscription, la connexion, la déconnexion POST et `Mon espace` avec les mécanismes Django auth et des templates Django en français.

Motif : les exigences `EF3`, `EF4`, `EM8`, `ENF3` et `ENF4` doivent être couvertes sans introduire de framework frontend séparé ni contourner le hachage et la gestion de session de Django.

Impact : les URLs `/inscription/`, `/connexion/`, `/deconnexion/` et `/mon-espace/` sont disponibles. L'inscription connecte automatiquement l'utilisateur et le redirige vers `Mon espace`. La déconnexion passe par un formulaire POST dans la navigation. `EM9` reste une fondation de rôle seulement, car les permissions d'administration des concerts sont hors de cette étape.

## 2026-05-06 - Domaine billetterie isolé en services testables

Décision : implémenter les modèles `Concert`, `SeatCategory`, `Cart`, `CartLine`, `Order`, `OrderLine` et `Payment`, avec des services pour l'ajout panier et le paiement simulé.

Motif : les règles de quantité, stock, date, statut de concert, paiement accepté/refusé et prix snapshots doivent être testables sans attendre les vues.

Impact : `EF5`, `EF7`, `EF8` et `EF9` sont documentées comme couvertures partielles domaine/service. Les confirmations, messages d'erreur visibles et parcours utilisateur restent à implémenter plus tard.

## 2026-05-06 - Applications `cart` et `payments` séparées

Décision : créer des applications Django dédiées `cart` et `payments` plutôt que de placer tout le domaine dans `orders`.

Motif : ce découpage correspond à l'architecture cible déjà documentée et garde les responsabilités lisibles.

Impact : `config.settings.INSTALLED_APPS` inclut maintenant `cart` et `payments` ; la couverture inclut aussi ces packages.

## 2026-05-06 - Panier et commande limités à un concert

Décision : un panier actif et une commande ne peuvent contenir qu'un seul concert.

Motif : la règle `EM3` limite à 6 billets pour un même concert et une même commande. Cette limite rend la première implémentation plus simple et explicite.

Impact : les services refusent les paniers multi-concerts et appliquent le plafond de 6 billets sur la quantité agrégée de toutes les catégories du concert.

## 2026-04-25 - Fondation Django technique

Décision : initialiser Django avec le module `config`, les apps `accounts`, `concerts` et `orders`, une page d'accueil minimale, pytest, coverage, Ruff, GitHub Actions et SonarCloud.

Motif : la demande courante portait sur une fondation technique exécutable et testable, pas sur les parcours métier complets.

Impact : les exigences couvertes restent limitées à la fondation utilisateur et qualité (`EF3` partiel, `EM8`, `ENF3`, `ENF5`, `ENF6`, `ENF7`). Les exigences de concerts, panier, paiement, stock et commandes restent non couvertes.

## 2026-04-25 - CustomUser e-mail dès le départ

Décision : créer `accounts.User` comme modèle utilisateur personnalisé avec e-mail unique comme identifiant.

Motif : le cahier des charges impose l'unicité e-mail (`EM8`) et l'utilisateur principal est défini autour de l'e-mail. Le faire avant les premières migrations évite une migration tardive complexe.

Impact : `AUTH_USER_MODEL = "accounts.User"` est configuré. Les mots de passe restent gérés par le hachage Django (`ENF3`). Les rôles spécifiques ne sont pas ajoutés ; les premiers droits administrateur utilisent `is_staff` et `is_superuser`.

## 2026-04-25 - SonarCloud conditionnel

Décision : enrichir `sonar-project.properties` avec les chemins existants et déclencher l'analyse CI seulement si `SONAR_TOKEN` est disponible.

Motif : la configuration SonarCloud doit être versionnée sans exposer de secret et ne doit pas référencer de chemins absents comme `e2e/`.

Impact : la CI ne doit pas échouer uniquement parce que le secret SonarCloud est absent.

## 2026-04-25 - Baseline documentaire avant initialisation Django

Décision : créer la documentation de dépôt et de validation avant d'initialiser le projet Django.

Motif : l'étape initiale prévoie de compléter la structure documentaire sans initialiser Django sauf s'il est déjà présent. Le dépôt ne contient actuellement aucun projet Django.

Impact : les documents de validation indiquent les exigences officielles et les tests prévus, mais ne revendiquent aucune couverture fonctionnelle déjà implémentée.

## 2026-04-25 - Stack principale Django

Décision : utiliser Python, Django, SQLite en développement, templates Django et Bootstrap via CDN.

Motif : ce choix est cohérent avec le besoin, limite la complexité frontend et permet de concentrer l'effort sur les exigences, les tests et la qualité.

Impact : React, Vite, TypeScript, Node.js et une application frontend séparée ne sont pas prévus.

## 2026-04-25 - Stratégie de validation

Décision : préparer une validation multi-couches avec tests unitaires, tests d'intégration, couverture, Ruff et scénarios fonctionnels Playwright.

Motif : le cahier des charges demande des preuves de qualité, une traçabilité exigences-tests, de l'analyse statique et de l'intégration continue.

Impact : les dépendances de développement incluent déjà `pytest`, `pytest-django`, `pytest-cov`, `coverage`, `ruff`, `freezegun`, `factory-boy` et `pytest-playwright`.

## 2026-04-25 - CI et SonarQube planifiés

Décision : documenter CI et SonarQube comme objectifs planifiés, pas comme fonctionnalités déjà livrées.

Motif : aucun workflow GitHub Actions ni fichier SonarQube n'est versionné pour l'instant.

Impact : `quality-ci.md` décrit les commandes et seuils cibles sans prétendre qu'ils sont actifs.
