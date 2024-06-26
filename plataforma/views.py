from django.db import connection, transaction
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroForm, LoginForm, RegistroAlumnoForm, RegistroProfesorForm, VerificationCodeForm, EmailForm
from django.contrib.auth.decorators import login_required
from .models import Usuario, Catalogo, Alumno, Profesor, Rol
import json
from django.contrib  import messages
from datetime import datetime
import random
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.db.models import Q
from django.views.generic.edit import FormView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy


from django.template.loader import render_to_string
# Create your views here.
def index(request):
    return redirect('Login')

def LlenarLayout(request): 
        usuario = request.user
        tipo_usuario = usuario.rol.nombre
        correo = request.user.correo_institucional
        try:
            if tipo_usuario == "Alumno":
                alumno = Alumno.objects.get(id_usuario_id=usuario.id)
                universidad = alumno.universidad_origen
                id_alumno = alumno.id
                nombres= alumno.nombre
                apellidos = alumno.apellidos
                matricula = alumno.matricula_dni
                with connection.cursor() as cursor:
                    cursor.callproc('BuscarNombreProyectos', [id_alumno])
                    listaProyectos = cursor.fetchall()
            elif tipo_usuario == "Profesor":
                profesor = Profesor.objects.get(id_usuario_id=usuario.id)
                id_profesor = profesor.id
                nombres= profesor.nombre
                apellidos = profesor.apellidos
                matricula = profesor.idmex_dni
                universidad = profesor.universidad_origen
                with connection.cursor() as cursor:
                    cursor.callproc('BuscarProyectoNombreImpartido', [id_profesor])
                    listaProyectos = cursor.fetchall()
            else:
                return redirect('logout')
        except (Alumno.DoesNotExist, Profesor.DoesNotExist):
            return redirect('logout')
        return [
            tipo_usuario,
            usuario,
            nombres,
            apellidos,
            correo,
            matricula,
            universidad,
            listaProyectos]

@login_required(login_url='Login')
def ListaProyectos(request): 
        layout = LlenarLayout(request)
        usuario = request.user
        tipo_usuario = usuario.rol.nombre
        try:
            if tipo_usuario == "Alumno":
                alumno = Alumno.objects.get(id_usuario_id=usuario.id)
                id_alumno = alumno.id
                with connection.cursor() as cursor:
                    cursor.callproc('ListaProfesoresproyecto', [])
                    listaProfesores = cursor.fetchall()
                    cursor.callproc('BuscarProyectos', [id_alumno])
                    proyectos = cursor.fetchall()
            elif tipo_usuario == "Profesor":
                profesor = Profesor.objects.get(id_usuario_id=usuario.id)
                id_profesor = profesor.id
                with connection.cursor() as cursor:
                    cursor.callproc('ListaProfesoresproyecto', [])
                    listaProfesores = cursor.fetchall()
                    cursor.callproc('BuscarProyectoImpartido', [id_profesor])
                    proyectos = cursor.fetchall()
            else:
                return redirect('logout')
        except (Alumno.DoesNotExist, Profesor.DoesNotExist):
            return redirect('logout')
        return render(request, 'pages/Proyectos/ListaProyectos.html', {
            'listaProfesores': listaProfesores,
            'proyectos': proyectos,
            'usuario' : usuario,
            'layout' : layout})

@login_required(login_url='Login')
def ListaArchivoProyectos(request):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('ListaProfesoresproyecto', [])
                listaProfesores = cursor.fetchall()
                cursor.callproc('BuscarProyectosArchivado', [id_alumno])
                proyectos = cursor.fetchall()
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('ListaProfesoresproyecto', [])
                listaProfesores = cursor.fetchall()
                cursor.callproc('BuscarProyectoImpartidoArchivado', [id_profesor])
                proyectos = cursor.fetchall()
        else:
            return redirect('Error', 'Datos no válidos')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    return render(request, 'pages/Proyectos/ListaProyectos.html', {
        'rol': tipo_usuario,
        'listaProfesores': listaProfesores,
        'proyectos': proyectos,
        'usuario' : usuario,
        'layout' : layout})

def generar_codigo_unico():
    while True:
        codigo = random.randint(-999999999, 999999999)
        with connection.cursor() as cursor:
            cursor.callproc('CodigosClase', [])
            codigos_clase = cursor.fetchall()
            codigos_existentes = {codigo_clase[0] for codigo_clase in codigos_clase}
            if codigo not in codigos_existentes:
                return codigo

