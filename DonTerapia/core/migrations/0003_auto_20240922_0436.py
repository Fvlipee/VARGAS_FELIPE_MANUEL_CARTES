# Generated by Django 3.1.2 on 2024-09-22 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0002_auto_20240922_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariopersonalizado',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='usuariopersonalizado',
            name='paciente',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usuariopersonalizado',
            name='terapeuta',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usuariopersonalizado',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
