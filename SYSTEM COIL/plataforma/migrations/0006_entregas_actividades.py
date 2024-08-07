# Generated by Django 5.0.6 on 2024-08-05 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0005_remove_materiales_comentarios_priv_id_actividad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entregas_Actividades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(blank=True, null=True, upload_to='entregas')),
                ('fecha', models.DateField()),
                ('id_actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.actividades')),
                ('id_alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.alumno')),
            ],
        ),
    ]
