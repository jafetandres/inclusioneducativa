# Generated by Django 2.2.7 on 2020-08-13 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200813_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='foto',
            field=models.ImageField(blank=True, default='img_perfil/default-avatar.jpg', null=True, upload_to='img_perfil'),
        ),
    ]
