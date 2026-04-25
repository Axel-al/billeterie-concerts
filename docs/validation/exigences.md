# Exigences

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

Ce document reformule les exigences sous une forme exploitable pour la validation. Les IDs officiels du cahier des charges sont conserves.

## Exigences fonctionnelles

| ID | Resume testable |
| --- | --- |
| EF1 | Afficher la liste des concerts ouverts a la vente. |
| EF2 | Afficher la fiche detaillee d'un concert avec titre, artiste, date, lieu, categories, prix et stock restant. |
| EF3 | Permettre la creation d'un compte avec email unique et mot de passe. |
| EF4 | Permettre la connexion d'un utilisateur enregistre. |
| EF5 | Permettre a un utilisateur connecte d'ajouter des billets au panier dans la limite du stock. |
| EF6 | Calculer automatiquement le total du panier selon les billets selectionnes. |
| EF7 | Permettre la validation du panier par paiement simule. |
| EF8 | En cas de paiement accepte, enregistrer la commande et afficher une confirmation. |
| EF9 | En cas de paiement refuse, ne pas creer de commande validee et afficher un message explicite. |
| EF10 | Permettre a un utilisateur connecte de consulter ses commandes passees. |
| EF11 | Permettre a l'administrateur de creer, modifier, suspendre ou annuler un concert. |
| EF12 | Mettre a jour le nombre de places disponibles apres validation d'une commande. |

## Exigences metier

| ID | Resume testable |
| --- | --- |
| EM1 | Ne jamais vendre plus de billets que le stock disponible. |
| EM2 | Une reservation contient au moins un billet. |
| EM3 | Une commande ne contient pas plus de six billets pour un meme concert. |
| EM4 | Interdire la reservation d'un concert passe. |
| EM5 | Interdire la reservation d'un concert annule. |
| EM6 | Une commande devient definitive seulement si le paiement est accepte. |
| EM7 | Le prix paye correspond au prix de la categorie au moment de la validation. |
| EM8 | Deux comptes ne peuvent pas partager le meme email. |
| EM9 | Seul un administrateur peut creer ou modifier un concert. |
| EM10 | Toute commande est associee a un utilisateur, un concert, une date et un statut. |

## Exigences non fonctionnelles

| ID | Resume testable |
| --- | --- |
| ENF1 | Les actions principales restent accessibles sans navigation excessive. |
| ENF2 | Une page standard s'affiche en moins de deux secondes en conditions normales. |
| ENF3 | Les mots de passe ne sont pas stockes en clair. |
| ENF4 | Les saisies invalides sont gerees proprement sans plantage. |
| ENF5 | Le projet integre un outil d'analyse statique et vise un niveau de qualite defini. |
| ENF6 | Les fonctionnalites principales sont assez isolees pour etre testees automatiquement. |
| ENF7 | Le projet est versionne et integre un pipeline automatique de tests. |

## Regles de gestion

| ID | Resume testable |
| --- | --- |
| RG1 | Un concert est reservable seulement s'il n'est pas passe, ouvert a la vente et avec du stock. |
| RG2 | Une categorie est reservable seulement si le stock restant couvre la quantite demandee. |
| RG3 | La quantite saisie est un entier compris entre 1 et 6. |
| RG4 | Si le paiement echoue, la commande reste non validee. |
| RG5 | Si le paiement reussit, la commande passe a l'etat payee et le stock est decremente. |
| RG6 | Un utilisateur non connecte ne peut pas acceder au paiement. |
| RG7 | Apres annulation d'un concert par un administrateur, aucune nouvelle reservation n'est possible. |
| RG8 | Un utilisateur peut consulter uniquement ses propres commandes. |
