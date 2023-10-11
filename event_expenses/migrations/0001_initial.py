# Generated by Django 4.2.6 on 2023-10-11 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividades',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField(blank=True)),
                ('valor', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Contactos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('CENA', 'CENA'), ('FIESTA', 'FIESTA'), ('VIAJE', 'VIAJE')], max_length=10)),
                ('foto', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('correo_electronico', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('apodo', models.CharField(max_length=100)),
                ('foto', models.CharField(max_length=100)),
                ('id_evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_expenses.evento')),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantesEventoActividad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valor_participacion', models.IntegerField()),
                ('id_actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_expenses.actividades')),
                ('id_evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_expenses.evento')),
                ('id_participante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_expenses.contactos')),
            ],
        ),
        migrations.AddField(
            model_name='evento',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_expenses.usuario'),
        ),
        migrations.AddField(
            model_name='contactos',
            name='correo_electronico_contacto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_expenses.usuario'),
        ),
        migrations.AddField(
            model_name='actividades',
            name='id_evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_expenses.evento'),
        ),
    ]
