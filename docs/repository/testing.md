# Stratégie de test

## Résultats

Vérification locale finale du 15 juin 2026 :

- 111 tests Django réussis ;
- 6 tests Playwright Chromium réussis ;
- couverture applicative avec branches : 99,6 % ;
- seuil bloquant : 90 %.

## Répartition

| Fichier | Périmètre |
| --- | --- |
| `tests/test_accounts.py` | utilisateur e-mail, unicité, hachage et manager |
| `tests/test_authentication_views.py` | inscription, connexion, déconnexion et espace |
| `tests/test_concert_views.py` | catalogue, fiches et états non réservables |
| `tests/test_booking_flow.py` | formulaires, panier, paiement et isolation |
| `tests/test_order_history.py` | historique, détail et propriétaire |
| `tests/test_admin_concert_management.py` | permissions, ventes et administration |
| `tests/test_core_domain.py` | quantité, stock, paiement, snapshots et rollback |
| `tests/test_template_quality.py` | SRI et qualité statique des templates |
| `tests/test_settings.py` | lecture des variables d'environnement |
| `e2e/test_nominal_booking_flow.py` | parcours nominal et quantité invalide |
| `e2e/test_page_performance.py` | LCP de quatre pages standards |

## Commandes

Tests Django :

```bash
pytest
```

Couverture :

```bash
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
```

Playwright :

```bash
pytest e2e --browser chromium \
  --tracing=retain-on-failure \
  --output=test-results/playwright \
  -rP
```

Checks complémentaires :

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
ruff check .
```

## Données de test

Les scénarios Playwright utilisent `pytest-django`, `transactional_db` et
`live_server`. Ils créent leurs propres utilisateurs, concerts, catégories et
commandes dans la base de test. Ils ne dépendent pas de `db.sqlite3` ni du jeu
de démonstration.

`freezegun` stabilise les tests sensibles aux dates. Les helpers locaux
restent préférés à des factories lorsque le montage est court et spécifique.

## Performance

`ENF2` mesure le Largest Contentful Paint sous Chromium sur l'accueil, le
catalogue, une fiche et l'historique authentifié. Le test emploie un contexte
froid par page et rejoue localement les ressources Bootstrap correspondant aux
empreintes SRI.

Le seuil est de 2 000 ms. Cette preuve est reproductible en CI mais ne couvre
pas tous les appareils, réseaux ou états du CDN.

## Couverture

Les packages applicatifs sont définis par `source_pkgs` dans `pyproject.toml`.
Les tests ne font pas partie du dénominateur. Les migrations, `manage.py`,
`config/asgi.py` et `config/wsgi.py` sont exclus.

Les deux instructions défensives restantes dans `payments/services.py` ne sont
pas forcées par des données incohérentes uniquement pour atteindre 100 %.

## Priorités métier

Les preuves prioritaires concernent :

- absence de survente ;
- bornes 1 à 6 ;
- paiement accepté avant décrément ;
- rollback atomique ;
- isolation des commandes ;
- permissions administrateur ;
- unicité de l'e-mail et hachage du mot de passe.

La correspondance détaillée est maintenue dans
`docs/validation/matrice_tracabilite.md`.
