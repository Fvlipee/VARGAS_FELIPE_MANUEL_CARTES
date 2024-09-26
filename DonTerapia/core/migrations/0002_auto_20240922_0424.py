# Generated by Django 3.1.2 on 2024-09-22 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuariopersonalizado',
            name='es_paciente',
        ),
        migrations.RemoveField(
            model_name='usuariopersonalizado',
            name='es_terapeuta',
        ),
        migrations.AddField(
            model_name='usuariopersonalizado',
            name='paciente',
            field=models.BooleanField(default=False, verbose_name='Es Paciente'),
        ),
        migrations.AddField(
            model_name='usuariopersonalizado',
            name='terapeuta',
            field=models.BooleanField(default=False, verbose_name='Es Terapeuta'),
        ),
    ]
