from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Catalogo)
admin.site.register(Usuarios_general)
admin.site.register(Proyectos)
admin.site.register(Anuncios)
admin.site.register(Anuncios_archivos)
admin.site.register(Anuncios_comentarios)
admin.site.register(Materiales)
admin.site.register(Materiales_archivos)
admin.site.register(Materiales_comentarios)
admin.site.register(Tareas)
admin.site.register(Tareas_archivos)
admin.site.register(Tareas_comentarios)
admin.site.register(Entregas)
admin.site.register(Entregas_archivos)
admin.site.register(Presentacion_profesor)
admin.site.register(Profesores_proyecto)
admin.site.register(Alumnos_proyecto)