@login_required(login_url='Login')
def crearProyecto(request):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            return redirect('Error', 'sin permisos')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
        else:
            return redirect('Error', 'Datos no válidos')
        nombre = request.POST.get('nombre')
        materia = request.POST.get('materia')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        ciclo_escolar = request.POST.get('ciclo_escolar')
        color = request.POST.get('color')
        codigo = generar_codigo_unico() 
        with connection.cursor() as cursor:
            cursor.callproc('CrearProyectocoil', [
                id_profesor,
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
            return redirect('IntroduccionCoil', codigo)
        else:
            return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')


def ComprobarCodigoUsuario(request,codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('CodigosClase', [])
                codigos_bd = cursor.fetchall()
                proyecto_existe = False
                for tupla_codigo in codigos_bd:
                    if codigo in tupla_codigo:
                        proyecto_existe = True
                if proyecto_existe:
                    cursor.callproc('ComprobarAlumnoProyecto', [id_alumno, codigo])
                    comprobar = cursor.fetchone()[0]
                    if comprobar != codigo:
                        return 'No inscrito'
                    else:
                        return 'Inscrito'
                if not proyecto_existe:
                    return 'El proyecto de este código no existe'
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('CodigosClase', [])
                codigos_bd = cursor.fetchall()
                proyecto_existe = False
                for tupla_codigo in codigos_bd:
                    if codigo in tupla_codigo:
                        proyecto_existe = True
                if proyecto_existe:
                    cursor.callproc('ComprobarProfesorProyecto', [id_profesor, codigo])
                    comprobar = cursor.fetchone()[0]
                    if comprobar != codigo:
                        return 'No inscrito'
                    else:
                        return 'Inscrito'
                if not proyecto_existe:
                    return 'El proyecto de este código no existe'
        else:
            return 'Datos no válidos'
    except Exception as e:
        return e
    return 'Algo fallo'

@login_required(login_url='Login')
def UnirteProyecto(request):
    codigo = request.POST['codigo']
    terminos = request.POST['terminos']
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    if comprobacion == 'No inscrito':
        try:
            if tipo_usuario == "Alumno":
                alumno = Alumno.objects.get(id_usuario_id=usuario.id)
                id_alumno = alumno.id
                with connection.cursor() as cursor:
                    with transaction.atomic():
                        cursor.callproc('buscarProyectoPorCodigo', [codigo])
                        proyecto = cursor.fetchone()[0]
                        cursor.callproc('AgregarAlumno', [id_alumno, proyecto])
                        respuesta = cursor.fetchone()[0]
                        if respuesta == 'Agregado exitosamente':
                            return redirect('IntroduccionCoil', codigo)
                        else:
                            return redirect('Error','Error al agregar al proyecto')
            elif tipo_usuario == "Profesor":
                profesor = Profesor.objects.get(id_usuario_id=usuario.id)
                id_profesor = profesor.id
                with connection.cursor() as cursor:
                    cursor.callproc('buscarProyectoPorCodigo', [codigo])
                    proyecto = cursor.fetchone()[0]
                    with transaction.atomic():
                        cursor.callproc('AgregarProfesor', [id_profesor, proyecto])
                        respuesta = cursor.fetchone()[0]
                        if respuesta == 'Agregado exitosamente':
                            return redirect('IntroduccionCoil', codigo)
                        else:
                            return redirect('Error','Error al agregar al proyecto')
            else:
                return redirect('Error', 'Datos no válidos')
        except Exception as e:
            return redirect('Error',e)
    elif comprobacion == 'Inscrito':
        return redirect('FasesCoil', codigo)
    else:
        return redirect('Error', comprobacion)

@login_required(login_url='Login')
def AgregarUsuarioProyecto(request,proyecto,codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                with transaction.atomic():
                        cursor.callproc('AgregarAlumno', [ id_alumno, proyecto])
                        respuesta = cursor.fetchone()[0]
                        if respuesta == 'Agregado exitosamente':
                            return redirect('IntroduccionCoil',codigo)
                        else:
                            return redirect('Error','Error al agregar al proyecto')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                with transaction.atomic():
                        cursor.callproc('AgregarProfesor', [id_profesor, proyecto])
                        respuesta = cursor.fetchone()[0]
                        if respuesta == 'Agregado exitosamente':
                            return redirect('IntroduccionCoil',codigo)
                        else:
                            return redirect('Error','Error al agregar al proyecto')
        else:
            return redirect('Error','Datos no validos')
    except Exception as e:
        return redirect('Error',e)
    return redirect('Error','Algo fallo')

@login_required(login_url='Login')
def UnirteProyectoPage(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('buscarProyectoPorCodigo', [codigo])
                proyectoCodigo = cursor.fetchone()[0]
                cursor.callproc('BuscarNombreProyectosByCodigo', [codigo])
                ProyectoNombre = cursor.fetchone()[0]
                return render(request,'pages/Proyectos/EntrarProyecto.html', {
                    'usuario' : usuario,
                    'Proyecto':ProyectoNombre,
                    'proyectoCodigo':proyectoCodigo,
                    'codigo': codigo,
                    'layout' : layout})
        except Exception as e:
            return redirect('Error',e)
    elif comprobacion == 'Inscrito':
        return redirect('FasesCoil')
    else:
        return redirect('Error', comprobacion)

@login_required(login_url='Login')
def IntroduccionCoil(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            return render(request,'pages/Proyectos/IntroduccionCoil.html',{
                'enlace_activo': 'coil',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario' : usuario,
                'layout' : layout})
    else:
        return redirect('Error', comprobacion)

@login_required(login_url='Login')
def indexFases(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            cursor.callproc('buscarProyectoPorCodigo', [codigo])
            proyectoCodigo = cursor.fetchone()[0]
            cursor.callproc('ListasFasesByProyecto', [proyectoCodigo])
            fases = cursor.fetchall()
            return render(request,'pages/FasesCoil/indexFases.html',{
                'enlace_activo': 'tareas',
                'enlace_activo1': 'fases',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario' : usuario,
                'layout' : layout,
                'fases': fases})
    else:
        return redirect('Error', comprobacion)

@login_required(login_url='Login')
def Fase1(request,codigo,nombre):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            cursor.callproc('buscarProyectoPorCodigo', [codigo])
            proyectoCodigo = cursor.fetchone()[0]
            cursor.callproc('ListasFasesByProyecto', [proyectoCodigo])
            fases = cursor.fetchall()
            return render(request,'pages/FasesCoil/fase1.html',{
                'enlace_activo': 'tareas',
                'enlace_activo1': nombre,
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario' : usuario,
                'layout' : layout,
                'fases': fases})
    else:
        return redirect('Error', comprobacion)

@login_required(login_url='Login')
def ListaAlumnosProfesores (request, codigo): 
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            cursor.callproc('buscarProyectoPorCodigo', [codigo])
            proyectoCodigo = cursor.fetchone()[0]
            cursor.callproc('BuscarProyectoProfesores', [proyectoCodigo])
            profesores = cursor.fetchall()
            cursor.callproc('BuscarProyectoAlumnos', [proyectoCodigo])
            alumnos = cursor.fetchall()
            return render(request,'pages/Proyectos/ListaAlumnosProfesores.html',{
                'enlace_activo': 'personas',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario' : usuario,
                'layout' : layout,
                'profesores':profesores,
                'alumnos':alumnos})
    else:
        return redirect('Error', comprobacion)

@login_required(login_url='Login')
def ProyectoDetail(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            return render(request,'pages/Proyectos/ProyectoDetail.html',{
                'enlace_activo': 'tablon',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario' : usuario,
                'layout' : layout})
    else:
        return redirect('Error', comprobacion)

@login_required(login_url='Login')
def ListaActividadesPorFases(request):
    return render(request,'pages/Actividades/ListaActividadesPorFases.html',{'enlace_activo': 'tareas'})

@login_required(login_url='Login')
def ConfiguracionProyecto(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        if tipo_usuario == "Profesor":
            with connection.cursor() as cursor:
                cursor.callproc('BuscarProyectoByCodigo', [codigo])
                proyectoDetails = cursor.fetchall()
                return render(request,'pages/Proyectos/ConfiguracionProyecto.html',{
                    'enlace_activo': 'configurar',
                    'proyectoDetails': proyectoDetails,
                    'codigo': codigo,
                    'usuario' : usuario,
                    'layout' : layout})
        else:
            return redirect('Error', 'Sin permisos')
    else:
        return redirect('Error', comprobacion)

@login_required(login_url='Login')
def SeguimientoActividad(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return render('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            return render(request,'pages/Actividades/SeguimientoActividad.html',{
                'enlace_activo': 'calificaciones',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario' : usuario,
                'layout' : layout})
    else:
        return redirect('Error', comprobacion)

def ActividadesPendientes(request):
    return render(request, 'pages/Actividades/ActividadesPendientes.html')


def ViAlActividades(request):
    return render(request, 'pages/Actividades/ViAlActividades.html')

def ViAlMateriales(request):
    return render(request, 'pages/Materiales/ViAlMateriales.html')

@login_required(login_url='Login')
def RegistroAlumno(request):
    usuario = request.user

    if usuario.rol.nombre != "Alumno" or usuario.is_firstLogin == False:
        logout(request)
        return redirect('Login')

    if request.method == 'POST':
        form = RegistroAlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.id_usuario_id = usuario
            alumno.save()
            usuario.is_firstLogin = False
            usuario.save()
            messages.success(request, "Alumno registrado correctamente")
            # return redirect('ListaProyectos')  # Redirigir a la vista deseada después del registro
    else:
        form = RegistroAlumnoForm()

    return render(request, 'pages/Registro/FormularioAlumno.html', {'form': form, 'nombre_usuario': usuario.nombre_usuario})


@login_required(login_url='Login')
def RegistroProfesor(request):
    usuario = request.user
    if usuario.rol.nombre != "Profesor" or usuario.is_firstLogin == False:
        logout(request)
        return redirect('Login')

    if request.method == 'POST':
        form = RegistroProfesorForm(request.POST)
        if form.is_valid():
            profesor = form.save(commit=False)
            profesor.id_usuario_id = usuario
            profesor.save()
            usuario.is_firstLogin = False
            usuario.save()
            messages.success(request, "Profesor registrado correctamente")
            # return redirect('ListaProyectos')  # Redirigir a la vista deseada después del registro
    else:
        form = RegistroProfesorForm()

    return render(request, 'pages/Registro/FormularioProfesor.html', {'form': form, 'nombre_usuario': usuario.nombre_usuario})


def Registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guardar datos del formulario en la sesión para usar después
            request.session['registro_form_data'] = {
                'nombre_usuario': form.cleaned_data['nombre_usuario'],
                'correo_institucional': form.cleaned_data['correo_institucional'],
                'password': form.cleaned_data['password'],
                'rol': form.cleaned_data['rol'].id,  # Guardar el ID del rol
            }

            # Generar el código de verificación
            codigo_verificacion = get_random_string(6, allowed_chars='0123456789')

            # Enviar el correo de verificación
            send_mail(
                'Código de verificación',
                f'Tu código de verificación es: {codigo_verificacion}',
                'from@example.com',
                [form.cleaned_data['correo_institucional']],
                fail_silently=False,
            )
            
            # Guardar el código de verificación en la sesión
            request.session['codigo_verificacion'] = codigo_verificacion
            request.session['correo_institucional'] = form.cleaned_data['correo_institucional']

            messages.success(request, "Se envio un codigo para la verificacion del correo")
            # return redirect('verify_code')  # Redirigir a la vista de verificación de código
    else:
        form = RegistroForm()

    return render(request, 'pages/Registro/Registro.html', {'form': form})




def verify_code(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['code']
            codigo_correcto = request.session.get('codigo_verificacion')

            if codigo_ingresado == codigo_correcto:
                # Obtener datos de registro del usuario de la sesión
                registro_data = request.session.get('registro_form_data')

                if registro_data:
                    # Obtener el objeto Rol
                    rol_id = registro_data['rol']
                    rol = Rol.objects.get(id=rol_id)

                    # Guardar el usuario en la base de datos con el rol obtenido
                    usuario = Usuario.objects.create_user(
                        nombre_usuario=registro_data['nombre_usuario'],
                        password=registro_data['password'],
                        rol=rol  # Asignar la instancia de Rol obtenida
                    )
                    
                    usuario.correo_institucional = registro_data['correo_institucional']

                    usuario.save()  # Guardar el usuario con el correo institucional

                    messages.success(request, "Codigo correcto, Usuario registrado correctamente")
                    del request.session['registro_form_data']
                    del request.session['codigo_verificacion']
                    del request.session['correo_institucional']

                    # Realizar cualquier acción adicional después del registro exitoso

                    # return redirect('ListaProyectos')  # Redirigir a la página deseada después del registro

            else:
                form.add_error('code', 'Código de verificación incorrecto.')
    else:
        form = VerificationCodeForm()

    return render(request, 'pages/Registro/VerificarCodigo.html', {'form': form})


def save_other_university(request):
    usuario = request.user
    if request.method == 'POST':
        nombre_universidad = request.POST.get('nombre_universidad')
        pais = request.POST.get('pais')

        # Guarda en la base de datos
        nueva_universidad = Catalogo(nombre_universidad=nombre_universidad, pais=pais)
        nueva_universidad.save()
        if usuario.rol.nombre == "Alumno":
            return redirect('registro_alumno')
        elif usuario.rol.nombre == "Profesor":
            return redirect('registro_profesor')

    return render(request, 'pages/Modals/AgregarUniversidad.html')





def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            password = form.cleaned_data['password']
            usuario = authenticate(request, username=nombre_usuario, password=password)
            if usuario is not None:
                login(request, usuario)
                if usuario.is_firstLogin is True:
                    if usuario.rol.nombre == "Alumno":
                        return redirect('registro_alumno')
                    elif usuario.rol.nombre == "Profesor":
                        return redirect('registro_profesor')
                else:
                    return redirect('ListaProyectos')    
            else:
                print(f"Autenticación fallida para: {nombre_usuario}")
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
        else:
            print("Formulario no es válido")
    else:
        form = LoginForm()
    return render(request, 'pages/Login/Login.html', {'form': form})


@login_required(login_url='Login')
def Home(request):
    usuario = request.user  # Obtener el usuario autenticado
    nombre_completo = None
    tipo_usuario = usuario.rol.nombre
    id_user = usuario.id
    if usuario.rol.nombre == "Alumno":
        
        alumno = Alumno.objects.get(id_usuario_id=usuario.id)
        nombre_completo = f"{alumno.nombre} {alumno.apellidos}"
    elif usuario.rol.nombre == "Profesor":
        profesor = Profesor.objects.get(id_usuario_id=usuario.id)
        nombre_completo = f"{profesor.nombre} {profesor.apellidos}"
            
    
    return render(request, 'pages/Home/Home.html', {'nombre_completo': nombre_completo, 'tipo_usuario': tipo_usuario, 'id_user': id_user})

def logout_view(request):
    logout(request)
    return redirect('Login')



class CustomPasswordResetView(FormView):
    template_name = 'registration/password_reset_form.html'
    form_class = EmailForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        usuario = Usuario.objects.filter(correo_institucional=email).first()
        
        if usuario:
            self.send_password_reset_email(usuario)
            return super().form_valid(form)
        else:
            form.add_error('email', 'Correo no encontrado.')
            return self.form_invalid(form)




    def send_password_reset_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        reset_link = f"{self.request.scheme}://{self.request.get_host()}{url}"
        
        subject = 'Restablece tu contraseña'
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        send_mail(subject, message, 'tu_correo@example.com', [user.correo_institucional])

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Usuario.objects.filter(nombre_usuario__iexact=username).exists()
    }
    return JsonResponse(data)


def validate_credentials(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user_exists = Usuario.objects.filter(nombre_usuario__iexact=username).exists()
        user = authenticate(request, username=username, password=password)
        credentials_valid = user is not None
        return JsonResponse({
            'user_exists': user_exists,
            'credentials_valid': credentials_valid
        })

def Fase2(request):
    return render(request, 'pages/FasesCoil/fase2.html', {'enlace_activo': 'tareas','enlace_activo1': 'fase2'})

def Fase3(request):
    return render(request, 'pages/FasesCoil/fase3.html', {'enlace_activo': 'tareas','enlace_activo1': 'fase3'})

def Fase4(request):
    return render(request, 'pages/FasesCoil/fase4.html', {'enlace_activo': 'tareas','enlace_activo1': 'fase4'})

def Fase5(request):
    return render(request, 'pages/FasesCoil/fase5.html', {'enlace_activo': 'tareas','enlace_activo1': 'fase5'})

def Error(request,error):
    layout = LlenarLayout(request)
    return render(request, 'pages/error.html',{'error':error,'layout':layout})

# def articulos(request):
#     return render(request,'pages/articulos.html')

# def arcticulo(request):
#     return render(request,'pages/articulo.html')
