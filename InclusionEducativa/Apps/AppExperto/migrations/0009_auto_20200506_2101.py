# Generated by Django 2.2.7 on 2020-05-06 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestionSistema', '0017_auto_20200430_2314'),
        ('AppExperto', '0008_auto_20200419_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='fichaEstudiante',
        ),
        migrations.AddField(
            model_name='comentario',
            name='estudiante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GestionSistema.Estudiante'),
        ),
    ]