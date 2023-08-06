"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets
import accounting.views
from article import views
from accounting.models import ContractSale


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('detail/<int:id>', views.detail, name="detail"),
    path('article/', include("article.urls")),
    path('user/', include("user.urls")),
    path('accounting/', include("accounting.urls")),
    path('error_404/', accounting.views.error_404, name='error_404')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler403 = 'mysite.views.my_custom_permission_denied_view'
# handler400 = 'mysite.views.my_custom_bad_request_view'
handler404 = "accounting.views.error_404"
# handler500 = "accounting.views.error_500"
