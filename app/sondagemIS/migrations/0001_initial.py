# Generated by Django 3.2.25 on 2024-12-14 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assistencia_tecnica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaixaEtaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Faixas Etarias',
            },
        ),
        migrations.CreateModel(
            name='Intervencao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Intervencoes',
            },
        ),
        migrations.CreateModel(
            name='SectorClinico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Sectores Clinicos',
            },
        ),
        migrations.CreateModel(
            name='ServicoCuidadosTratamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Servicos de Cuidadados e Tratamento',
            },
        ),
        migrations.CreateModel(
            name='ServicoPrevencao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Servicos de Prevencao',
            },
        ),
        migrations.CreateModel(
            name='Inquerito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data_inquerito', models.DateField()),
                ('outra_razao', models.CharField(blank=True, max_length=100, null=True)),
                ('distrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistencia_tecnica.distrito')),
                ('faixa_etaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sondagemIS.faixaetaria')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistencia_tecnica.provincia')),
                ('razoes_procura_servicos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sondagemIS.intervencao')),
                ('sector_clinico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sondagemIS.sectorclinico')),
                ('servico_cuidado_tratamento_recebeu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sondagemIS.servicocuidadostratamento')),
                ('servico_prevencao_recebeu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sondagemIS.servicoprevencao')),
                ('unidade_sanitaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistencia_tecnica.unidadesanitaria')),
            ],
        ),
    ]
