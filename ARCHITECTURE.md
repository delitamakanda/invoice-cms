# ARCHITECTURE.md

Architecture technique de `invoice-cms`.

## Vue d'ensemble

Le dépôt contient une application full-stack de facturation :

```text
Navigateur Vue 3
  -> routes protégées par Vue Router/Vuex
  -> appels HTTP Axios avec token DRF
  -> Django / Django REST Framework
  -> apps métier client, team, invoice
  -> SQLite en local ou PostgreSQL en production
  -> templates Django + pdfkit pour les PDFs
```

Django sert aussi l'application frontend compilée via `TemplateView`, `django-webpack-loader` 3.x et les assets statiques générés par Vue CLI.

## Arborescence principale

```text
.
├── apps/
│   ├── client/      # Modèle, API et admin des clients
│   ├── invoice/     # Modèles, API, PDF et rappels email des factures
│   └── team/        # Modèle et API de l'entreprise/équipe utilisateur
├── frontend/
│   ├── public/      # Fichiers publics Vue CLI
│   └── src/         # Application Vue 3
├── invoices/        # Projet Django : settings, urls, ASGI/WSGI, sitemap
├── templates/       # Shell HTML, robots/ads et templates PDF
├── static/          # Fichiers statiques versionnés simples
├── manage.py
├── requirements.txt
└── requirements-dev.txt
```

## Backend Django

### Projet `invoices/`

- `invoices/settings.py` : configuration locale, SQLite, DRF, Djoser, CORS, templates et static files.
- `invoices/settings_prod.py` : surcharge production pour Azure/PostgreSQL, WhiteNoise et email SMTP.
- `invoices/urls.py` : point d'entrée URL principal.
- `invoices/sitemaps.py` : sitemap pour les vues statiques.

### Routage API

Les routes principales sont incluses sous `/api/v1/` :

- Djoser : inscription, connexion et endpoints utilisateur.
- Djoser token auth : obtention/suppression de token.
- `apps.client.urls` : endpoints clients.
- `apps.team.urls` : endpoints équipes.
- `apps.invoice.urls` : endpoints factures, génération PDF et rappels.

Les routes non-API incluent :

- `/admin/` pour Django Admin.
- `/ads.txt`, `/robots.txt`, `/sitemap.xml`.
- `/` pour le shell frontend `application.html`.

### Apps métier

#### `apps.team`

- Modèle `Team` : profil entreprise d'un utilisateur.
- Serializer `TeamSerializer`.
- ViewSet `TeamViewSet` filtré par utilisateur.

#### `apps.client`

- Modèle `Client` : fiche client appartenant à un utilisateur.
- Serializer `ClientSerializer`, avec factures imbriquées en lecture seule via `ClientInvoiceSerializer`.
- ViewSet `ClientViewSet` filtré par utilisateur.

#### `apps.invoice`

- Modèle `Invoice` : facture ou note de crédit, montants, statut, relations `Team`, `Client`, auteur/modificateur.
- Modèle `Item` : ligne de facture.
- Serializer `InvoiceSerializer` : création imbriquée des `items`.
- `InvoiceViewSet` : CRUD factures filtré par `created_by`.
- `generate_pdf` : rend un template PDF puis retourne un fichier PDF.
- `send_reminder` : envoie un email de relance avec PDF attaché.

## Frontend Vue

### Entrée et configuration

- `frontend/src/main.js` initialise Vue, Ant Design Vue, Vuex, Vue Router, i18n, Axios et Datadog RUM.
- `frontend/src/utils/constants.js` définit le titre et l'endpoint API courant.
- `frontend/src/utils/auth.js` crée une instance Axios qui ajoute le token DRF.

### Routage

`frontend/src/router/index.js` définit les pages principales :

- `/dashboard` : tableau de bord protégé.
- `/dashboard/my-account` et `/dashboard/my-account/edit-team` : compte et équipe.
- `/dashboard/clients*` : liste, détail, création et modification client.
- `/dashboard/invoices*` : liste, détail et création facture.
- `/sign-in`, `/sign-up`, `/about` : pages publiques.

Les routes avec `meta.requireLogin` redirigent vers `/sign-in` si `store.state.user.isLoggedIn` est faux.

### État utilisateur

`frontend/src/store/user/index.js` conserve :

- `user` : id, username, email ;
- `isLoggedIn` ;
- `token`.

`initStore` restaure ces informations depuis `localStorage`.

## Flux fonctionnels clés

### Authentification

1. Le frontend appelle les endpoints Djoser/token sous `/api/v1/`.
2. Le token reçu est stocké dans `localStorage`.
3. Les appels authentifiés passent par `authAxios`, qui ajoute `Authorization: Token <token>`.
4. Vue Router protège les pages dashboard à partir de l'état Vuex.

### Création d'une facture

1. L'utilisateur sélectionne ou renseigne un client et des lignes de facture côté Vue.
2. Le frontend envoie une facture avec `items` imbriqués à l'API.
3. `InvoiceSerializer.create()` crée la facture puis les `Item` associés.
4. `InvoiceViewSet.perform_create()` associe l'utilisateur, l'équipe, le compte bancaire et le numéro de facture.
5. `Team.first_invoice_number` est incrémenté.

### Génération PDF

1. Le frontend appelle l'endpoint PDF d'une facture authentifiée.
2. Le backend vérifie que la facture appartient à l'utilisateur.
3. Django rend `pdf.html` ou `pdf_creditnote.html`.
4. `pdfkit.from_string()` convertit le HTML en PDF.
5. La réponse est renvoyée en `application/pdf` avec téléchargement.

### Relance email

1. Le backend récupère la facture et l'équipe de l'utilisateur.
2. Il prépare un email texte + HTML.
3. Il génère le PDF de facture et l'attache.
4. Il envoie l'email via le backend email configuré.

## Configuration et variables d'environnement

### Développement local

Le settings local utilise SQLite et un email backend console. Les variables d'environnement ne sont pas strictement nécessaires sauf pour certains services frontend comme Datadog.

### Production

`invoices/settings_prod.py` attend notamment :

- `WEBSITE_HOSTNAME`
- `DEBUG`
- `DBHOST`, `DBNAME`, `DBUSER`, `DBPASS`
- `ADMIN_NAME`, `ADMIN_EMAIL`
- `SENDGRID_SERVER`, `SENDGRID_PORT`, `SENDGRID_USERNAME`, `SENDGRID_PASSWORD`

Le frontend Datadog peut utiliser :

- `VUE_APP_DATADOG_APPLICATION_ID`
- `VUE_APP_DATADOG_CLIENT_TOKEN`
- `VUE_APP_DATADOG_SITE`
- `VUE_APP_DATADOG_SERVICE`
- `VUE_APP_DATADOG_ENV`

## Tests et contrôles recommandés

Backend :

```bash
python3 manage.py check
python3 manage.py test
```

Frontend :

```bash
(cd frontend && npm run build)
python3 manage.py collectstatic --noinput
```

Pour une modification documentaire seulement, vérifier au minimum le diff Git et, si l'environnement Python est prêt, `python3 manage.py check`.
