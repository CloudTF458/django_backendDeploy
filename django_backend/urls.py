"""
URL configuration for django_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from event_expenses import views

# ================================================================================
#Enseñandole al proyecto la ruta de las urls
# ================================================================================
# --------------------------------------------------------------------------------
# Ruta ejemplo= http://localhost:8000/event_expenses/api/v1/usuario
# *** PARA VER MAS EJEMPLOS CONSULTAR EL ARCHIVO urls_ejemplos.txt ***
# --------------------------------------------------------------------------------

urlpatterns = [
     path('admin/', 
          admin.site.urls),
     path('login/user/', 
          views.login_user, name="login_user"),
     path('event_expenses/', 
          include('event_expenses.urls')),
     # Gestión de usuarios
     path('crear/usuario/', 
          views.crear_usuario, name="crear_usuario"),
     path('modificar/usuario/', 
          views.modificar_usuario, name="modificar_usuario"),
     # Gestión de contactos
     path('listar/contactos/', 
          views.listar_contactos, name="listar_contactos"),
     path('listar/contactos/evento/', 
          views.listar_contactos_evento, name="listar_contactos_evento"),
     path("agregar/contacto/", 
          views.agregar_contacto, name="agregar_contacto"),
     path("eliminar/contacto/", 
          views.eliminar_contacto, name="eliminar_contacto"),
     # Gestión de eventos
     path('crear/evento/', 
          views.crear_evento, name="crear_evento"),
     path('view/events-activities-as-participant/', 
          views.ver_eventos_actividades_usuario, name="ver_eventos_actividades_usuario"),
     path('view/pending-balance/', 
          views.ver_saldos_pendientes, name="ver_saldos_pendientes"),
     path('update/event/', 
          views.modificar_evento, name="modificar_evento"),
     path('view/activities/event/',
          views.ver_actividades_evento, name="ver_actividades_evento"),
     # Gestión de actividades
     path('create/activity/', 
          views.crear_actividad, name="crear_actividad"),
     path('delete/activity/', 
          views.quitar_actividad, name="quitar_actividad"),
]
