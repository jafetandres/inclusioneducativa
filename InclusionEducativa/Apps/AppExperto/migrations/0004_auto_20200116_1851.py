# Generated by Django 2.2.7 on 2020-01-16 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppExperto', '0003_comentario_fechacreacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
