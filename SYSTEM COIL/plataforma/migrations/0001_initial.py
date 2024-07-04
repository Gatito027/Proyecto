# Generated by Django 5.0.6 on 2024-07-02 20:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_universidad', models.CharField(max_length=200)),
                ('pais', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('nombre_usuario', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('correo_institucional', models.EmailField(max_length=254, unique=True)),
                ('is_firstLogin', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.rol')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('matricula_dni', models.CharField(max_length=50)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'No Binario')], max_length=1)),
                ('id_usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('universidad_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.catalogo')),
            ],
        ),
        migrations.CreateModel(
            name='Anuncios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('fecha_edit', models.DateField()),
                ('id_alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plataforma.alumno')),
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
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('idmex_dni', models.CharField(max_length=20)),
                ('genero', models.CharField(choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('no_binario', 'No Binario')], max_length=20)),
                ('trayectoria_academica', models.TextField(blank=True, null=True)),
                ('trayectoria_profesional', models.TextField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('gustos_personales', models.TextField(blank=True, null=True)),
                ('id_usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('universidad_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.catalogo')),
            ],
        ),
        migrations.CreateModel(
            name='Anuncios_comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('fecha_edit', models.DateField()),
                ('id_alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plataforma.alumno')),
                ('id_anuncio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.anuncios')),
                ('id_profesor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plataforma.profesor')),
            ],
        ),
        migrations.AddField(
            model_name='anuncios',
            name='id_profesor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plataforma.profesor'),
        ),
        migrations.CreateModel(
            name='Proyectos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('materia', models.CharField(max_length=50, null=True)),
                ('codigo', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('ciclo_escolar', models.TextField()),
                ('achivo_proyecto', models.BooleanField(default=False)),
                ('color', models.CharField(max_length=10)),
                ('enlace_zoom', models.TextField(null=True)),
                ('id_profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.profesor')),
            ],
        ),
        migrations.CreateModel(
            name='Profesores_proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateField()),
                ('id_profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.profesor')),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos')),
            ],
        ),
        migrations.CreateModel(
            name='Fases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('puntuacion', models.CharField(max_length=5)),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos')),
            ],
        ),
        migrations.AddField(
            model_name='anuncios',
            name='id_proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos'),
        ),
        migrations.CreateModel(
            name='Alumnos_proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateField()),
                ('id_alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.alumno')),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.proyectos')),
            ],
        ),
    ]