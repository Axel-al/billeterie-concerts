# Exigences

Source officielle : `docs/brief/projet-validation-logiciel-e4a-2026.md`.

Ce document reformule les exigences sous une forme exploitable pour la validation. Les IDs officiels du cahier des charges sont conservés.

## Exigences fonctionnelles

| ID | Résumé testable |
| --- | --- |
| EF1 | Afficher la liste des concerts ouverts à la vente. |
| EF2 | Afficher la fiche détaillée d'un concert avec titre, artiste, date, lieu, catégories, prix et stock restant. |
| EF3 | Permettre la création d'un compte avec e-mail unique et mot de passe. |
| EF4 | Permettre la connexion d'un utilisateur enregistré. |
| EF5 | Permettre à un utilisateur connecté d'ajouter des billets au panier dans la limite du stock. |
| EF6 | Calculer automatiquement le total du panier selon les billets sélectionnés. |
| EF7 | Permettre la validation du panier par paiement simulé. |
| EF8 | En cas de paiement accepté, enregistrer la commande et afficher une confirmation. |
| EF9 | En cas de paiement refusé, ne pas créer de commande validée et afficher un message explicite. |
| EF10 | Permettre à un utilisateur connecté de consulter ses commandes passées. |
| EF11 | Permettre à l'administrateur de créer, modifier, suspendre ou annuler un concert. |
| EF12 | Mettre à jour le nombre de places disponibles après validation d'une commande. |

## Exigences métier

| ID | Résumé testable |
| --- | --- |
| EM1 | Ne jamais vendre plus de billets que le stock disponible. |
| EM2 | Une réservation contient au moins un billet. |
| EM3 | Une commande ne contient pas plus de six billets pour un même concert. |
| EM4 | Interdire la réservation d'un concert passé. |
| EM5 | Interdire la réservation d'un concert annulé. |
| EM6 | Une commande devient définitive seulement si le paiement est accepté. |
| EM7 | Le prix payé correspond au prix de la catégorie au moment de la validation. |
| EM8 | Deux comptes ne peuvent pas partager le même e-mail. |
| EM9 | Seul un administrateur peut créer ou modifier un concert. |
| EM10 | Toute commande est associée à un utilisateur, un concert, une date et un statut. |

## Exigences non fonctionnelles

| ID | Résumé testable |
| --- | --- |
| ENF1 | Les actions principales restent accessibles sans navigation excessive. |
| ENF2 | Une page standard s'affiche en moins de deux secondes en conditions normales. |
| ENF3 | Les mots de passe ne sont pas stockés en clair. |
| ENF4 | Les saisies invalides sont gérées proprement sans plantage. |
| ENF5 | Le projet intègre un outil d'analyse statique et vise un niveau de qualité défini. |
| ENF6 | Les fonctionnalités principales sont assez isolées pour être testées automatiquement. |
| ENF7 | Le projet est versionné et intègre un pipeline automatique de tests. |

## Règles de gestion

| ID | Résumé testable |
| --- | --- |
| RG1 | Un concert est réservable seulement s'il n'est pas passé, ouvert à la vente et avec du stock. |
| RG2 | Une catégorie est réservable seulement si le stock restant couvre la quantité demandée. |
| RG3 | La quantité saisie est un entier compris entre 1 et 6. |
| RG4 | Si le paiement échoue, la commande reste non validée. |
| RG5 | Si le paiement réussit, la commande passe à l'état payée et le stock est décrémenté. |
| RG6 | Un utilisateur non connecté ne peut pas accéder au paiement. |
| RG7 | Après annulation d'un concert par un administrateur, aucune nouvelle réservation n'est possible. |
| RG8 | Un utilisateur peut consulter uniquement ses propres commandes. |
