# Frontend

## État actuel

Le frontend applicatif minimal est initialise avec Django templates.

- `templates/base.html` fournit le layout HTML, la navigation minimale et Bootstrap via CDN.
- `templates/pages/home.html` fournit une page d'accueil française avec un accès direct au catalogue.
- `templates/concerts/concert_list.html` affiche les concerts ouverts, futurs et disponibles.
- `templates/concerts/concert_detail.html` affiche les informations du concert, les catégories, prix, stocks, l'état de réservation et le formulaire d'ajout au panier pour les utilisateurs connectés.
- `templates/cart/detail.html` affiche le panier actif, les lignes, les sous-totaux et le total.
- `templates/cart/checkout.html` affiche le récapitulatif de validation avant paiement.
- `templates/payments/payment_form.html` affiche le formulaire de paiement simulé.
- `templates/payments/confirmation.html` affiche une commande payée avec les prix snapshots.
- `templates/payments/refused.html` affiche le refus explicite et permet de retenter le paiement.
- `templates/orders/list.html` affiche l'historique des commandes payées du client connecté.
- `templates/orders/detail.html` affiche le détail d'une commande payée du client connecté avec les prix snapshots.
- `templates/concerts/admin_sales_overview.html` affiche une synthèse admin des ventes par concert et les actions d'annulation/clôture.
- `templates/accounts/signup.html` fournit le formulaire d'inscription en français.
- `templates/accounts/login.html` fournit le formulaire de connexion en français.
- `templates/accounts/personal_area.html` fournit la page protégée `Mon espace` avec un accès à `Mes commandes`.
- La route `/` affiche la page d'accueil via `TemplateView`.
- Les routes `/concerts/` et `/concerts/<id>/` fournissent le catalogue et les fiches publiques.
- La navigation fournit un lien `Concerts`, puis affiche `Inscription` et `Connexion` aux visiteurs ou `Panier`, `Mes commandes`, `Mon espace` et un bouton POST `Déconnexion` aux utilisateurs connectés.
- Le lien `Administration ventes` est affiché seulement aux utilisateurs disposant de `concerts.view_concert` et `orders.view_order`.
- Des attributs `data-testid` stables existent sur les contrôles du parcours nominal pour Playwright, sans modifier les libelles visibles en français.
- Les pages standards accueil, catalogue, fiche concert et historique authentifié servent de surfaces représentatives pour la mesure navigateur `ENF2`.

## Direction cible

Le frontend cible repose sur :

- Django templates ;
- Bootstrap via CDN ;
- HTML sémantique ;
- JavaScript léger seulement lorsque cela améliore clairement l'ergonomie ;
- éventuellement HTMX via CDN pour des interactions simples, si justifié.

## Principes d'interface

- Rendre visibles les actions principales : consulter un concert, ajouter au panier, payer.
- Afficher clairement les erreurs de saisie, de stock, d'authentification et de paiement.
- Éviter une navigation excessive pour les parcours principaux.
- Garder les pages lisibles sur mobile et desktop.
- Afficher les prix, quantités, stocks et statuts de façon explicite avant validation.

## Écrans disponibles

- Liste des concerts ouverts à la vente.
- Détail d'un concert avec catégories, prix et stock restant.
- Création de compte et connexion.
- Espace personnel protégé.
- Historique des commandes.
- Suivi admin des ventes par concert avec annulation et clôture.

## Écrans cibles restants

- Parcours d'erreur Playwright optionnels : paiement refusé, quantité invalide ou redirection anonyme. Ces cas restent couverts par les tests d'intégration Django.

## Couverture fonctionnelle

Le catalogue et les fiches couvrent `EF1` et `EF2`. La navigation directe depuis l'accueil et entre liste et détail apporte une couverture partielle de `ENF1`.

Le lien `Se connecter pour réserver` est affiché seulement au visiteur lorsqu'un concert est réservable et conserve la fiche dans le paramètre `next`. Pour un utilisateur connecté, la fiche réservable expose le formulaire catégorie/quantité permettant d'ajouter au panier.

Les concerts non réservables affichent un motif explicite en français et aucune action de réservation. Les brouillons ne sont pas accessibles publiquement.

Le parcours panier/paiement couvre maintenant l'ajout au panier, le total, le checkout, la confirmation et le refus explicite. Les pages de résultat de paiement sont filtrées par utilisateur connecté.

`EF10` et `RG8` sont couverts par les pages `Mes commandes` et détail de commande, limitées aux commandes payées du client connecté. Les commandes refusées restent tracées comme non finales et sont exclues de l'historique des achats payés.

`EF11`, `EM9` et `RG7` sont couverts par une page d'administration Django template : synthèse des ventes, annulation et clôture. Cette page est une fonctionnalité privilégiée et ne remplace pas l'historique normal des commandes utilisateur.

Le scénario `e2e/test_nominal_booking_flow.py` couvre le chemin utilisateur principal en navigateur : liste des concerts, fiche réservable, connexion, choix de catégorie, quantité valide, panier, validation, paiement accepté, confirmation et historique.

Le test `e2e/test_page_performance.py` couvre `ENF2` en Chromium sur des pages
standards. Pendant la mesure, les URLs jsDelivr de Bootstrap sont interceptées
et servies depuis des fixtures locales contenant les vrais fichiers Bootstrap
5.3.3, vérifiées par les mêmes empreintes SRI que le template. Cela évite la
latence tierce pendant la mesure LCP tout en conservant un rendu proche de
l'usage normal.

## Contraintes

Aucune application frontend séparée n'est prévue. Tout changement de direction devra être justifié dans `docs/repository/decisions.md`.
