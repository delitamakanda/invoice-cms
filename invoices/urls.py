"""invoices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .auth_views import CurrentUserView, TokenLoginView, TokenLogoutView, UserCreateView
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', UserCreateView.as_view(), name='user-create'),
    path('api/v1/users/me/', CurrentUserView.as_view(), name='user-me'),
    path('api/v1/token/login/', TokenLoginView.as_view(), name='token-login'),
    path('api/v1/token/logout/', TokenLogoutView.as_view(), name='token-logout'),
    path('api/v1/', include('apps.client.urls')),
    path('api/v1/', include('apps.team.urls')),
    path('api/v1/', include('apps.invoice.urls')),
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type="text/plain"), name='ads'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type="text/plain"), name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', TemplateView.as_view(template_name='application.html'), name='application'),
]
