# SESSION_NOTES.md

Notes de session pour les agents IA travaillant sur `invoice-cms`.

## Session du 2026-05-11

### Demande

- Ajouter `AGENTS.md`, `MEMORY.md`, `ARCHITECTURE.md` et `SESSION_NOTES.md` afin de rendre le projet plus compatible avec le travail d'agents IA.

### Travail réalisé

- Création de `AGENTS.md` avec consignes de contribution, commandes utiles, conventions backend/frontend et attentes de PR.
- Création de `MEMORY.md` avec contexte durable, invariants, dette technique et bonnes pratiques pour futures sessions.
- Création de `ARCHITECTURE.md` avec vue d'ensemble backend Django, frontend Vue, routage, modèles métier et flux clés.
- Création de `SESSION_NOTES.md` pour tracer la demande et l'état de la session.

### État connu

- Les changements sont documentaires uniquement.
- Aucun comportement applicatif n'a été modifié.
- Les contrôles à exécuter avant livraison sont listés dans `AGENTS.md` et `ARCHITECTURE.md`.

### À faire lors de futures sessions

- Mettre à jour `MEMORY.md` lorsqu'une convention durable ou une contrainte importante change.
- Mettre à jour `ARCHITECTURE.md` lors d'un changement structurel backend, frontend, API ou infrastructure.
- Ajouter une nouvelle entrée datée dans ce fichier à la fin de chaque session significative.

## Session du 2026-05-12

### Demande

- Mettre à niveau les dépendances backend pour Python 3.14 et Django 6.

### Travail réalisé

- Mise à jour de `requirements.txt` et `requirements-dev.txt` vers des dépendances backend directes compatibles Python 3.14 / Django 6.0.
- Mise à jour des commentaires de settings Django et remplacement de `STATICFILES_STORAGE` par la configuration `STORAGES` compatible Django 6.
- Mise à jour du workflow GitHub Actions pour installer Python 3.14 avec `actions/setup-python@v5`.
- Mise à jour de la documentation durable (`README.md`, `AGENTS.md`, `MEMORY.md`) pour refléter la cible Python 3.14 / Django 6.0.

### État connu

- La résolution/install pip n'a pas pu être validée dans l'environnement courant car l'accès PyPI via proxy renvoie `403 Forbidden`.
- `djoser` a été remplacé par des endpoints DRF internes afin d’éviter de conserver une dépendance tierce sans support Django 6 explicite.
- Upgrader les dépendances frontend vers les dernières updates.

### Travail réalisé

- Synchronisation des versions minimales déclarées dans `frontend/package.json` avec les versions déjà résolues dans `frontend/package-lock.json` pour Vue, Vue Router, Vuex, Sass et Sass Loader.
- Maintien du verrou npm cohérent avec les versions déclarées afin de préserver `npm ci`.

### État connu

- Le registre npm était inaccessible depuis l'environnement shell (`403 Forbidden` via le proxy), ce qui a empêché une régénération complète du lockfile vers les dernières versions publiées en ligne.
- Le build frontend passe avec les dépendances actuellement installées/verrouillées, avec uniquement les avertissements de taille de bundle et de données Browserslist déjà présents.
