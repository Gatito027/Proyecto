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
    path('proyectoDetail/', views.ProyectoDetail,name="ProyectoDetail"),
    path('listaActividadesPorFases/', views.ListaActividadesPorFases, name="ListaActividadesPorFases"),
    path('configuracionProyecto/',views.ConfiguracionProyecto, name="ConfiguracionProyecto"),
    path('seguimientoActividad/',views.SeguimientoActividad,name='SeguimientoActividad'),
    path('viAlActividades/',views.ViAlActividades,name="ViAlActividades"),
    path('viAlMateriales/',views.ViAlMateriales,name="ViAlMateriales"),
    path('actividadesPendientes/',views.ActividadesPendientes,name="ActividadesPendientes"),
    path('fasesCoil/',views.indexFases,name="FasesCoil"),
    path('fase1/',views.Fase1,name="Fase1"),
    path('fase2/',views.Fase2,name="Fase2"),
    path('fase3/',views.Fase3,name="Fase3"),
    path('fase4/',views.Fase4,name="Fase4"),
    path('fase5/',views.Fase5,name="Fase5"),
    path('crearProyecto/<int:usuario>/',views.crearProyecto,name="crearProyecto"),
    # path('unirteProyecto/<int:usuario>/',views.crearProyecto,name="unirteProyecto"),
    path('error/<str:error>',views.Error,name="Error")
    
    # path('articulos/',views.articulos,name="articulos"),
    # path('articulo/',views.arcticulo,name="articulo"),

]