# Criteres d'acceptation

## CA1 - Liste des concerts ouverts

- Etant donne des concerts avec plusieurs statuts, quand un visiteur ouvre la liste, alors seuls les concerts ouverts a la vente et reservables sont affiches.
- Exigences : EF1, RG1.

## CA2 - Detail concert

- Etant donne un concert existant, quand un visiteur ouvre sa fiche, alors le titre, l'artiste, la date, le lieu, les categories, les prix et le stock restant sont visibles.
- Exigences : EF2.

## CA3 - Creation de compte

- Etant donne un email non utilise, quand un visiteur cree un compte avec un mot de passe valide, alors le compte est cree.
- Etant donne un email deja utilise, quand un visiteur tente de creer un compte, alors la creation est refusee avec un message explicite.
- Etant donne un compte cree, quand l'inscription reussit, alors l'utilisateur est connecte et redirige vers `Mon espace`.
- Exigences : EF3, EM8, ENF3, ENF4.

## CA3 bis - Authentification

- Etant donne un utilisateur enregistre, quand il saisit des identifiants valides, alors il est connecte.
- Etant donne un utilisateur enregistre, quand il saisit un mot de passe invalide, alors la connexion est refusee avec un message explicite en francais.
- Etant donne un utilisateur connecte, quand il utilise la deconnexion, alors sa session est fermee par une requete POST.
- Etant donne un visiteur non connecte, quand il accede a `Mon espace`, alors il est redirige vers la connexion.
- Exigences : EF4, ENF4.

## CA4 - Ajout au panier

- Etant donne un utilisateur connecte et une categorie avec assez de stock, quand il ajoute une quantite entre 1 et 6, alors la ligne est ajoutee au panier.
- Etant donne une quantite hors limites ou un stock insuffisant, quand l'utilisateur ajoute au panier, alors l'ajout est refuse.
- Exigences : EF5, EF6, EM1, EM2, EM3, RG2, RG3.

## CA5 - Paiement accepte

- Etant donne un panier valide, quand le paiement simule est accepte, alors une commande payee est creee, une confirmation est affichee et le stock est decremente.
- Exigences : EF7, EF8, EF12, EM6, EM7, EM10, RG5.

## CA6 - Paiement refuse

- Etant donne un panier valide, quand le paiement simule est refuse, alors aucune commande payee n'est creee, un message explicite est affiche et le stock ne change pas.
- Exigences : EF7, EF9, EM6, RG4.

## CA7 - Acces au paiement

- Etant donne un utilisateur non connecte, quand il tente d'acceder au paiement, alors l'acces est bloque et une connexion est demandee.
- Exigences : RG6.

## CA8 - Historique de commandes

- Etant donne deux utilisateurs avec des commandes distinctes, quand l'un consulte son historique, alors seules ses propres commandes sont visibles.
- Etant donne une commande payee, quand son proprietaire ouvre le detail, alors la date, le statut, le total, le concert, la categorie, la quantite et le prix paye sont visibles.
- Etant donne une commande payee d'un autre utilisateur, quand un client tente d'ouvrir son detail, alors l'acces est refuse.
- Etant donne un visiteur non connecte, quand il tente d'ouvrir l'historique ou un detail de commande, alors une connexion est demandee.
- Etant donne une commande refusee, quand le client consulte `Mes commandes`, alors elle n'apparait pas dans l'historique des achats payes.
- Exigences : EF10, RG8.

## CA9 - Administration concerts

- Etant donne un administrateur authentifie, quand il cree, modifie, suspend ou annule un concert, alors le changement est applique.
- Etant donne un utilisateur non administrateur, quand il tente de gerer un concert, alors l'acces est refuse.
- Exigences : EF11, EM9, RG7.
