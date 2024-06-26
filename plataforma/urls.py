from django.urls import path, include
from . import views
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index,name='Index'),
    path('ListaProyectos/', views.ListaProyectos, name='ListaProyectos'),
    path('listaArchivoProyectos/', views.ListaArchivoProyectos, name='ListaArchivoProyectos'),
    path('crearProyecto/',views.crearProyecto,name="crearProyecto"),
    path('unirteProyecto/',views.UnirteProyecto,name="unirteProyecto"),
    path ('ListaAlumnosProfesores/<str:codigo>', views.ListaAlumnosProfesores,name="ListaAlumnosProfesores"),
    path('IntroduccionCoil/<str:codigo>', views.IntroduccionCoil,name="IntroduccionCoil"),
    path('Foro/<str:codigo>', views.ProyectoDetail,name="ProyectoDetail"),
    path('ListaActividadesPorFases/', views.ListaActividadesPorFases, name="ListaActividadesPorFases"),
    path('ConfiguracionProyecto/<str:codigo>',views.ConfiguracionProyecto, name="ConfiguracionProyecto"),
    path('SeguimientoActividad/<str:codigo>',views.SeguimientoActividad,name='SeguimientoActividad'),
    path('ViAlActividades/',views.ViAlActividades,name="ViAlActividades"),
    path('ViAlMateriales/',views.ViAlMateriales,name="ViAlMateriales"),
    path('ActividadesPendientes/',views.ActividadesPendientes,name="ActividadesPendientes"),
    
    
    path('Registro/', views.Registro, name='Registro'),
    path('Login/', views.Login, name='Login'),
    path('Home/', views.Home, name="Home"),
    path('Logout/', views.logout_view, name='logout'),
    path('verificationcode/', views.verify_code, name='verify_code'),
    
    
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    
    
    
    path('registro_alumno/', views.RegistroAlumno, name='registro_alumno'),
    path('save_other_university/', views.save_other_university, name='save_other_university'),
    path('registro_profesor/', views.RegistroProfesor, name='registro_profesor'),
    
    
    
    path('Validatecredentials/', views.validate_credentials, name='validate_credentials'),
    path('Checkusername/', views.check_username, name='check_username'),
    path('fasesCoil/<str:codigo>',views.indexFases,name="FasesCoil"),
    path('fasesCoil/<str:codigo>/<str:nombre>',views.Fase1,name="Fase"),
    path('fase2/',views.Fase2,name="Fase2"),
    path('fase3/',views.Fase3,name="Fase3"),
    path('fase4/',views.Fase4,name="Fase4"),
    path('fase5/',views.Fase5,name="Fase5"),
    path('error/<str:error>',views.Error,name="Error"),
    path('Proyecto/<str:codigo>',views.UnirteProyectoPage, name="EntrarProyecto"),
    path('AgregarUsuarioProyecto/<int:proyecto>/<str:codigo>',views.AgregarUsuarioProyecto, name="AgregarUsuarioProyecto")
    # path('articulos/',views.articulos,name="articulos"),
    # path('articulo/',views.arcticulo,name="articulo"),

]