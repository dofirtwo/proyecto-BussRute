# Generated by Django 4.2.1 on 2023-09-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appBussRute', '0011_alter_comentario_comruta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruta',
            name='rutNumero',
            field=models.IntegerField(db_comment='Numero de la ruta del bus', null=True),
        ),
    ]
