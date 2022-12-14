"""EjemploORM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.inicio),
    path('respuesta', views.respuesta),
    path('registro', views.registro),
    path('listar', views.listar),
    path('listarEditar', views.listarEditar),
    path('listarProductos', views.listarProductos, name="listarProductos"),
    path('actualizar', views.actualizar),
    path('actualiza', views.actualiza),
    path('modificarProducto/<id>/',views.modificarProducto, name="modificarProducto"),
    path('elimina', views.elimina),
    path('eliminar', views.eliminar),
    path('eliminarProducto/<id>/', views.eliminarProducto, name="eliminarProducto"),
    path('ingresar',views.ingresar),
    path('ingresarProducto',views.ingresarProducto),
    path('agregarProducto',views.agregarProducto),
    path('iniciar_sesion', views.iniciar_sesion, name="iniciar_sesion"),
    path('sesion',views.sesion),
    path('detalleProducto/<id>/',views.detalleProducto, name="detalleProducto"),
    path('admin/', admin.site.urls),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
