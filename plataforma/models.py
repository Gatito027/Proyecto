from django.db import models

# Create your models here.
class Catalogo(models.Model):
    pais = models.CharField(max_length=25)
    nombre_universidad = models.CharField(max_length=70)

class Usuarios_general(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=30)
    matricula = models.IntegerField
    correo_electronico = models.CharField(max_length=35)
    sexo = models.CharField(max_length=15)
    nombre_usuario = models.CharField(max_length=50)
    Contrasena = models.CharField(max_length=250)
    rol_usuario = models.IntegerField
    id_catalogo = models.ForeignKey(Catalogo, on_delete=models.CASCADE)

class Proyectos(models.Model):
    Nombre = models.CharField(max_length=100)
    Materia = models.CharField(max_length=50)
    Codigo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ciclo_escolar = models.CharField(max_length=15)
    achivo_proyecto = models.BooleanField(default=False)
    color = models.CharField(max_length=10)
    id_profesor = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)

class Presentacion_profesor(models.Model):
    estudios = models.CharField(max_length=250)
    descripcion = models.TextField()
    id_profesor = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)

class Profesores_proyecto(models.Model):
    fecha_ingreso = models.DateField()
    id_profesor = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)

class Alumnos_proyecto(models.Model):
    fecha_ingreso = models.DateField()
    id_alumno = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)


