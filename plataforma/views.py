from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    return redirect('login')

def login(request): 
    return render(request , 'pages/login.html')

def registrate (request): 
    return render(request , 'pages/registro.html')

def registrateFinal (request): 
    return render(request , 'pages/RegistroFinal.html')

def InterfazAlumno(request):
    return render(request,'pages/InterfazAlumno.html')

def personas (request): 
    return render(request , 'pages/personas.html',{'enlace_activo': 'personas'})

def clase(request):
    return render(request,'pages/clase.html',{'enlace_activo': 'tablon'})

def tareas_clase(request):
    return render(request,'pages/tareasClase.html',{'enlace_activo': 'tareas'})

def configurar_clase(request):
    return render(request,'pages/configurarClase.html',{'enlace_activo': 'configurar'})

def calificaciones_clase(request):
    return render(request,'pages/calificacionesClase.html',{'enlace_activo': 'calificaciones'})

def tareas_pendientes(request):
    return render(request, 'pages/TareasPendientes.html')

def error_page(request):
    return render(request,'pages/errorPage.html')

def articulos(request):
    return render(request,'pages/articulos.html')

def arcticulo(request):
    return render(request,'pages/articulo.html')

def ViAlTareas(request):
    return render(request, 'pages/ViAlTareas.html')

def ViAlMateriales(request):
    return render(request, 'pages/ViAlMateriales.html')

def CrearArticulo(request):
    return render(request, 'pages/CrearArticulo.html')