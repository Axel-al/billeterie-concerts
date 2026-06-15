# Guide de démonstration pour la soutenance

## Objectif

Présenter en une séquence courte les fonctionnalités principales, les règles
métier critiques et les preuves de qualité du projet.

## Préparation

Depuis un clone propre, préparer l'application :

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py createsuperuser
python manage.py runserver
```

Ouvrir `http://127.0.0.1:8000/`.

La commande `seed_demo_data` crée notamment :

- `Nuit Électrique`, futur et ouvert à la vente ;
- `Silence Annulé`, futur mais annulé ;
- `Hier Encore`, passé et terminé.

Créer le compte client pendant la démonstration ou avant celle-ci par la page
`Inscription`. Aucun identifiant ou mot de passe de démonstration n'est
versionné.

Ne pas annuler ni clôturer `Nuit Électrique` avant la fin des parcours client.

## 1. Liste des concerts

1. Depuis l'accueil, sélectionner `Voir les concerts`.
2. Montrer que seul `Nuit Électrique` apparaît dans le catalogue.
3. Expliquer que les concerts annulés, passés, clôturés ou sans stock sont
   masqués de cette liste.

Preuves : `EF1`, `EM4`, `EM5`, `RG1`.

## 2. Détail d'un concert

1. Ouvrir `Nuit Électrique`.
2. Montrer le titre, l'artiste, la date, le lieu, la description, les
   catégories, les prix et les stocks restants.
3. Montrer le lien `Se connecter pour réserver`.
4. Ouvrir directement la fiche de `Silence Annulé` depuis l'administration ou
   son URL afin de montrer le motif d'indisponibilité et l'absence de CTA.

Preuves : `EF2`, `EM5`, `RG1`, `RG7`.

## 3. Création de compte ou connexion

1. Utiliser `Inscription` pour créer un client avec une adresse e-mail unique,
   ou se connecter avec un compte client préparé.
2. Montrer `Mon espace` et l'adresse e-mail du compte.
3. Signaler que les mots de passe sont gérés et hachés par Django.

Preuves : `EF3`, `EF4`, `EM8`, `ENF3`, `ENF4`.

## 4. Panier

1. Revenir sur `Nuit Électrique`.
2. Sélectionner la catégorie `Fosse` et une quantité de `2`.
3. Ajouter au panier.
4. Montrer les lignes, le prix unitaire, la quantité et le total calculé.
5. Ouvrir `Valider le panier`.

Preuves : `EF5`, `EF6`, `EM1`, `EM2`, `EM3`, `RG2`, `RG3`.

## 5. Paiement accepté

1. Sélectionner `Passer au paiement`.
2. Saisir la carte simulée acceptée :

   ```text
   4242424242424242
   ```

3. Montrer la confirmation, le total payé et les prix figés.
4. Revenir sur la fiche du concert pour montrer que le stock a diminué.

Preuves : `EF7`, `EF8`, `EF12`, `EM6`, `EM7`, `EM10`, `RG5`.

## 6. Historique des commandes

1. Ouvrir `Mes commandes`.
2. Montrer que la commande payée apparaît.
3. Ouvrir son détail.
4. Expliquer que les vues filtrent les commandes par propriétaire et excluent
   les tentatives refusées.

Preuves : `EF10`, `RG8`.

## 7. Paiement refusé

1. Revenir sur `Nuit Électrique` et ajouter un billet pour créer un nouveau
   panier actif.
2. Aller jusqu'au paiement.
3. Saisir toute autre valeur non vide, par exemple :

   ```text
   4000000000000000
   ```

4. Montrer le message `Paiement refusé`.
5. Montrer que le panier reste disponible pour une nouvelle tentative et que
   le stock n'a pas changé.
6. Vérifier que cette tentative n'apparaît pas dans `Mes commandes`.

Preuves : `EF9`, `EM6`, `RG4`.

## 8. Quantité invalide

1. Depuis une fiche réservable, saisir `7`.
2. Soumettre le formulaire.
3. Montrer le message français
   `La quantité ne peut pas dépasser 6 billets.`
4. Expliquer que les attributs HTML `required`, `min`, `max` et le type
   numérique sont conservés, mais que Django reste l'autorité de validation.

Preuves : `EM3`, `ENF4`, `RG3`.

## 9. Gestion administrateur des concerts

1. Se déconnecter du compte client puis se connecter avec le superutilisateur.
2. Ouvrir `Administration ventes`.
3. Montrer les commandes payées, billets vendus, chiffre d'affaires et stocks.
4. Ouvrir l'administration Django, entièrement libellée en français.
5. Créer un concert de démonstration avec une catégorie et du stock.
6. Modifier ce concert, puis utiliser la synthèse pour clôturer ou annuler ses
   ventes.
7. Montrer que le concert n'est plus réservable.

Preuves : `EF11`, `EM9`, `RG7`.

## 10. Tests, CI, couverture et SonarQube

Présenter les commandes locales :

```bash
ruff check .
pytest
pytest --cov --cov-report=term-missing --cov-report=xml
pytest e2e --browser chromium \
  --tracing=retain-on-failure \
  --output=test-results/playwright \
  -rP
```

Montrer ensuite :

- la matrice `docs/validation/matrice_tracabilite.md` ;
- le rapport `docs/validation/rapport_qualite.md` ;
- le workflow `.github/workflows/ci.yml` ;
- les checks GitHub `Django checks` et `SonarCloud Code Analysis` ;
- le Quality Gate SonarQube Cloud ;
- la couverture applicative supérieure au seuil local de 90 % ;
- la mesure `ENF2` sous Chromium, en rappelant ses conditions contrôlées.

Preuves : `ENF1`, `ENF2`, `ENF5`, `ENF6`, `ENF7`.

## Limites à annoncer

- Le paiement est simulé et aucun numéro de carte n'est stocké.
- Un panier est limité à un seul concert.
- SQLite convient à la démonstration locale ; la concurrence multi-processus
  n'est pas validée comme elle le serait avec une base de production.
- Aucun déploiement de production n'est fourni.
- Bootstrap est chargé depuis jsDelivr en usage normal.
- La mesure de performance est une preuve de laboratoire CI, pas une garantie
  pour tous les appareils et réseaux.
