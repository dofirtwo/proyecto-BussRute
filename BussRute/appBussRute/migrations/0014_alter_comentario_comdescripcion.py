# Generated by Django 4.2.1 on 2023-09-05 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appBussRute', '0013_alter_comentario_comruta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='comDescripcion',
            field=models.CharField(max_length=500),
        ),
    ]
