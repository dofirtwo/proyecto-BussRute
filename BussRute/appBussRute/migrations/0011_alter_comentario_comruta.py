# Generated by Django 4.2.1 on 2023-09-05 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appBussRute', '0010_comentario_comruta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='comRuta',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='appBussRute.ruta'),
        ),
    ]
