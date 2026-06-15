# Architecture

## État actuel

Le dépôt contient maintenant une application Django exécutable avec un noyau domaine testé.

- `config` porte la configuration Django, les URLs racines, ASGI et WSGI.
- `accounts` contient le modèle utilisateur personnalisé basé sur l'e-mail unique.
- `concerts` contient les concerts, catégories de places, statuts et stocks.
- `cart` contient les paniers mono-concert et lignes de panier.
- `orders` contient les commandes et lignes figeant les prix au moment du paiement.
- `payments` contient le paiement simulé accepté/refusé.
- `templates/` contient le gabarit de base Bootstrap CDN et une page d'accueil française minimale.

Le stockage local est SQLite. Les migrations Django sont en place pour le modèle utilisateur et le noyau domaine, mais la base locale `db.sqlite3` n'est pas versionnée.

## Architecture cible

L'architecture cible reste une application Django monolithe, organisée autour de domaines métier simples et testables :

- consultation des concerts ;
- comptes et authentification ;
- panier mono-concert dans cette première version ;
- commandes ;
- paiement simulé au niveau service ;
- administration des concerts.

Le stockage local cible est SQLite pour le développement. La persistance sera portée par l'ORM Django et les migrations Django.

## Principes

- Garder le domaine métier proche des modèles et services Django.
- Isoler les règles sensibles dans du code testable, notamment le stock, les quantités, les statuts de concert et le paiement.
- Utiliser les vues Django et les templates pour limiter la complexité frontend.
- Introduire des services métier seulement quand une règle devient partagée entre plusieurs vues, formulaires ou commandes.
- Utiliser `is_staff` et `is_superuser` pour les premiers droits administrateur ; un champ de rôle dédié sera ajouté seulement si un cas d'usage le justifie.

## Flux cible de réservation

1. Un visiteur consulte les concerts ouverts.
2. Un utilisateur connecté ajoute une sélection valide au panier.
3. Le panier calcule son total à partir des prix applicables et reste limité à un seul concert.
4. Le paiement simulé accepte ou refuse la validation.
5. En cas de succès seulement, la commande devient payée et le stock est décrémenté.
6. En cas de refus, la commande ne devient pas définitive et le stock reste inchangé.

## Points d'attention

- Les transactions seront importantes pour éviter la survendue.
- La vérification du stock devra être faite au moment de la validation, pas seulement à l'ajout au panier.
- Les commandes devront être cloisonnées par utilisateur.
- Les mots de passe seront gérés par le système d'authentification Django, jamais stockés en clair.
- Le modèle utilisateur personnalisé a été créé dès le départ afin d'éviter une migration tardive coûteuse.
