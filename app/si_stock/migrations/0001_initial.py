# Generated by Django 3.2.25 on 2024-12-14 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aprovacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_aprovacao', models.CharField(choices=[('Aprovada', 'Aprovada'), ('Rejeitada', 'Rejeitada')], max_length=100)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('feito_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Aprovacao',
                'verbose_name_plural': 'Aprovacoes',
            },
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_entrada', models.DateField()),
                ('fornecedor', models.CharField(choices=[('ECHO', 'ECHO'), ('MISAU', 'MISAU'), ('LEVANTAMENTO DEPOSITO', 'LEVANTAMENTO NO DEPOSITO')], max_length=100)),
                ('quantidade', models.IntegerField()),
                ('feito_em', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('stock', models.IntegerField()),
                ('ano', models.PositiveSmallIntegerField()),
                ('quantidade_necessaria', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Necessidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.PositiveSmallIntegerField()),
                ('quantidade', models.IntegerField()),
                ('feito_em', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Requisicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_requisicao', models.DateField()),
                ('quantidade', models.IntegerField()),
                ('feito_em', models.DateTimeField(auto_now=True)),
                ('status_requisicao', models.CharField(choices=[('Pendente', 'Pendente'), ('Aprovada', 'Aprovada'), ('Rejeitada', 'Rejeitada')], default='Pendente', max_length=50)),
            ],
            options={
                'verbose_name': 'Requisicao',
                'verbose_name_plural': 'Requisicoes',
            },
        ),
        migrations.CreateModel(
            name='Resumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provincia', models.CharField(blank=True, max_length=255, null=True)),
                ('sector', models.CharField(blank=True, max_length=255, null=True)),
                ('instrumento', models.CharField(blank=True, max_length=255, null=True)),
                ('data_entrada', models.DateField(blank=True, null=True)),
                ('quantidade', models.IntegerField(blank=True, null=True)),
                ('fornecedor', models.CharField(blank=True, max_length=255, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('necessidade', models.IntegerField(blank=True, null=True)),
                ('requisicao_id', models.IntegerField(blank=True, null=True)),
                ('data_requisicao', models.DateField(blank=True, null=True)),
                ('quantidade_requisicao', models.IntegerField(blank=True, null=True)),
                ('status_requisicao', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Resumo de Instrumento',
                'verbose_name_plural': 'Resumo de Instrumentos',
            },
        ),
        migrations.CreateModel(
            name='ResumoVisualizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrumento', models.CharField(blank=True, max_length=255, null=True)),
                ('echo_misau', models.IntegerField(blank=True, null=True)),
                ('necessidade', models.IntegerField(blank=True, null=True)),
                ('stock_actual', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Resumo Visualizacao',
                'verbose_name_plural': 'Resumo Visualizacoes',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='si_stock.provincia')),
            ],
            options={
                'verbose_name': 'Sector',
                'verbose_name_plural': 'Sectores',
            },
        ),
    ]
