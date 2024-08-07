# Generated by Django 5.0.6 on 2024-08-04 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0004_remove_materiales_comentarios_priv_id_material_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materiales_comentarios_priv',
            name='id_actividad',
        ),
        migrations.AddField(
            model_name='materiales_comentarios_priv',
            name='id_material',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='plataforma.materiales'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Actividades_Comentarios_priv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateTimeField()),
                ('fecha_edit', models.DateTimeField()),
                ('id_actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.actividades')),
                ('id_alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plataforma.alumno')),
                ('id_profesor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plataforma.profesor')),
            ],
        ),
    ]