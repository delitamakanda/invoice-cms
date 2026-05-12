# MEMORY.md

Mémoire durable du projet `invoice-cms` pour les agents IA.

## Objectif produit

`invoice-cms` est un CMS léger de facturation. Il permet à un utilisateur authentifié de gérer son équipe/entreprise, ses clients, ses factures, leurs lignes, l'émission de PDF et l'envoi de rappels par email.

## Stack actuelle

- Backend : Python 3.14, Django 6.0, Django REST Framework, endpoints auth internes, authentification par token DRF.
- Frontend : Vue 3, Vue Router 4, Vuex 4, Ant Design Vue 2, Vue CLI 5.
- Base locale : SQLite via `invoices/settings.py`.
- Base production : PostgreSQL Azure via `invoices/settings_prod.py`.
- Assets statiques production : WhiteNoise.
- PDFs : `pdfkit` côté Django, templates `templates/pdf.html` et `templates/pdf_creditnote.html`.
- Observabilité frontend : Datadog RUM initialisé dans `frontend/src/main.js` à partir de variables `VUE_APP_DATADOG_*`.

## Domain model durable

- `Team` représente l'entreprise de l'utilisateur : nom, numéro d'organisation, email, adresse, compte bancaire, prochain numéro de facture.
- `Client` représente un client appartenant à un utilisateur.
- `Invoice` représente une facture ou une note de crédit. Elle snapshot les informations client au moment de la création et appartient à un `Team`, un `Client`, `created_by` et `modified_by`.
- `Item` représente une ligne de facture attachée à une facture.
- Le numéro de facture est dérivé de `Team.first_invoice_number` puis incrémenté à la création d'une facture.

## Invariants importants

- Les ressources métier privées doivent être limitées à l'utilisateur authentifié.
- Les endpoints applicatifs restent sous `/api/v1/`.
- Le frontend suppose que l'API est servie depuis la même origine (`endpoint = '/'` et `axios.defaults.baseURL = '/'`).
- Le token d'authentification est stocké dans `localStorage` et envoyé sous la forme `Authorization: Token <token>`.
- Les PDFs dépendent de `wkhtmltopdf` disponible dans l'environnement d'exécution.
- Les montants utilisent des `DecimalField`; éviter les calculs flottants côté backend.

## Risques connus / dette technique

- `SECRET_KEY` de développement est actuellement codée en dur dans `invoices/settings.py`; ne pas la réutiliser en production.
- `ALLOWED_HOSTS = ['*']` et `DEBUG = True` dans les settings locaux sont seulement adaptés au développement.
- `settings_prod.py` lit plusieurs variables d'environnement avec `os.environ[...]`; l'application échoue au démarrage si elles sont absentes.
- La création d'une facture incrémente `Team.first_invoice_number` sans verrou transactionnel explicite ; attention aux créations concurrentes.
- Le frontend n'a pas de script de test dédié dans `frontend/package.json`; utiliser au minimum `npm run build` pour vérifier l'intégration.

## Bonnes pratiques pour futures sessions IA

- Lire `AGENTS.md` puis `ARCHITECTURE.md` avant toute modification substantielle.
- Vérifier `git status --short` avant de modifier pour ne pas écraser un travail en cours.
- Pour un changement backend : exécuter `python3 manage.py check` et, si possible, `python3 manage.py test`.
- Pour un changement frontend : exécuter `cd frontend && npm run build` si les dépendances sont installées.
- Mettre à jour cette mémoire si une décision durable, une convention ou une contrainte importante change.
