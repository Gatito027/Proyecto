from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='Index'),
    path('login/', views.login,name="Login"),
    path('registro/', views.registro,name='Registro'),
    path ('registroFinal/', views.registroFinal,name="RegistroFinal"),
    path('listaProyectos/<int:usuario>/', views.ListaProyectos, name='ListaProyectos'),
    path ('listaAlumnosProfesores/', views.ListaAlumnosProfesores,name="ListaAlumnosProfesores"),
    path('introduccionCoil/', views.IntroduccionCoil,name="IntroduccionCoil"),
    path('ProyectoDetail/', views.ProyectoDetail,name="ProyectoDetail"),
    path('ListaActividadesPorFases/', views.ListaActividadesPorFases, name="ListaActividadesPorFases"),
    path('ConfiguracionProyecto/',views.ConfiguracionProyecto, name="ConfiguracionProyecto"),
    path('SeguimientoActividad/',views.SeguimientoActividad,name='SeguimientoActividad'),
    path('ViAlActividades/',views.ViAlActividades,name="ViAlActividades"),
    path('ViAlMateriales/',views.ViAlMateriales,name="ViAlMateriales"),
    path('ActividadesPendientes/',views.ActividadesPendientes,name="ActividadesPendientes"),
    path('FasesCoil/',views.indexFases,name="FasesCoil"),
    path('Fase1/',views.Fase1,name="Fase1"),
    path('Fase2/',views.Fase2,name="Fase2"),
    path('Fase3/',views.Fase3,name="Fase3"),
    path('Fase4/',views.Fase4,name="Fase4"),
    path('Fase5/',views.Fase5,name="Fase5"),
    
    # path('articulos/',views.articulos,name="articulos"),
    # path('articulo/',views.arcticulo,name="articulo"),

]