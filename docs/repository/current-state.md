# Etat courant du depot

Derniere mise a jour : 2026-04-25

## Synthese

Le depot contient actuellement la baseline de tooling et de documentation du projet de billetterie de concerts. Le projet Django n'est pas encore initialise : il n'existe pas de `manage.py`, pas de module de configuration Django, pas d'application Django, pas de migrations et pas de tests applicatifs versionnes.

Le cahier des charges officiel est conserve dans `docs/brief/projet-validation-logiciel-e4a-2026.md`.

## Fichiers suivis avant cette baseline

- `.gitignore`
- `requirements.txt`
- `requirements-dev.txt`
- `docs/brief/projet-validation-logiciel-e4a-2026.md`

## Structure ajoutee

- `docs/repository/` : documentation du depot, des choix techniques, de l'architecture cible, du frontend, des tests et de la qualite.
- `docs/validation/` : exigences, user stories, criteres d'acceptation, conception de tests et matrice de tracabilite.

## Environnement local observe

- Branche locale : `main`.
- Branche distante : `origin/main`.
- Dernier commit observe avant changement : `002ead7 chore: initial project tooling setup`.
- Remote Git : `https://github.com/Axel-al/billeterie-concerts.git`.
- Fichier `AGENTS.md` demande par le prompt : absent du depot.
- Fichier local lu a la place car present : `AGENT.md`.
- `AGENT.md` et `docs/prompts/` sont ignores via `.git/info/exclude`.
- `.python-version` et `.vscode/` sont ignores via `.gitignore`.

## Decisions de scope appliquees

- Aucun projet Django n'a ete initialise dans cette etape.
- Aucun fichier de `docs/prompts/` n'a ete lu.
- `.gitignore` n'a pas ete modifie car les exclusions utiles sont deja presentes.
- La matrice de tracabilite indique explicitement que les exigences fonctionnelles, metier et regles de gestion ne sont pas encore couvertes par du code ou des tests.

## Fichiers crees ou modifies dans cette etape

- `docs/repository/README.md`
- `docs/repository/current-state.md`
- `docs/repository/architecture.md`
- `docs/repository/apps.md`
- `docs/repository/decisions.md`
- `docs/repository/frontend.md`
- `docs/repository/testing.md`
- `docs/repository/quality-ci.md`
- `docs/validation/exigences.md`
- `docs/validation/user_stories.md`
- `docs/validation/criteres_acceptation.md`
- `docs/validation/plan_de_test.md`
- `docs/validation/classes_equivalence.md`
- `docs/validation/valeurs_limites.md`
- `docs/validation/table_decision.md`
- `docs/validation/diagrammes_etats.md`
- `docs/validation/matrice_tracabilite.md`
- `docs/validation/rapport_qualite.md`

## Commandes lancees

- `cat AGENTS.md`
- `rg --files -g 'AGENTS.md' -g '!**/.venv/**' -g '!**/node_modules/**'`
- `git status --short --branch`
- `git log --oneline --decorate -5`
- `rg --files -g '!**/.venv/**' -g '!**/node_modules/**'`
- `git remote -v`
- `ls -la`
- `git ls-files`
- `sed -n '1,240p' requirements.txt`
- `sed -n '1,260p' requirements-dev.txt`
- `sed -n '1,260p' docs/brief/projet-validation-logiciel-e4a-2026.md`
- `sed -n '1,260p' AGENT.md`
- `sed -n '1,240p' .gitignore`
- `find docs -maxdepth 3 -type d -print`
- `find docs -maxdepth 3 -type f -print`
- `git check-ignore -v AGENT.md docs/prompts/prompt-0.md .python-version .vscode/settings.json`
- `mkdir -p docs/repository docs/validation`
- `git add -N docs/repository docs/validation`
- `test -f docs/repository/README.md && test -f docs/repository/current-state.md && test -f docs/repository/architecture.md && test -f docs/repository/apps.md && test -f docs/repository/decisions.md && test -f docs/repository/frontend.md && test -f docs/repository/testing.md && test -f docs/repository/quality-ci.md && test -f docs/validation/exigences.md && test -f docs/validation/user_stories.md && test -f docs/validation/criteres_acceptation.md && test -f docs/validation/plan_de_test.md && test -f docs/validation/classes_equivalence.md && test -f docs/validation/valeurs_limites.md && test -f docs/validation/table_decision.md && test -f docs/validation/diagrammes_etats.md && test -f docs/validation/matrice_tracabilite.md && test -f docs/validation/rapport_qualite.md`
- `git diff --check`
- `git diff --stat`
- `git diff --name-only`
- `sed -n '1,260p' docs/repository/current-state.md`

## Checks lances

- Presence des 18 fichiers documentaires attendus : OK.
- `git diff --check` : OK, aucune erreur de whitespace detectee.
- Revue Git des fichiers ajoutes : OK, 18 fichiers documentaires ajoutes.
- Les tests Python, Django, Playwright et couverture ne sont pas lances car cette etape est strictement documentaire et il n'existe pas encore de code applicatif ni de projet Django initialise.

## Statut Git

Statut observe avant staging final et commit :

```text
## main...origin/main
 A docs/repository/README.md
 A docs/repository/apps.md
 A docs/repository/architecture.md
 A docs/repository/current-state.md
 A docs/repository/decisions.md
 A docs/repository/frontend.md
 A docs/repository/quality-ci.md
 A docs/repository/testing.md
 A docs/validation/classes_equivalence.md
 A docs/validation/criteres_acceptation.md
 A docs/validation/diagrammes_etats.md
 A docs/validation/exigences.md
 A docs/validation/matrice_tracabilite.md
 A docs/validation/plan_de_test.md
 A docs/validation/rapport_qualite.md
 A docs/validation/table_decision.md
 A docs/validation/user_stories.md
 A docs/validation/valeurs_limites.md
```

Commit prevu : `docs: add project documentation baseline`.

Etat attendu apres commit et push : branche `main` propre et synchronisee avec `origin/main`.

## Prochaine etape recommandee

Initialiser le projet Django seulement dans l'etape dediee, puis creer les premiers modules et tests en reliant chaque changement aux IDs officiels du cahier des charges dans `docs/validation/matrice_tracabilite.md`.
