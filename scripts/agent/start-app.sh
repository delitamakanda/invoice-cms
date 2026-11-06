#!/usr/bin/env bash
# Démarre l'app pour les agents (MCP Playwright) en arrière-plan :
#   - API Django sur :8000 (SQLite locale `db.sqlite3`, ignorée par git),
#     migrée, avec un compte de test créé à chaque lancement ;
#   - serveur Vite (`npm run serve`) sur :8080, qui sert la SPA Vue et
#     redirige /api vers l'API Django (voir frontend/vite.config.js).
# Attend que les deux répondent. Logs dans .agent-out/*.log.
#
# Identifiants du compte de test : .agent-out/test-user.md (mot de passe
# aléatoire, propre au run ; à ne jamais recopier dans la PR).
#
# Emails : backend console des settings locaux (rien n'est envoyé).
# Facturation électronique / e-reporting : services mock du dépôt.
# PDF : nécessite wkhtmltopdf (installé par les workflows).
#
# Prérequis : pip install -r requirements.txt et npm ci --prefix frontend.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

PYTHON="${PYTHON:-python}"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON=python3

out=.agent-out
mkdir -p "$out/playwright"

"$PYTHON" manage.py migrate --noinput > "$out/migrate.log" 2>&1

user="${AGENT_TEST_USER:-agent}"
password="${AGENT_TEST_PASSWORD:-$(openssl rand -hex 12)}"
AGENT_TEST_USER="$user" AGENT_TEST_PASSWORD="$password" "$PYTHON" manage.py shell -c "
import os
from django.contrib.auth.models import User
u, _ = User.objects.get_or_create(username=os.environ['AGENT_TEST_USER'], defaults={'email': 'agent@example.test'})
u.set_password(os.environ['AGENT_TEST_PASSWORD'])
u.save()
"
cat > "$out/test-user.md" <<EOF
# Compte de test (app locale uniquement)

- Page de connexion : http://localhost:8080/sign-in
- Nom d'utilisateur : $user
- Mot de passe : $password
EOF

nohup "$PYTHON" manage.py runserver 8000 > "$out/api.log" 2>&1 < /dev/null &
(cd frontend && nohup npx vite --port 8080 --strictPort > "../$out/vite.log" 2>&1 < /dev/null &)

if ! timeout "${START_TIMEOUT:-300}" bash -c \
  'until curl -sf http://localhost:8000/admin/login/ >/dev/null && curl -sf http://localhost:8080/ >/dev/null; do sleep 3; done'; then
  echo "::error::l'app n'a pas démarré à temps"
  tail -n 50 "$out/api.log" "$out/vite.log"
  exit 1
fi
echo "App prête : http://localhost:8080 (API Django : http://localhost:8000/api/v1, compte de test dans $out/test-user.md)"
