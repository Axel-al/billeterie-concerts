# État courant du dépôt

Dernière mise à jour : 2026-06-15

## Synthèse

Le dépôt contient une application Django de billetterie prête pour la
présentation :

- catalogue et fiches de concerts ;
- inscription et authentification par e-mail ;
- panier, checkout et paiement simulé ;
- commandes payées et historique isolé par client ;
- gestion administrateur des concerts et des ventes ;
- interface et administration en français ;
- tests unitaires, intégration et Playwright ;
- couverture, Ruff, GitHub Actions et SonarQube Cloud ;
- documentation de validation et guide de soutenance.

La documentation d'installation principale est le `README.md` racine.

## Exigences

La matrice `docs/validation/matrice_tracabilite.md` documente la couverture de :

- `EF1` à `EF12` ;
- `EM1` à `EM10` ;
- `ENF1` à `ENF7` ;
- `RG1` à `RG8`.

La finalisation renforce particulièrement :

- `ENF4` et `RG3` : validation Django en français avec contraintes HTML
  conservées ;
- `EF11` et `EM9` : administration Django entièrement libellée en français.

## Comportement principal

- Un concert est réservable uniquement s'il est futur, `open` et disponible.
- La quantité totale est comprise entre 1 et 6.
- Un panier actif concerne un seul concert.
- Le paiement accepté utilise `4242424242424242`.
- Le stock diminue seulement après paiement accepté.
- Le paiement refusé conserve le stock et le panier actif.
- Une commande refusée est tracée mais absente de l'historique payé.
- Un client consulte uniquement ses propres commandes payées.
- Les permissions Django protègent la gestion des concerts et ventes.

## Validation des formulaires

Les formulaires de réservation et paiement utilisent `novalidate` pour laisser
Django afficher les erreurs en français. Ils conservent les attributs HTML
utiles :

- quantité : `required`, `type="number"`, `min="1"`, `max="6"` ;
- carte : `required`, `type="text"`, `maxlength="32"`,
  `inputmode="numeric"`.

Les mêmes contraintes sont appliquées dans les formulaires, modèles et services
métier.

## Données de démonstration

```bash
python manage.py migrate
python manage.py seed_demo_data
python manage.py createsuperuser
python manage.py runserver
```

`seed_demo_data` est idempotente et crée trois concerts avec sept catégories.
Les comptes client et administrateur ne sont pas versionnés.

## Résultats locaux

```text
python manage.py check                              OK
python manage.py makemigrations --check --dry-run  OK
ruff check .                                       OK
pytest                                             111 réussis
pytest --cov ...                                   99,6 %
pytest e2e --browser chromium ...                  6 réussis
git diff --check                                   OK
```

Le clone vierge a été validé avec création de l'environnement virtuel,
installation des dépendances, migrations et double exécution du jeu de
démonstration.

## Vérification navigateur

Les parcours suivants ont été contrôlés :

- catalogue et fiche ;
- connexion ;
- panier et paiement refusé ;
- nouvelle tentative acceptée ;
- historique ;
- quantité supérieure à 6 avec message français ;
- synthèse des ventes ;
- administration Django française.

La vérification a conduit à corriger les messages natifs dépendant de la langue
du navigateur et les anciens noms anglais de l'administration.

## Qualité distante

La référence `main` au début de la finalisation, commit `946ad8c`, possède les
checks `Django checks` et `SonarCloud Code Analysis` réussis. Le résultat final
de la branche est contrôlé sur sa pull request avant fusion.

## Limites

- paiement simulé ;
- panier mono-concert ;
- SQLite et absence de preuve de concurrence multi-processus en production ;
- aucun déploiement de production ;
- Bootstrap chargé depuis jsDelivr en usage normal ;
- performance mesurée sous conditions Chromium contrôlées ;
- transitions automatiques vers `sold_out` et `finished` non implémentées.

## Références

- `docs/repository/architecture.md`
- `docs/repository/data-model.md`
- `docs/repository/domain-rules.md`
- `docs/repository/testing.md`
- `docs/repository/quality-ci.md`
- `docs/validation/demo_soutenance.md`
- `docs/validation/rapport_qualite.md`
