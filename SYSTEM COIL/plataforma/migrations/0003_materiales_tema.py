# Generated by Django 5.0.6 on 2024-07-17 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0002_materiales'),
    ]

    operations = [
        migrations.AddField(
            model_name='materiales',
            name='tema',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
