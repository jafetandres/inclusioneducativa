# Generated by Django 2.2.7 on 2020-04-24 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionSistema', '0011_auto_20200419_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='nombres',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]