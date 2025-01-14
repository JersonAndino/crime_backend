# Generated by Django 5.1.3 on 2024-12-10 04:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fecha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_completa', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Fecha',
                'verbose_name_plural': 'Fechas',
            },
        ),
        migrations.CreateModel(
            name='Parroquia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('nombre', models.CharField()),
                ('descripcion', models.TextField()),
            ],
            options={
                'verbose_name': 'Parroquia',
                'verbose_name_plural': 'Parroquias',
            },
        ),
        migrations.CreateModel(
            name='Topico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('nombre', models.CharField()),
                ('descripcion', models.TextField()),
            ],
            options={
                'verbose_name': 'Topico',
                'verbose_name_plural': 'Topicos',
            },
        ),
        migrations.CreateModel(
            name='HechoTopico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_tweets', models.IntegerField()),
                ('fecha', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.fecha')),
                ('parroquia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.parroquia')),
                ('topico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.topico')),
            ],
            options={
                'verbose_name': 'Hecho',
                'verbose_name_plural': 'Hechos',
            },
        ),
    ]
