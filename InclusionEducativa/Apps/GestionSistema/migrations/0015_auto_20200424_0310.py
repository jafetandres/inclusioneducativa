# Generated by Django 2.2.7 on 2020-04-24 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionSistema', '0014_auto_20200424_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]