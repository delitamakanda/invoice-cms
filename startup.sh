wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.stretch_amd64.deb
apt-get install -y ./wkhtmltox_0.12.6-1.stretch_amd64.deb
rm wkhtmltox_0.12.6-1.stretch_amd64.deb

gunicorn --bind=0.0.0.0 --timeout 600 --chdir invoices wsgi  --access-logfile '-' --error-logfile '-'
