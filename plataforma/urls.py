from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('clase/', views.clase,name='clase'),
    path('tareaspen', views.tareas_pendientes, name='tareas_pendientes'),
    path('error', views.error_page, name='error_page'),
    path('login/', views.login,name="login"),
    path('registrate/', views.registrate,name="registrate"),
    path ('registrateFinal/', views.registrateFinal,name="registrateFinal"),
    path ('InterfazAlumno/', views.InterfazAlumno,name="InterfazAlumno"),
    path('personas/', views.personas,name="personas"),
    path('tareasClase/', views.tareas_clase,name="tareas_clase"),
    path('configrarClase/', views.configurar_clase, name="configurar_clase"),
    path('calificacionesClase/',views.calificaciones_clase, name="calificaciones"),
    path('introduccion/',views.introduccion_clase,name='introduccion'),
    path('articulos/',views.articulos,name="articulos"),
    path('articulo/',views.arcticulo,name="articulo"),
    path('ViAlTareas/',views.ViAlTareas,name="ViAlTareas"),
    path('ViAlMateriales/',views.ViAlMateriales,name="ViAlMateriales"),
    path('CrearArticulo/',views.CrearArticulo,name="CrearArticulo"),

]