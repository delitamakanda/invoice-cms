export LANG=C.UTF-8

apt-get install wkhtmltopdf
gunicorn — bind=0.0.0.0 — timeout 600 invoices.wsgi
