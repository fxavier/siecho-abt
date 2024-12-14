# Generated by Django 3.2.25 on 2024-12-14 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FichaAssistenciaTecnica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_responsavel', models.CharField(max_length=255)),
                ('nome_provedor', models.CharField(max_length=255)),
                ('problemas_identificados', models.TextField()),
                ('tipo_problema', models.CharField(choices=[('Antigo', 'Antigo'), ('Novo', 'Novo')], max_length=100)),
                ('atcividades_realizar_resolver_problema', models.CharField(max_length=255)),
                ('nome_pessoa_responsavel_resolver', models.CharField(max_length=255)),
                ('email_pessoa_responsavel_resolver', models.CharField(max_length=255)),
                ('prazo', models.DateField()),
                ('nome_beneficiario_at', models.CharField(max_length=255)),
                ('comentarios', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Resolvido', 'Resolvido')], default='Pendente', max_length=255)),
                ('feito_em', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UnidadeSanitaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('distrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unidades_sanitarias', to='assistencia_tecnica.distrito')),
            ],
        ),
        migrations.CreateModel(
            name='Indicador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=500)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicadores', to='assistencia_tecnica.area')),
            ],
        ),
    ]