# Generated by Django 2.2.7 on 2020-04-14 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionSistema', '0008_auto_20200414_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]