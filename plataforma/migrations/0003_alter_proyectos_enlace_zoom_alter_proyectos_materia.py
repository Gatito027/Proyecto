# Generated by Django 5.0.6 on 2024-06-27 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0002_rename_usuario_alumno_id_usuario_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyectos',
            name='enlace_zoom',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='proyectos',
            name='materia',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
