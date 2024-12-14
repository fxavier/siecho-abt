from django.db import models
from assistencia_tecnica.models import Provincia, Distrito, UnidadeSanitaria


class Intervencao(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Intervencoes'

    def __str__(self):
        return self.nome


class FaixaEtaria(models.Model):
    descricao = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Faixas Etarias'

    def __str__(self):
        return self.descricao


class SectorClinico(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Sectores Clinicos'

    def __str__(self):
        return self.nome


class ServicoCuidadosTratamento(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Servicos de Cuidadados e Tratamento'

    def __str__(self):
        return self.nome


class ServicoPrevencao(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Servicos de Prevencao'

    def __str__(self):
        return self.nome


class Inquerito(models.Model):
    nome = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    unidade_sanitaria = models.ForeignKey(
        UnidadeSanitaria, on_delete=models.CASCADE)
    data_inquerito = models.DateField()
    razoes_procura_servicos = models.ForeignKey(
        Intervencao, on_delete=models.CASCADE, null=True, blank=True)
    outra_razao = models.CharField(max_length=100, null=True, blank=True)
    faixa_etaria = models.ForeignKey(FaixaEtaria, on_delete=models.CASCADE)
    sector_clinico = models.ForeignKey(SectorClinico, on_delete=models.CASCADE)
    servico_prevencao_recebeu = models.ForeignKey(
        ServicoPrevencao, on_delete=models.CASCADE)
    servico_cuidado_tratamento_recebeu = models.ForeignKey(
        ServicoCuidadosTratamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
