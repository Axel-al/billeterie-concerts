# Architecture

## Vue d'ensemble

Le projet est un monolithe Django rendu côté serveur. Il utilise l'ORM Django,
SQLite en développement, les templates Django et Bootstrap via CDN. Aucun
frontend séparé ni service externe de paiement n'est nécessaire.

```text
Navigateur
   |
   v
Vues Django + formulaires
   |
   v
Services métier transactionnels
   |
   v
Modèles Django / SQLite
```

## Applications

- `config` : réglages, URLs racines, ASGI et WSGI.
- `accounts` : utilisateur e-mail, inscription et authentification.
- `concerts` : catalogue, catégories, stock et gestion administrateur.
- `cart` : panier actif mono-concert et validation avant paiement.
- `orders` : commandes et lignes avec prix figés.
- `payments` : décision du paiement simulé et orchestration transactionnelle.

Les responsabilités détaillées sont décrites dans `apps.md`.

## Flux de consultation

1. `ConcertListView` sélectionne les concerts `open`, futurs et disposant de
   stock.
2. `ConcertDetailView` affiche toutes les catégories et explique les états non
   réservables.
3. Les brouillons restent inaccessibles publiquement.

## Flux de réservation

1. Un utilisateur connecté soumet une catégorie et une quantité.
2. `AddTicketForm` vérifie le type et les bornes.
3. `add_ticket_to_cart` revérifie quantité, concert, stock et unicité du
   concert.
4. `validate_cart_for_checkout` contrôle à nouveau l'état complet du panier.
5. `process_simulated_payment` verrouille panier et catégories dans une
   transaction.
6. Un paiement accepté crée une commande `paid`, fige les prix, décrémente le
   stock et valide le panier.
7. Un paiement refusé crée une commande `refused`, conserve le stock et laisse
   le panier actif.

La validation est volontairement répétée aux frontières afin qu'un attribut
HTML ou un contrôle antérieur ne soit jamais l'unique protection.

## Authentification et autorisation

- L'adresse e-mail est l'identifiant unique.
- Django gère le hachage des mots de passe et les sessions.
- Les vues panier, paiement et commandes exigent une authentification.
- Les commandes sont filtrées par propriétaire.
- La synthèse des ventes exige `concerts.view_concert` et
  `orders.view_order`.
- L'annulation et la clôture exigent `concerts.change_concert`.
- L'administration Django est réservée aux comptes autorisés.

## Transactions et stock

Le paiement accepté utilise `transaction.atomic`, `select_for_update` et un
décrément conditionnel avec `F`. Si le stock ne peut pas être décrémenté, la
commande, le paiement et la transition du panier sont annulés ensemble.

SQLite permet de tester le rollback et les invariants, mais ne remplace pas une
campagne de concurrence multi-processus sur une base de production.

## Interface

Les templates restent simples et sans JavaScript applicatif. Les formulaires de
réservation et paiement utilisent `novalidate` pour garantir des erreurs Django
en français, tout en conservant les attributs HTML utiles à la sémantique et
aux claviers adaptés.

## Fichiers importants

- `config/settings.py` : environnement et configuration Django.
- `config/urls.py` : routes racines et titres de l'administration.
- `cart/services.py` : quantité, stock et panier.
- `payments/services.py` : paiement et transaction de stock.
- `concerts/services.py` : administration et synthèse des ventes.
- `pyproject.toml` : pytest, coverage et Ruff.
- `.github/workflows/ci.yml` : pipeline automatique.

## Limites architecturales

- base SQLite locale ;
- panier limité à un concert ;
- paiement uniquement simulé ;
- pas de déploiement de production ;
- statuts complet et terminé non automatisés ;
- dépendance Bootstrap à jsDelivr en usage normal.
