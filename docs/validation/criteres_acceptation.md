# Critères d'acceptation

## CA1 - Liste des concerts ouverts

- Étant donné des concerts avec plusieurs statuts, quand un visiteur ouvre la liste, alors seuls les concerts ouverts à la vente et réservables sont affichés.
- Exigences : EF1, RG1.

## CA2 - Détail concert

- Étant donné un concert existant, quand un visiteur ouvre sa fiche, alors le titre, l'artiste, la date, le lieu, les catégories, les prix et le stock restant sont visibles.
- Exigences : EF2.

## CA3 - Création de compte

- Étant donné un e-mail non utilisé, quand un visiteur crée un compte avec un mot de passe valide, alors le compte est créé.
- Étant donné un e-mail déjà utilisé, quand un visiteur tente de créer un compte, alors la création est refusée avec un message explicite.
- Étant donné un compte créé, quand l'inscription réussit, alors l'utilisateur est connecté et redirigé vers `Mon espace`.
- Exigences : EF3, EM8, ENF3, ENF4.

## CA3 bis - Authentification

- Étant donné un utilisateur enregistré, quand il saisit des identifiants valides, alors il est connecté.
- Étant donné un utilisateur enregistré, quand il saisit un mot de passe invalide, alors la connexion est refusée avec un message explicite en français.
- Étant donné un utilisateur connecté, quand il utilise la déconnexion, alors sa session est fermée par une requête POST.
- Étant donné un visiteur non connecté, quand il accède à `Mon espace`, alors il est redirigé vers la connexion.
- Exigences : EF4, ENF4.

## CA4 - Ajout au panier

- Étant donné un utilisateur connecté et une catégorie avec assez de stock, quand il ajoute une quantité entre 1 et 6, alors la ligne est ajoutée au panier.
- Étant donné une quantité hors limites ou un stock insuffisant, quand l'utilisateur ajoute au panier, alors l'ajout est refusé.
- Les attributs HTML `required`, `min="1"`, `max="6"` et `type="number"` restent présents pour la sémantique et l'aide à la saisie. Le formulaire utilise `novalidate` afin que la validation de référence soit exécutée côté Django et que le message soit affiché en français.
- Exigences : EF5, EF6, EM1, EM2, EM3, RG2, RG3.

## CA5 - Paiement accepté

- Étant donné un panier valide, quand le paiement simulé est accepté, alors une commande payée est créée, une confirmation est affichée et le stock est décrémenté.
- Exigences : EF7, EF8, EF12, EM6, EM7, EM10, RG5.

## CA6 - Paiement refusé

- Étant donné un panier valide, quand le paiement simulé est refusé, alors aucune commande payée n'est créée, un message explicite est affiché et le stock ne change pas.
- Étant donné un numéro de carte vide ou trop long, quand le formulaire est soumis, alors Django refuse la saisie avec un message français. Les attributs HTML `required`, `maxlength`, `type` et `inputmode` restent présents.
- Exigences : EF7, EF9, EM6, RG4.

## CA7 - Accès au paiement

- Étant donné un utilisateur non connecté, quand il tente d'accéder au paiement, alors l'accès est bloqué et une connexion est demandée.
- Exigences : RG6.

## CA8 - Historique de commandes

- Étant donné deux utilisateurs avec des commandes distinctes, quand l'un consulte son historique, alors seules ses propres commandes sont visibles.
- Étant donné une commande payée, quand son propriétaire ouvre le détail, alors la date, le statut, le total, le concert, la catégorie, la quantité et le prix payé sont visibles.
- Étant donné une commande payée d'un autre utilisateur, quand un client tente d'ouvrir son détail, alors l'accès est refusé.
- Étant donné un visiteur non connecté, quand il tente d'ouvrir l'historique ou un détail de commande, alors une connexion est demandée.
- Étant donné une commande refusée, quand le client consulte `Mes commandes`, alors elle n'apparaît pas dans l'historique des achats payés.
- Exigences : EF10, RG8.

## CA9 - Administration concerts

- Étant donné un administrateur authentifié, quand il crée, modifie, suspend ou annule un concert, alors le changement est appliqué.
- Étant donné un utilisateur avec `concerts.change_concert`, quand il annule un concert, alors le statut passe à `cancelled` et aucune nouvelle réservation n'est possible.
- Étant donné un utilisateur avec `concerts.change_concert`, quand il clôture les ventes d'un concert, alors le statut passe à `closed` et aucune nouvelle réservation n'est possible.
- Étant donné un utilisateur avec `concerts.view_concert` et `orders.view_order`, quand il ouvre la synthèse des ventes, alors les commandes payées, billets vendus, revenus, stocks initiaux et stocks restants sont visibles par concert.
- Étant donné un visiteur non connecté, quand il tente d'accéder à une fonctionnalité admin, alors il est redirigé vers la connexion.
- Étant donné un utilisateur connecté sans permission admin, quand il tente de gérer un concert ou de consulter les ventes, alors l'accès est refusé avec `403`.
- Étant donné une commande payée existante, quand le concert est annulé ensuite, alors la commande reste visible par son propriétaire.
- Exigences : EF11, EM9, RG7.

Note : `RG8` reste traité dans `CA8` pour l'historique et le détail des commandes des utilisateurs standards. La synthèse admin des ventes est une fonctionnalité privilégiée distincte.

## CA10 - Performance page standard

- Étant donné Chromium installé par Playwright, `live_server`, des données de test contrôlées, une navigation locale loopback, un viewport desktop 1366x768, aucun throttling CPU ou réseau, un contexte navigateur froid et les ressources Bootstrap rejouées depuis des fixtures locales conformes aux empreintes SRI, quand l'accueil, le catalogue, une fiche concert ou l'historique authentifié affichent leur contenu principal, alors le Largest Contentful Paint mesuré par le navigateur reste inférieur ou égal à 2 000 ms.
- La durée de chargement issue de `PerformanceNavigationTiming` est collectée comme diagnostic, sans remplacer le seuil LCP.
- Cette acceptation prouve le rendu navigateur sous conditions CI contrôlées, pas la performance production sur tous les appareils, états CDN ou réseaux.
- Exigences : ENF2.
