"""uygulama URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
# konfigürasyon dosyaları
from django.conf import settings
from django.conf.urls.static import static

# viewleri import
from urunApp.views import *
urlpatterns = [
    path('yonetici/', admin.site.urls),
    path('', anasayfa, name="anasayfa"),
    path("urun/olustur", createProduct, name="create-product"),
    path('urun/<urunId>', detail_page, name="urun-detay-sayfasi"),
    path('yorum-yap/<urunId>', makeComment, name="yorum-yap"),
    path('sayfa-bulunamadi', sayfa_bulunamadi, name="404")


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
