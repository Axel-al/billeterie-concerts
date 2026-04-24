# Cahier des charges

# Projet de billetterie en ligne pour concerts

Ce document présente le besoin métier, le périmètre attendu, les règles de gestion et les attendus qualité du projet que vous devrez concevoir, développer, tester et présenter. L'objectif n'est pas seulement de produire une application fonctionnelle, mais de démontrer sa qualité au moyen d'exigences testables, de cas de test, de traçabilité, d'analyse statique et d'intégration continue.

## 1. Contexte

Une société souhaite mettre en place une application web de billetterie permettant aux utilisateurs de consulter des concerts, réserver des places et effectuer un paiement en ligne simulé.

Vous devrez réaliser ce projet de bout en bout, depuis l'analyse du besoin jusqu'à la démonstration finale, en intégrant une démarche complète de validation logicielle.

## 2. Objectifs du projet

Développer une application répondant à un besoin métier réaliste.

Formaliser un besoin sous forme d’exigences claires et testables.

Concevoir et implémenter les fonctionnalités principales.

Mettre en place une stratégie de validation et de test.

Démontrer la qualité du logiciel par des preuves : tests, couverture, traçabilité, analyse statique et pipeline CI.

## 3. Périmètre fonctionnel

### 3.1 Consultation des concerts

Vous devez permettre à un visiteur de consulter la liste des concerts disponibles.

Vous devez permettre l’affichage du détail d’un concert : titre, artiste, date, heure, lieu, catégories de places, prix et nombre de places restantes.

### 3.2 Création de compte et authentification

Vous devez permettre la création d’un compte utilisateur.

Vous devez permettre la connexion, la déconnexion et l’accès à un espace personnel.

### 3.3 Réservation de billets

Un utilisateur connecté doit pouvoir sélectionner un concert, choisir une catégorie de place, indiquer une quantité de billets et ajouter cette sélection à son panier.

Le montant total du panier doit être calculé automatiquement.

### 3.4 Paiement

Vous devez permettre la validation du panier par un paiement simulé.

En cas de succès, une confirmation de commande doit être affichée.

En cas d’échec, un message explicite doit être affiché et la commande ne doit pas être validée.

### 3.5 Gestion des commandes

Un utilisateur connecté doit pouvoir consulter l’historique de ses commandes et le détail de ses billets achetés.

### 3.6 Administration

Un administrateur doit pouvoir créer un concert, modifier ses informations, définir le nombre de places par catégorie, consulter les ventes et clôturer ou annuler un concert.

## 4. Acteurs

**Visiteur** : utilisateur non connecté pouvant consulter les concerts.

**Client** : utilisateur connecté pouvant réserver et payer des billets.

**Administrateur** : utilisateur disposant des droits de gestion sur les concerts et les ventes.

## 5. Exigences fonctionnelles

**EF1** - Le système doit afficher la liste des concerts ouverts à la vente.

**EF2** - Le système doit permettre de consulter la fiche détaillée d’un concert comprenant au minimum : titre, artiste, date, lieu, catégories de places, prix et stock restant.

**EF3** - Le système doit permettre à un utilisateur de créer un compte avec une adresse email unique et un mot de passe.

**EF4** - Le système doit permettre à un utilisateur enregistré de se connecter avec ses identifiants.

**EF5** - Le système doit permettre à un utilisateur connecté d’ajouter un ou plusieurs billets à son panier, dans la limite du stock disponible.

**EF6** - Le système doit calculer automatiquement le montant total du panier en fonction des billets sélectionnés.

**EF7** - Le système doit permettre la validation d’un panier par un paiement simulé.

**EF8** - En cas de paiement accepté, le système doit enregistrer la commande et afficher une confirmation.

**EF9** - En cas de paiement refusé, le système ne doit pas créer de commande validée et doit afficher un message explicite.

**EF10** - Le système doit permettre à un utilisateur connecté de consulter ses commandes passées.

**EF11** - L’administrateur doit pouvoir créer, modifier, suspendre ou annuler un concert.

**EF12** - Le système doit mettre à jour le nombre de places disponibles après validation d’une commande.

## 6. Exigences métier

**EM1** - Il est interdit de vendre plus de billets que le stock disponible pour une catégorie donnée.

**EM2** - Une réservation doit contenir au moins 1 billet.

**EM3** - Une réservation ne peut pas contenir plus de 6 billets pour un même concert et une même commande.

**EM4** - Il est interdit de réserver des billets pour un concert dont la date est passée.

**EM5** - Il est interdit de réserver des billets pour un concert annulé.

**EM6** - Une commande ne devient définitive que si le paiement est accepté.

**EM7** - Le prix payé doit correspondre au prix de la catégorie sélectionnée au moment de la validation.

**EM8** - Deux comptes ne peuvent pas être créés avec la même adresse email.

**EM9** - Seul un administrateur peut créer ou modifier un concert.

**EM10** - Toute commande doit être associée à un utilisateur, à un concert, à une date et à un statut.

## 7. Exigences non fonctionnelles

