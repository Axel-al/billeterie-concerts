# Rapport qualité

Dernière mise à jour : 2026-06-15

## Synthèse

L'application Django est exécutable et accompagnée de preuves automatisées :

- 111 tests Django unitaires et d'intégration ;
- 6 tests Playwright Chromium ;
- couverture applicative avec branches à 99,6 % ;
- seuil local bloquant fixé à 90 % ;
- Ruff, checks Django et contrôle de migrations ;
- GitHub Actions ;
- Quality Gate SonarQube Cloud ;
- matrice de traçabilité reliant exigences, code et tests.

Les exigences `EF1` à `EF12`, `EM1` à `EM10`, `ENF1` à `ENF7` et `RG1` à
`RG8` disposent d'une preuve documentée dans `matrice_tracabilite.md`.

## Outillage

| Outil | Usage | Déclaration |
| --- | --- | --- |
| Django | Application, ORM, authentification et administration | `requirements.txt` |
| pytest / pytest-django | Tests unitaires et d'intégration | `requirements-dev.txt` |
| pytest-playwright | Parcours fonctionnels et performance | `requirements-dev.txt`, `e2e/` |
| coverage.py / pytest-cov | Couverture de branches et XML | `pyproject.toml` |
| Ruff | Analyse statique Python | `pyproject.toml` |
| freezegun | Stabilisation des dates de test | `requirements-dev.txt` |
| GitHub Actions | Pipeline automatique | `.github/workflows/ci.yml` |
| SonarQube Cloud | Quality Gate externe | `sonar-project.properties` |

`factory-boy` est déclaré pour permettre une évolution des fixtures, mais les
helpers actuels restent plus lisibles pour ce volume de données.

## Résultats locaux

Commandes exécutées :

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
ruff check .
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
pytest e2e --browser chromium \
  --tracing=retain-on-failure \
  --output=test-results/playwright \
  -rP
```

Résultats observés :

- 111 tests Django réussis ;
- 6 tests Playwright réussis ;
- 838 instructions applicatives mesurées ;
- 2 instructions non couvertes ;
- 102 branches mesurées ;
- couverture totale : 99,6 % ;
- aucune migration manquante ;
- aucune erreur Ruff.

Les deux lignes non couvertes dans `payments/services.py` défendent des
incohérences entre un panier déjà validé et les catégories verrouillées au
moment du paiement. Des données artificiellement incohérentes ne sont pas
créées uniquement pour atteindre 100 %.

## Validation des formulaires

Les formulaires de réservation et de paiement utilisent `novalidate` afin que
les erreurs de référence proviennent de Django et soient affichées en français.
Les attributs HTML utiles restent présents :

- réservation : `required`, `type="number"`, `min="1"` et `max="6"` ;
- paiement : `required`, `type="text"`, `maxlength="32"` et
  `inputmode="numeric"`.

Les mêmes contraintes sont appliquées côté Django :

- champs et messages des formulaires ;
- validateurs des modèles ;
- services métier de quantité, stock et paiement.

Le test Playwright
`test_invalid_quantity_displays_french_server_validation` vérifie la borne
haute et le message français dans un navigateur réel.

## Couverture

Coverage mesure les packages `accounts`, `concerts`, `cart`, `orders`,
`payments` et `config`. Les migrations, `manage.py`, `config/asgi.py` et
`config/wsgi.py` sont exclus car ils ne portent pas de logique applicative
écrite pour le projet.

Le rapport `coverage.xml` utilise des chemins relatifs non ambigus, par exemple
`accounts/admin.py`. Le script
`.github/scripts/validate_coverage_xml.py` refuse les chemins absolus,
introuvables ou ambigus avant l'analyse SonarQube Cloud.

## Tests fonctionnels

Le scénario nominal couvre le catalogue, la fiche, la connexion, le panier, le
checkout, le paiement accepté, la confirmation, le stock et l'historique.

Un second scénario vérifie une quantité supérieure à six, la conservation des
attributs HTML et l'affichage du message français produit par Django.

Les paiements refusés, permissions, stocks insuffisants, accès d'un autre
utilisateur et autres valeurs limites sont couverts par les tests
d'intégration.

## Performance ENF2

Le test `e2e/test_page_performance.py` utilise Chromium, `live_server`, un
viewport 1366 × 768, un contexte froid par page, aucune limitation CPU/réseau
et les fichiers Bootstrap 5.3.3 locaux correspondant aux empreintes SRI du
template.

Résultats observés lors de la vérification finale locale :

| Page | LCP | Durée de chargement |
| --- | ---: | ---: |
| Accueil | 40 ms | 35,0 ms |
| Catalogue | 36 ms | 32,9 ms |
| Fiche concert | 48 ms | 25,8 ms |
| Historique authentifié | 36 ms | 31,0 ms |

Le seuil est de 2 000 ms. Cette mesure valide un environnement de laboratoire
CI contrôlé et ne garantit pas la performance de tous les appareils, réseaux
ou états du CDN en production.

## Intégration continue

Le job `Django checks` exécute :

1. installation Python 3.12 depuis `requirements-ci.txt` avec empreintes ;
2. Ruff ;
3. checks Django ;
4. contrôle de dérive des migrations ;
5. pytest avec couverture et XML ;
6. validation du XML ;
7. installation de Chromium ;
8. tests Playwright ;
9. publication des traces en cas d'échec ;
10. analyse SonarQube Cloud lorsque `SONAR_TOKEN` est disponible.

Les actions GitHub sont épinglées par SHA immuable. Le lock CI impose
`--require-hashes` et `--only-binary=:all:`.

## SonarQube Cloud

Le check `SonarCloud Code Analysis` de référence sur `main`, commit
`946ad8c`, a réussi le 15 juin 2026 avec :

- Quality Gate réussi ;
- 0 nouvelle anomalie ;
- 0 hotspot de sécurité ;
- 99,5 % de couverture du nouveau code ;
- 0,0 % de duplication sur le nouveau code.

La branche de finalisation doit obtenir à son tour les checks `Django checks`
et `SonarCloud Code Analysis` avant toute fusion.

## Limites et risques résiduels

- Le paiement est simulé ; aucun prestataire réel n'est intégré.
- Le panier est volontairement limité à un seul concert.
- SQLite ne fournit pas une preuve de concurrence multi-processus équivalente à
  une base de production.
- Les transitions automatiques vers `sold_out` et `finished` ne sont pas
  implémentées ; la réservabilité contrôle directement stock, date et statut.
- Les commandes refusées sont conservées comme traces non finales, mais ne sont
  pas affichées dans l'historique des achats payés.
- Bootstrap dépend de jsDelivr en usage normal.
- Aucun déploiement ni durcissement de production n'est fourni.
