"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.login.urls')),
    path('user/',include('core.user.urls')),
    path('doctor/',include('core.doctor.urls')),
    path('nurse/',include('core.nurse.urls')),
    path('patient/',include('core.patient.urls')),
    path('appointment/',include('core.appointment.urls')),
    path('product/',include('core.product.urls')),
    path('sale/',include('core.sale.urls')),
    path('office/',include('core.office.urls')),
    path('clinical-history/',include('core.clinical_history.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