**ENF1** - Les principales actions utilisateur doivent être accessibles sans navigation excessive : consulter un concert, ajouter au panier et payer.

**ENF2** - L’affichage d’une page standard ne doit pas dépasser 2 secondes dans des conditions normales d’utilisation.

**ENF3** - Les mots de passe ne doivent pas être stockés en clair.

**ENF4** - Le système doit gérer proprement les saisies invalides sans planter.

**ENF5** - Le projet doit intégrer un outil d’analyse statique et viser un niveau de qualité défini par l’équipe.

**ENF6** - Les fonctionnalités principales doivent être suffisamment isolées pour permettre l’écriture de tests automatisés.

**ENF7** - Le projet doit être versionné et intégrer un pipeline d’exécution automatique des tests.

## 8. Données principales du système

### 8.1 Concert

Identifiant, titre, artiste ou groupe, description, date et heure, lieu, statut.

### 8.2 Catégorie de place

Identifiant, nom, prix, stock initial, stock restant, concert associé.

### 8.3 Utilisateur

Identifiant, nom, prénom, email, mot de passe, rôle.

### 8.4 Panier

Identifiant, utilisateur, lignes de panier, total.

### 8.5 Commande

Identifiant, utilisateur, date, montant total, statut.

### 8.6 Paiement

Identifiant, commande, date, montant, résultat.

## 9. Règles de gestion

**RG1** - Un concert est réservable uniquement si sa date n’est pas passée, si son statut est « ouvert à la vente » et si au moins une catégorie possède du stock.

**RG2** - Une catégorie est réservable uniquement si le stock restant est supérieur ou égal à la quantité demandée.

**RG3** - La quantité saisie doit être un entier compris entre 1 et 6.

**RG4** - Si le paiement échoue, la commande reste non validée.

**RG5** - Si le paiement réussit, la commande passe à l’état « payée » et le stock est décrémenté.

**RG6** - Un utilisateur non connecté ne peut pas accéder au paiement.

**RG7** - Un administrateur peut annuler un concert ; après annulation, aucune nouvelle réservation n’est possible.

**RG8** - Un utilisateur peut consulter uniquement ses propres commandes.

## 10. Parcours utilisateurs attendus

### 10.1 Parcours nominal

Le visiteur consulte la liste des concerts puis ouvre la fiche détaillée d’un concert.

Il se connecte, choisit une catégorie et une quantité valide puis ajoute les billets à son panier.

Il valide son panier, le paiement simulé est accepté, une confirmation est affichée et la commande apparaît dans son historique.

### 10.2 Parcours d’erreur

Tentative de réservation avec une quantité égale à 0 : le système doit refuser la demande avec un message explicite.

Tentative de réservation au-delà du stock disponible : le système doit refuser l’ajout au panier.

Tentative de paiement sans authentification : le système doit bloquer l’accès et demander la connexion.

Paiement refusé : la commande ne doit pas être validée.

## 11. États métier intéressants

Vous devrez identifier et modéliser les principaux états du système afin de justifier certains cas de test.

### 11.1 État d’un concert

Brouillon, ouvert à la vente, complet, annulé, terminé.

### 11.2 État d’une commande

Panier, en attente de paiement, payée, refusée, annulée.

## 12. Attendus techniques minimales

- Une application exécutable.
- Un jeu de données minimal.
- Des tests automatisés.
- Démarche qualité.
- Les technologies sont libres, sous réserve qu’elles soient cohérentes avec vos capacités à développer, tester et présenter le projet proprement.

## 13. Attendus en validation et qualité

### 13.1 Exigences et traçabilité

Vous devrez produire une liste d’exigences fonctionnelles et non fonctionnelles, des user stories, des critères d’acceptation et une matrice de traçabilité Exigence -> Test(s).

### 13.2 Conception des tests

Vous devrez concevoir et justifier des classes d’équivalence, des tests aux limites, au moins une table de décision et au moins un cas de test basé sur un diagramme d’états ou un cycle de vie métier.

### 13.3 Tests automatisés

Vous devrez mettre en place des tests unitaires, quelques tests d’intégration et au moins un scénario fonctionnel automatisé ou semi-automatisé.

### 13.4 Qualité du code

Vous devrez utiliser un outil d’analyse statique, mesurer la couverture, identifier quelques problèmes détectés et corriger au moins une partie de ces problèmes.

### 13.5 Intégration continue

Le dépôt devra exécuter automatiquement le build, les tests et, si possible, l’analyse qualité.

## 14. Consigne de synthèse

Vous devez concevoir, développer et valider une application web de billetterie pour concerts. Le projet doit répondre à un besoin métier explicite, être accompagné d’exigences claires et testables, intégrer une démarche de validation complète et être démontré lors d’une soutenance.

L’objectif n’est pas seulement de faire une application qui fonctionne, mais de prouver sa qualité par des exigences, des tests, de la traçabilité, de l’analyse statique et une intégration continue.

**Remarque :** vous êtes libres dans vos choix techniques, mais vous serez évalués sur la cohérence de vos décisions, la qualité de votre réalisation, la pertinence de vos tests et votre capacité à justifier votre démarche.