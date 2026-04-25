# Architecture

## Etat actuel

Le depot ne contient pas encore d'architecture applicative executable. Aucun projet Django n'est initialise dans cette baseline documentaire.

## Architecture cible

L'architecture cible est une application Django monolithe, organisee autour de domaines metier simples et testables :

- consultation des concerts ;
- comptes et authentification ;
- panier ;
- commandes ;
- paiement simule ;
- administration des concerts.

Le stockage local cible est SQLite pour le developpement. La persistance sera portee par l'ORM Django et les migrations Django.

## Principes

- Garder le domaine metier proche des modeles et services Django.
- Isoler les regles sensibles dans du code testable, notamment le stock, les quantites, les statuts de concert et le paiement.
- Utiliser les vues Django et les templates pour limiter la complexite frontend.
- Introduire des services metier seulement quand une regle devient partagee entre plusieurs vues, formulaires ou commandes.

## Flux cible de reservation

1. Un visiteur consulte les concerts ouverts.
2. Un utilisateur connecte ajoute une selection valide au panier.
3. Le panier calcule son total a partir des prix applicables.
4. Le paiement simule accepte ou refuse la validation.
5. En cas de succes seulement, la commande devient payee et le stock est decremente.
6. En cas de refus, la commande ne devient pas definitive et le stock reste inchange.

## Points d'attention

- Les transactions seront importantes pour eviter la survendue.
- La verification du stock devra etre faite au moment de la validation, pas seulement a l'ajout au panier.
- Les commandes devront etre cloisonnees par utilisateur.
- Les mots de passe seront geres par le systeme d'authentification Django, jamais stockes en clair.
