# Architecture

## Etat actuel

Le depot contient maintenant une application Django executable avec un noyau domaine teste.

- `config` porte la configuration Django, les URLs racines, ASGI et WSGI.
- `accounts` contient le modele utilisateur personnalise base sur l'email unique.
- `concerts` contient les concerts, categories de places, statuts et stocks.
- `cart` contient les paniers mono-concert et lignes de panier.
- `orders` contient les commandes et lignes figeant les prix au moment du paiement.
- `payments` contient le paiement simule accepte/refuse.
- `templates/` contient le gabarit de base Bootstrap CDN et une page d'accueil francaise minimale.

Le stockage local est SQLite. Les migrations Django sont en place pour le modele utilisateur et le noyau domaine, mais la base locale `db.sqlite3` n'est pas versionnee.

## Architecture cible

L'architecture cible reste une application Django monolithe, organisee autour de domaines metier simples et testables :

- consultation des concerts ;
- comptes et authentification ;
- panier mono-concert dans cette premiere version ;
- commandes ;
- paiement simule au niveau service ;
- administration des concerts.

Le stockage local cible est SQLite pour le developpement. La persistance sera portee par l'ORM Django et les migrations Django.

## Principes

- Garder le domaine metier proche des modeles et services Django.
- Isoler les regles sensibles dans du code testable, notamment le stock, les quantites, les statuts de concert et le paiement.
- Utiliser les vues Django et les templates pour limiter la complexite frontend.
- Introduire des services metier seulement quand une regle devient partagee entre plusieurs vues, formulaires ou commandes.
- Utiliser `is_staff` et `is_superuser` pour les premiers droits administrateur ; un champ de role dedie sera ajoute seulement si un cas d'usage le justifie.

## Flux cible de reservation

1. Un visiteur consulte les concerts ouverts.
2. Un utilisateur connecte ajoute une selection valide au panier.
3. Le panier calcule son total a partir des prix applicables et reste limite a un seul concert.
4. Le paiement simule accepte ou refuse la validation.
5. En cas de succes seulement, la commande devient payee et le stock est decremente.
6. En cas de refus, la commande ne devient pas definitive et le stock reste inchange.

## Points d'attention

- Les transactions seront importantes pour eviter la survendue.
- La verification du stock devra etre faite au moment de la validation, pas seulement a l'ajout au panier.
- Les commandes devront etre cloisonnees par utilisateur.
- Les mots de passe seront geres par le systeme d'authentification Django, jamais stockes en clair.
- Le modele utilisateur personnalise a ete cree des le depart afin d'eviter une migration tardive couteuse.
