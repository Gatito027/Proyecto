from django.db import connection
from django.shortcuts import redirect, render
from .models import *
from datetime import datetime
import random

# Create your views here.
def index(request):
    return redirect('Login')

def login(request): 
    return render(request , 'pages/login/login.html')

def registro (request): 
    return render(request , 'pages/registro/registro.html')

def registroFinal (request): 
    return render(request , 'pages/registro/registroFinal.html')


def ListaProyectos(request, usuario):
    with connection.cursor() as cursor:
        cursor.callproc('BuscarRolByID', [usuario])
        rol = cursor.fetchone()[0]
        if rol == 1:
            cursor.callproc('ListaProfesoresproyecto', [])
            listaProfesores = cursor.fetchall()
            cursor.callproc('BuscarProyectos', [usuario])
            proyectos = cursor.fetchall()
        elif rol == 2:
            cursor.callproc('ListaProfesoresproyecto', [])
            listaProfesores = cursor.fetchall()
            cursor.callproc('BuscarProyectoImpartido', [usuario])
            proyectos = cursor.fetchall()
        else:
            return redirect('Error','Datos no validos')
    return render(request, 'pages/proyectos/ListaProyectos.html', {
        'rol': rol,
        'listaProfesores': listaProfesores,
        'proyectos': proyectos,
        'usuario' : usuario })

def generar_codigo_unico():
    while True:
        codigo = random.randint(-999999999, 999999999)
        with connection.cursor() as cursor:
            cursor.callproc('CodigosClase', [])
            codigos_clase = cursor.fetchall()
            codigos_existentes = {codigo_clase[0] for codigo_clase in codigos_clase}
            if codigo not in codigos_existentes:
                return codigo

def crearProyecto(request,usuario):
    nombre=request.POST['nombre']
    materia=request.POST['materia']
    descripcion=request.POST['descripcion']
    fecha_inicio=request.POST['fecha_inicio']
    fecha_fin=request.POST['fecha_fin']
    ciclo_escolar=request.POST['ciclo_escolar']
    color=request.POST['color']
    codigo =generar_codigo_unico()
    with connection.cursor() as cursor:
        cursor.callproc('CrearProyectocoil', [
            usuario,
            str(nombre),
            str(materia),
            str(codigo),
            str(descripcion),
            datetime.strptime(fecha_inicio, '%Y-%m-%d').date(),
            datetime.strptime(fecha_fin, '%Y-%m-%d').date(),
            str(ciclo_escolar),
            str(color)
        ])
        resultado = cursor.fetchone()[0]
    if resultado == 'Proyecto creado exitosamente':
        return redirect('IntroduccionCoil')
    else:
        return redirect('Error',resultado)
    
def UnirteProyecto(request, usuario):
    print(request.POST)
    codigo=request.POST['codigo']
    terminos=request.POST['terminos']
    redirect('Error','Prueba')

def IntroduccionCoil(request):
    return render(request,'pages/Proyectos/IntroduccionCoil.html',{'enlace_activo': 'coil'})

def ListaAlumnosProfesores (request): 
    return render(request , 'pages/Proyectos/ListaAlumnosProfesores.html',{'enlace_activo': 'personas'})


def ProyectoDetail(request):
    return render(request,'pages/Proyectos/ProyectoDetail.html',{'enlace_activo': 'tablon'})

def ListaActividadesPorFases(request):
    return render(request,'pages/Actividades/ListaActividadesPorFases.html',{'enlace_activo': 'tareas'})

def ConfiguracionProyecto(request):
    return render(request,'pages/Proyectos/ConfiguracionProyecto.html',{'enlace_activo': 'configurar'})

def SeguimientoActividad(request):
    return render(request,'pages/Actividades/SeguimientoActividad.html',{'enlace_activo': 'calificaciones'})

def ActividadesPendientes(request):
    return render(request, 'pages/Actividades/ActividadesPendientes.html')


def ViAlActividades(request):
    return render(request, 'pages/Actividades/ViAlActividades.html')

def ViAlMateriales(request):
    return render(request, 'pages/Materiales/ViAlMateriales.html')

def indexFases(request):
    return render(request, 'pages/FasesCoil/indexFases.html', {'enlace_activo': 'tareas','enlace_activo1': 'fases'})

def Fase1(request):
    return render(request, 'pages/FasesCoil/fase1.html', {'enlace_activo': 'tareas','enlace_activo1': 'fase1'})

def Fase2(request):
    return render(request, 'pages/FasesCoil/fase2.html', {'enlace_activo': 'tareas','enlace_activo1': 'fase2'})

def Fase3(request):
    return render(request, 'pages/FasesCoil/fase3.html', {'enlace_activo': 'tareas','enlace_activo1': 'fase3'})

def Fase4(request):
    return render(request, 'pages/FasesCoil/fase4.html', {'enlace_activo': 'tareas','enlace_activo1': 'fase4'})

def Fase5(request):
    return render(request, 'pages/FasesCoil/fase5.html', {'enlace_activo': 'tareas','enlace_activo1': 'fase5'})

def Error(request,error):
    return render(request, 'pages/error.html',{'error':error})


# def articulos(request):
#     return render(request,'pages/articulos.html')

# def arcticulo(request):
#     return render(request,'pages/articulo.html')

