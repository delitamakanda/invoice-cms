# AGENTS.md

Instructions pour les agents IA qui travaillent sur ce dépôt.

## Portée

Ces consignes s'appliquent à tout le dépôt `invoice-cms`.

## Vue rapide du projet

- Application de génération et de gestion de factures.
- Backend : Python 3.14 + Django 6.0 + Django REST Framework, projet `invoices/`, apps métier dans `apps/`.
- Frontend : Vue 3 + Vue CLI + Ant Design Vue dans `frontend/`.
- Authentification : endpoints DRF internes compatibles token DRF côté API, token stocké dans `localStorage` côté frontend.
- PDF : templates Django dans `templates/`, génération via `pdfkit`/`wkhtmltopdf`.
- Dev local : base SQLite par défaut ; production : configuration PostgreSQL Azure dans `invoices/settings_prod.py`.

## Commandes utiles

### Backend

```bash
python3.14 -m venv invoices_env
source invoices_env/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Contrôles recommandés avant de livrer une modification backend :

```bash
python3 manage.py check
python3 manage.py test
```

### Frontend

```bash
cd frontend
npm install
npm run serve
npm run build
```

Contrôle recommandé avant de livrer une modification frontend :

```bash
cd frontend && npm run build
```

## Conventions de modification

- Préserver la séparation backend/frontend :
  - API, modèles, serializers, permissions et routes DRF dans `apps/*` et `invoices/`.
  - UI, routes Vue, store Vuex, helpers et assets dans `frontend/src/`.
- Ajouter une migration Django pour tout changement de modèle.
- Ne pas modifier les migrations existantes déjà versionnées, sauf demande explicite.
- Protéger les données utilisateur : filtrer les querysets par `request.user` pour les ressources privées.
- Garder les endpoints API sous le préfixe `/api/v1/`.
- Les vues PDF doivent rester compatibles avec `pdfkit` et les templates Django.
- Ne pas committer de secrets, tokens, dumps de base de données, fichiers `.env`, `db.sqlite3`, `media/`, `staticfiles/`, `node_modules/` ou builds temporaires.

## Style

### Python/Django

- Suivre le style Django existant du dépôt.
- Garder les imports simples ; ne pas entourer les imports avec des blocs `try/except`.
- Utiliser des serializers DRF pour valider les entrées API.
- Utiliser `get_object_or_404(..., created_by=request.user)` ou une restriction équivalente pour les objets détenus par un utilisateur.

### JavaScript/Vue

- Suivre le style Vue existant : composants `.vue`, Vue Router, Vuex namespaced modules.
- Utiliser l'alias `@/` pour les imports frontend lorsque c'est cohérent avec le code existant.
- Garder les appels authentifiés via `frontend/src/utils/auth.js` lorsque l'API exige le token.

## Documentation IA

- `ARCHITECTURE.md` décrit l'organisation technique et les flux principaux.
- `MEMORY.md` contient la mémoire durable du projet : décisions, invariants, risques connus.
- `SESSION_NOTES.md` contient les notes de travail courantes et doit être mis à jour à la fin d'une session significative.
- Mettre ces fichiers à jour lorsque vous découvrez une information durable ou que vous changez une convention.

## Pull requests

Dans le résumé de PR, indiquer :

- ce qui a changé ;
- les fichiers ou zones principales ;
- les tests/contrôles exécutés ;
- les limites connues, notamment si un contrôle n'a pas pu être exécuté pour une raison d'environnement.
