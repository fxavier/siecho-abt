from django.db import models
from users.models import User
from django.db.models.signals import pre_save, post_save
from datetime import datetime


FORNECEDOR = (
    ('ECHO', 'ECHO'),
    ('MISAU', 'MISAU'),
    ('LEVANTAMENTO DEPOSITO', 'LEVANTAMENTO NO DEPOSITO')
)

TIPO_APROVACAO = (
    ('Aprovada', 'Aprovada'),
    ('Rejeitada', 'Rejeitada')
)

STATUS_REQUISICAO = (
    ('Pendente', 'Pendente'),
    ('Aprovada', 'Aprovada'),
    ('Rejeitada', 'Rejeitada'),
)

class Provincia(models.Model):
    nome = models.CharField(max_length=150)
    
    def __str__(self):
        return self.nome
    
    
class Sector(models.Model):
    nome = models.CharField(max_length=150)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'
    
    def __str__(self):
        return self.nome
    
class Instrumento(models.Model):
    nome = models.CharField(max_length=150)
    stock = models.IntegerField()
    ano = models.PositiveSmallIntegerField()
    quantidade_necessaria = models.IntegerField()
    provincia = models.ForeignKey(Provincia, related_name='instrumentos', on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, related_name='instrumentos', on_delete=models.CASCADE)
        
    def __str__(self):
        return self.nome
    
class Necessidade(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    ano = models.PositiveSmallIntegerField()
    quantidade = models.IntegerField()
    # stock = models.IntegerField()
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feito_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.instrumento.nome

class EntradaManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) 
        if qs.count() == 1:
            return qs.first()
        return None    
    
class Entrada(models.Model):
    data_entrada = models.DateField()
    fornecedor = models.CharField(max_length=100, choices=FORNECEDOR)
    quantidade = models.IntegerField()
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feito_em = models.DateTimeField(auto_now=True)
    
    objects = EntradaManager()
    
    def __str__(self):
        return self.instrumento.nome
    

class Requisicao(models.Model):
    data_requisicao = models.DateField()
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feito_em = models.DateTimeField(auto_now=True)
    status_requisicao = models.CharField(max_length=50, choices=STATUS_REQUISICAO, default='Pendente')
    
    class Meta:
        verbose_name = 'Requisicao'
        verbose_name_plural = 'Requisicoes'
        
    def __str__(self):
        return self.instrumento.nome
    
class Aprovacao(models.Model):
    requisicao = models.ForeignKey(Requisicao, on_delete=models.CASCADE)
    tipo_aprovacao = models.CharField(max_length=100, choices=TIPO_APROVACAO)
    comentario = models.TextField(null=True, blank=True)
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE)
    feito_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Aprovacao'
        verbose_name_plural = 'Aprovacoes'
        
        
class Resumo(models.Model):
    provincia = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    instrumento = models.CharField(max_length=255, blank=True, null=True)
    data_entrada = models.DateField(blank=True, null=True)
    quantidade = models.IntegerField(blank=True, null=True)
    fornecedor = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    necessidade = models.IntegerField(blank=True, null=True)
    requisicao_id = models.IntegerField(blank=True, null=True)
    data_requisicao = models.DateField(blank=True, null=True)
    quantidade_requisicao = models.IntegerField(blank=True, null=True)
    status_requisicao = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Resumo de Instrumento'
        verbose_name_plural = 'Resumo de Instrumentos'
        
    def __str__(self):
        return self.instrumento.nome
    
class ResumoVisualizacao(models.Model):
    instrumento = models.CharField(max_length=255, blank=True, null=True)
    echo_misau = models.IntegerField(blank=True, null=True)
    necessidade = models.IntegerField(blank=True, null=True)
    stock_actual = models.IntegerField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Resumo Visualizacao'
        verbose_name_plural = 'Resumo Visualizacoes'
        
    def __str__(self):
        return self.instrumento
    
   

def update_stock(sender, instance, created, *args, **kwargs):
    if created:
        instrumento = Instrumento.objects.get(entrada=instance)
        instrumento.stock += instance.quantidade
        instrumento.save()
         
post_save.connect(update_stock, sender=Entrada)

def update_requisicao_status(sender, instance, created, *args, **kwargs):
    if created:
        requisicao = Requisicao.objects.get(aprovacao=instance)
        requisicao.status_requisicao = instance.tipo_aprovacao
        requisicao.save()
        if instance.tipo_aprovacao == 'Aprovada':
             instrumento = Instrumento.objects.get(pk=instance.requisicao.instrumento.id)
             instrumento.stock -= instance.requisicao.quantidade
             instrumento.save()
        # print('Created at:', datetime.now(), instance.tipo_aprovacao)
        # print("Instrumento:", instance.requisicao.instrumento.nome)
        # print("Instrumento:", instrumento.id, instrumento.nome, instance.requisicao.quantidade)
        
post_save.connect(update_requisicao_status, sender=Aprovacao)


        
        
    
    
    
    