# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-15 17:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inicio', '0001_initial'),
        ('reusables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaseParticular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar', models.CharField(max_length=50)),
                ('nrocontacto', models.CharField(max_length=9, unique=True)),
                ('direccion', models.CharField(max_length=200)),
                ('fechasolicitud', models.DateField()),
                ('fechaclase', models.DateField()),
                ('horainicio', models.TimeField()),
                ('horafin', models.TimeField()),
                ('costohora', models.FloatField()),
                ('descuento', models.FloatField()),
                ('obsevacion', models.CharField(max_length=200)),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inicio.Docente')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inicio.Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechamatricula', models.DateField()),
                ('fechainicio', models.DateField()),
                ('fechafin', models.DateField()),
                ('montototal', models.FloatField()),
                ('descuento', models.FloatField()),
                ('numcuota', models.PositiveIntegerField()),
                ('tipopago', models.CharField(max_length=50)),
                ('conceptodescuento', models.CharField(max_length=200)),
                ('grado', models.CharField(max_length=1)),
                ('observacion', models.CharField(max_length=200)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inicio.Estudiante')),
                ('reusables', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reusables.Grupo')),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inicio.Institucion')),
            ],
        ),
        migrations.CreateModel(
            name='Practica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nrocontacto', models.CharField(max_length=9, unique=True)),
                ('fecharecepcion', models.DateField()),
                ('fechaentrega', models.DateField()),
                ('observacion', models.CharField(max_length=200)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inicio.Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='practica',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='servicios.Servicio'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='servicios.Servicio'),
        ),
        migrations.AddField(
            model_name='claseparticular',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='servicios.Servicio'),
        ),
        migrations.AddField(
            model_name='claseparticular',
            name='subnivel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reusables.SubNivel'),
        ),
    ]
