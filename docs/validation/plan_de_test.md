# Plan de test

## Objectif

Démontrer que l'application respecte les exigences officielles par des preuves
automatisées, reproductibles localement et exécutées en intégration continue.

## Périmètre couvert

Les tests couvrent :

- consultation du catalogue et des fiches ;
- inscription, authentification et isolation des comptes ;
- quantité, stock et panier mono-concert ;
- paiement simulé accepté ou refusé ;
- rollback transactionnel en cas d'échec du décrément ;
- historique et détail des commandes payées ;
- permissions et gestion administrateur ;
- interface française et validation des formulaires ;
- performance navigateur contrôlée ;
- analyse statique, couverture et CI.

La matrice `matrice_tracabilite.md` associe les tests aux exigences `EF1` à
`EF12`, `EM1` à `EM10`, `ENF1` à `ENF7` et `RG1` à `RG8`.

## Niveaux de test

| Niveau | Cible | Outils | Exemples |
| --- | --- | --- | --- |
| Unitaire et domaine | Validateurs, modèles et services | pytest, pytest-django | quantité, stock, prix figé, paiement, rollback |
| Intégration Django | Formulaires, vues, ORM, sessions et permissions | pytest-django | inscription, panier, historique, administration |
| Fonctionnel navigateur | Parcours utilisateur | pytest-playwright, Chromium | réservation nominale, quantité invalide en français |
| Performance navigateur | Pages standards contrôlées | Playwright, LCP | accueil, catalogue, fiche, historique |
| Qualité | Code et couverture | Ruff, coverage.py, SonarQube Cloud | seuil local 90 %, Quality Gate |

## Jeux de données

- Concert ouvert avec catégories et stock.
- Concert complet, annulé, clôturé, passé, terminé ou brouillon.
- Quantités `0`, `1`, `6`, `7`, valeur non entière et agrégats multi-lignes.
- Stock inférieur, égal ou supérieur à la demande.
- Client, autre client, gestionnaire avec permissions et superutilisateur.
- Panier vide, actif, invalide ou déjà validé.
- Carte acceptée `4242424242424242`, autre carte, valeur vide et valeur trop
  longue.
- Commande payée, commande refusée et échec atomique simulé.

## Techniques de conception

- Classes d'équivalence : `classes_equivalence.md`.
- Valeurs limites : `valeurs_limites.md`.
- Tables de décision : `table_decision.md`.
- Cycles de vie : `diagrammes_etats.md`.
- Critères d'acceptation : `criteres_acceptation.md`.

## Critères de sortie

- Toutes les règles métier critiques possèdent au moins une preuve automatisée.
- Tous les IDs officiels sont reliés à une implémentation et à des tests.
- Ruff, les checks Django, le contrôle des migrations et pytest passent.
- La couverture applicative avec branches reste supérieure ou égale à 90 %.
- Les scénarios Playwright Chromium passent.
- GitHub Actions et le Quality Gate SonarQube Cloud sont verts.
- Aucun secret, base locale ou rapport généré n'est versionné.

## Commandes de référence

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
ruff check .
pytest
pytest --cov --cov-report=term-missing --cov-report=xml
python .github/scripts/validate_coverage_xml.py
pytest e2e --browser chromium \
  --tracing=retain-on-failure \
  --output=test-results/playwright \
  -rP
```

La mesure de `ENF2` utilise un environnement navigateur local contrôlé et ne
constitue pas une preuve de performance pour tous les appareils ou réseaux de
production.
