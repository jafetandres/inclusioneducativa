# Generated by Django 2.2.7 on 2020-06-23 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionSistema', '0001_initial'),
        ('AppRepresentante', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichainformativarepresentante',
            name='estudiante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GestionSistema.Estudiante'),
        ),
        migrations.AddField(
            model_name='fichainformativarepresentante',
            name='representante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GestionSistema.Representante'),
        ),
    ]