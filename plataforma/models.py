from django.db import models

# Create your models here.
class Catalogo(models.Model):
    pais = models.CharField(max_length=25)
    nombre_universidad = models.CharField(max_length=70)

class Usuarios_general(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=30)
    matricula = models.IntegerField()
    correo_electronico = models.CharField(max_length=35)
    sexo = models.CharField(max_length=15)
    nombre_usuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=250)
    rol_usuario = models.IntegerField()
    id_catalogo = models.ForeignKey(Catalogo, on_delete=models.CASCADE)

class Proyectos(models.Model):
    nombre = models.CharField(max_length=100)
    materia = models.CharField(max_length=50)
    codigo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ciclo_escolar = models.CharField(max_length=15)
    achivo_proyecto = models.BooleanField(default=False)
    color = models.CharField(max_length=10)
    id_profesor = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)

class Anuncios(models.Model):
    comentario = models.TextField()
    fecha = models.DateField()
    fecha_edit = models.DateField()
    id_usuario = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)

class Anuncios_archivos(models.Model):
    path = models.TextField()
    fecha = models.DateField()
    id_anuncio= models.ForeignKey(Anuncios,on_delete=models.CASCADE)

class Anuncios_comentarios(models.Model):
    comentario = models.TextField()
    fecha = models.DateField()
    fecha_edit = models.DateField()
    id_usuario = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)
    id_anuncio= models.ForeignKey(Anuncios,on_delete=models.CASCADE)

class Temas(models.Model):
    titulo = models.CharField(max_length=50)
    puntuacion = models.CharField(max_length=5)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)

class Materiales(models.Model):
    comentario = models.TextField()
    fecha = models.DateField()
    fecha_edit = models.DateField()
    id_usuario = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    id_tema = models.ForeignKey(Temas, on_delete=models.CASCADE)

class Materiales_archivos(models.Model):
    path = models.TextField()
    fecha = models.DateField()
    id_material= models.ForeignKey(Materiales,on_delete=models.CASCADE)

class Materiales_comentarios(models.Model):
    comentario = models.TextField()
    fecha = models.DateField()
    fecha_edit = models.DateField()
    privado = models.BooleanField()
    id_usuario = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)
    id_materiales= models.ForeignKey(Materiales,on_delete=models.CASCADE)

class Tareas(models.Model):
    comentario = models.TextField()
    fecha = models.DateField()
    fecha_edit = models.DateField()
    id_usuario = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    id_tema = models.ForeignKey(Temas, on_delete=models.CASCADE)

class Tareas_archivos(models.Model):
    path = models.TextField()
    fecha = models.DateField()
    id_tarea= models.ForeignKey(Tareas,on_delete=models.CASCADE)

class Tareas_comentarios(models.Model):
    comentario = models.TextField()
    fecha = models.DateField()
    fecha_edit = models.DateField()
    privado = models.BooleanField()
    id_usuario = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)
    id_tarea= models.ForeignKey(Tareas,on_delete=models.CASCADE)

class Entregas(models.Model):
    fecha_entrega = models.DateField()
    avance = models.CharField(max_length=250)
    entregado = models.BooleanField()
    id_alumno = models.ForeignKey(Usuarios_general, on_delete=models.CASCADE)
    id_tarea= models.ForeignKey(Tareas,on_delete=models.CASCADE)

class Entregas_archivos(models.Model):
    path = models.TextField()
    fecha = models.DateField()
    id_entrega= models.ForeignKey(Entregas,on_delete=models.CASCADE)
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