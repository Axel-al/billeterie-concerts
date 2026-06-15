# Frontend

## Technologie

L'interface utilise :

- templates Django ;
- HTML sémantique ;
- Bootstrap 5.3.3 via jsDelivr ;
- aucun JavaScript applicatif obligatoire.

Les ressources Bootstrap possèdent des empreintes SRI et
`crossorigin="anonymous"`.

## Écrans

- accueil ;
- liste et détail des concerts ;
- inscription, connexion et espace personnel ;
- panier et validation ;
- paiement, confirmation et refus ;
- historique et détail des commandes ;
- synthèse administrateur des ventes ;
- administration Django francisée.

## Navigation

Le visiteur accède directement au catalogue, à l'inscription et à la
connexion. Le client connecté accède au panier, à ses commandes et à son
espace. Les liens administrateur apparaissent uniquement avec les permissions
requises.

Le lien de connexion depuis une fiche conserve l'URL dans `next` afin de
revenir au concert après authentification.

## Validation française

Les formulaires de réservation et paiement portent `novalidate`. La validation
de référence est ainsi exécutée par Django, qui affiche les messages français.

Les attributs HTML utiles sont conservés :

- `required` ;
- `type="number"`, `min="1"` et `max="6"` pour la quantité ;
- `type="text"`, `maxlength="32"` et `inputmode="numeric"` pour la carte.

Cette combinaison préserve la sémantique, l'accessibilité et les claviers
adaptés sans dépendre des messages natifs du navigateur, qui varient selon sa
langue.

## États et erreurs

- Les concerts non réservables affichent un motif précis.
- Les erreurs de quantité, stock et paiement utilisent les messages Django.
- Un paiement refusé propose de réessayer.
- Les paniers et historiques vides possèdent un état explicite.
- Les commandes d'autres utilisateurs ne sont pas révélées.

## Sélecteurs de test

Les contrôles du parcours principal possèdent des attributs `data-testid`
stables pour Playwright. Ces identifiants techniques n'altèrent pas les
libellés visibles en français.

## Responsive

Bootstrap fournit une mise en page adaptée aux écrans mobiles et desktop. La
mesure `ENF2` utilise un viewport desktop 1366 × 768 ; elle ne constitue pas
une campagne multi-appareils complète.
