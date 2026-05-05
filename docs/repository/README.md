# Documentation du depot

Ce dossier decrit l'etat technique du depot, les choix deja actés et la maniere dont le projet doit evoluer sans confondre le cahier des charges avec un backlog d'implementation.

Document de reference officiel :

- [Cahier des charges](../brief/projet-validation-logiciel-e4a-2026.md)

Documents du dossier :

- [current-state.md](current-state.md) : etat reel du depot et dernieres operations.
- [architecture.md](architecture.md) : architecture cible retenue a ce stade.
- [apps.md](apps.md) : applications Django prevues, sans initialisation pour l'instant.
- [data-model.md](data-model.md) : modele de donnees Django courant.
- [domain-rules.md](domain-rules.md) : regles metier implementees au niveau domaine/service.
- [decisions.md](decisions.md) : decisions techniques et qualite deja prises.
- [frontend.md](frontend.md) : principes d'interface et technologies frontend prevues.
- [testing.md](testing.md) : couches de tests prevues.
- [quality-ci.md](quality-ci.md) : analyse statique, couverture, CI et SonarQube.

Etat important : le depot contient une application Django executable et un noyau domaine teste. Les parcours web metier restent incomplets tant que les vues de concerts, panier, paiement et historique ne sont pas implementees.
