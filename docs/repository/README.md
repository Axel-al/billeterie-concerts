# Documentation du dépôt

Ce dossier décrit l'état technique du dépôt, les choix déjà actés et la manière dont le projet doit évoluer sans confondre le cahier des charges avec un backlog d'implémentation.

Document de référence officiel :

- [Cahier des charges](../brief/projet-validation-logiciel-e4a-2026.md)

Documents du dossier :

- [current-state.md](current-state.md) : état réel du dépôt et dernières opérations.
- [architecture.md](architecture.md) : architecture cible retenue à ce stade.
- [apps.md](apps.md) : applications Django prévues, sans initialisation pour l'instant.
- [data-model.md](data-model.md) : modèle de données Django courant.
- [domain-rules.md](domain-rules.md) : règles métier implémentées au niveau domaine/service.
- [decisions.md](decisions.md) : décisions techniques et qualité déjà prises.
- [frontend.md](frontend.md) : principes d'interface et technologies frontend prévues.
- [testing.md](testing.md) : couches de tests prévues.
- [quality-ci.md](quality-ci.md) : analyse statique, couverture, CI et SonarQube.

État important : le dépôt contient une application Django exécutable et un noyau domaine testé. Les parcours web métier restent incomplets tant que les vues de concerts, panier, paiement et historique ne sont pas implémentées.
