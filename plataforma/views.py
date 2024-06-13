from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    return redirect('Login')

def login(request): 
    return render(request , 'pages/login/login.html')

def registro (request): 
    return render(request , 'pages/registro/registro.html')

def registroFinal (request): 
    return render(request , 'pages/registro/registroFinal.html')


def ListaProyectos(request,usuario):
    return render(request,'pages/proyectos/ListaProyectos.html')

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

# def articulos(request):
#     return render(request,'pages/articulos.html')

# def arcticulo(request):
#     return render(request,'pages/articulo.html')
