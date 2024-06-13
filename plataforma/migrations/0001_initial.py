# Generated by Django 5.0.6 on 2024-06-12 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('fecha_edit', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pais', models.CharField(max_length=25)),
                ('nombre_universidad', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Entregas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrega', models.DateField()),
                ('avance', models.CharField(max_length=250)),
                ('entregado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Materiales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('fecha_edit', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Proyectos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('materia', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('ciclo_escolar', models.CharField(max_length=15)),
                ('achivo_proyecto', models.BooleanField(default=False)),
                ('color', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Anuncios_archivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('fecha', models.DateField()),
                ('id_anuncio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.anuncios')),
            ],
        ),
        migrations.CreateModel(
            name='Entregas_archivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('fecha', models.DateField()),
                ('id_entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.entregas')),
            ],
        ),
        migrations.CreateModel(
            name='Materiales_archivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('fecha', models.DateField()),
                ('id_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.materiales')),
            ],
        ),
        migrations.AddField(
            model_name='materiales',
            name='id_proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos'),
        ),
        migrations.AddField(
            model_name='anuncios',
            name='id_proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos'),
        ),
        migrations.CreateModel(
            name='Tareas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('fecha_edit', models.DateField()),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos')),
            ],
        ),
        migrations.AddField(
            model_name='entregas',
            name='id_tarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.tareas'),
        ),
        migrations.CreateModel(
            name='Tareas_archivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('fecha', models.DateField()),
                ('id_tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.tareas')),
            ],
        ),
        migrations.CreateModel(
            name='Temas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('puntuacion', models.CharField(max_length=5)),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos')),
            ],
        ),
        migrations.AddField(
            model_name='tareas',
            name='id_tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.temas'),
        ),
        migrations.AddField(
            model_name='materiales',
            name='id_tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.temas'),
        ),
        migrations.CreateModel(
            name='Usuarios_general',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=30)),
                ('matricula', models.IntegerField()),
                ('correo_electronico', models.CharField(max_length=35)),
                ('sexo', models.CharField(max_length=15)),
                ('nombre_usuario', models.CharField(max_length=50)),
                ('contrasena', models.CharField(max_length=250)),
                ('rol_usuario', models.IntegerField()),
                ('id_catalogo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.catalogo')),
            ],
        ),
        migrations.CreateModel(
            name='Tareas_comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('fecha_edit', models.DateField()),
                ('privado', models.BooleanField()),
                ('id_tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.tareas')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general')),
            ],
        ),
        migrations.AddField(
            model_name='tareas',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general'),
        ),
        migrations.AddField(
            model_name='proyectos',
            name='id_profesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general'),
        ),
        migrations.CreateModel(
            name='Profesores_proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateField()),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos')),
                ('id_profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general')),
            ],
        ),
        migrations.CreateModel(
            name='Presentacion_profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estudios', models.CharField(max_length=250)),
                ('descripcion', models.TextField()),
                ('id_profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general')),
            ],
        ),
        migrations.CreateModel(
            name='Materiales_comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('fecha_edit', models.DateField()),
                ('privado', models.BooleanField()),
                ('id_materiales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.materiales')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general')),
            ],
        ),
        migrations.AddField(
            model_name='materiales',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general'),
        ),
        migrations.AddField(
            model_name='entregas',
            name='id_alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general'),
        ),
        migrations.CreateModel(
            name='Anuncios_comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('fecha_edit', models.DateField()),
                ('id_anuncio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.anuncios')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general')),
            ],
        ),
        migrations.AddField(
            model_name='anuncios',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general'),
        ),
        migrations.CreateModel(
            name='Alumnos_proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateField()),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos')),
                ('id_alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.usuarios_general')),
            ],
        ),
    ]
