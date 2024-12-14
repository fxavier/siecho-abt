from sre_constants import IN
import graphene
from graphene_django import DjangoObjectType
from si_stock.models import Provincia, Sector, Instrumento, Entrada, Requisicao, Aprovacao, Resumo, ResumoVisualizacao
from graphql import GraphQLError
from django.db.models import Q
from user.models import User
from app.permissions import is_authenticated, paginate
import user.schema


class ProvinciaType(DjangoObjectType):
    class Meta:
        model = Provincia
        
class SectorType(DjangoObjectType):
    class Meta:
        model = Sector
        
class InstrumentoType(DjangoObjectType):
    class Meta:
        model = Instrumento
        
class EntradaType(DjangoObjectType):
    class Meta:
        model = Entrada 
        
class RequisicaoType(DjangoObjectType):
    class Meta:
        model = Requisicao
        
class AprovacaoType(DjangoObjectType):
    class Meta:
        model = Aprovacao
        
class ResumoType(DjangoObjectType):
    class Meta:
        model = Resumo
        
class ResumoVisualizacaoType(DjangoObjectType):
    class Meta:
        model = ResumoVisualizacao

class Query(graphene.ObjectType):
    provincias = graphene.List(ProvinciaType)
    provincia = graphene.Field(ProvinciaType, id=graphene.Int())
    sectores = graphene.Field(paginate(SectorType), page=graphene.Int(), search=graphene.String())
    # search_sectores = graphene.Field(paginate(SectorType), page=graphene.Int(), search=graphene.String())
    # sectores = graphene.List(SectorType)
    sector = graphene.Field(SectorType, id=graphene.Int())
    sector_by_province = graphene.List(SectorType, provincia_id=graphene.Int())
    instrumentos = graphene.Field(paginate(InstrumentoType), page=graphene.Int(), search=graphene.String())
    # instrumentos = graphene.List(InstrumentoType)
    instrumento_by_sector = graphene.List(InstrumentoType, sector_id=graphene.Int())
    instrumento = graphene.Field(InstrumentoType, id=graphene.Int())
    entradas = graphene.Field(paginate(EntradaType), page=graphene.Int(), search=graphene.String())
    entrada = graphene.Field(EntradaType, id=graphene.Int())
    entrada_by_province = graphene.List(EntradaType, provincia_id=graphene.Int())
    requisicoes = graphene.Field(paginate(RequisicaoType), page=graphene.Int(), search=graphene.String())
    requisicao = graphene.Field(RequisicaoType, id=graphene.Int())
    requisicoes_pendentes = graphene.List(RequisicaoType)
    requisicao_by_province = graphene.List(RequisicaoType, provincia_id=graphene.Int())
    aprovacoes = graphene.Field(paginate(AprovacaoType), page=graphene.Int())
    resumos = graphene.List(ResumoType)
    resumo_visualizacoes = graphene.List(ResumoVisualizacaoType)
    
    
    def resolve_provincias(self, info):
        return Provincia.objects.all()
    
    def resolve_provincia(self, info, id):
        return Provincia.objects.get(id=id)
    
    # def resolve_sectores(self, info, provincia_id=None):
    #     if provincia_id:
    #         provincia = Provincia.objects.get(id=provincia_id)
    #         return Sector.objects.filter(provincia=provincia)
    #     return Sector.objects.all()
    
    def resolve_sectores(self, info, search=None):
        if search:
            filter = (
                Q(provincia__nome__icontains=search) |
                Q(nome__icontains=search)
            )
            return Sector.objects.filter(filter).order_by('-id')
        return Sector.objects.all().order_by('-id')
    
    def resolve_sector(self, info, id):
        return Sector.objects.get(id=id)
    
    def resolve_sector_by_province(self, info, provincia_id):
        provincia = Provincia.objects.get(id=provincia_id)
        return Sector.objects.filter(provincia=provincia)
    
    def resolve_instrumentos(self, info, search=None):
        if search:
            filter = (
                Q(nome__icontains=search) |
                Q(provincia__nome__icontains=search)
            )
            return Instrumento.objects.filter(filter).order_by('-id')
        return Instrumento.objects.select_related("provincia", "sector").all().order_by('-id')
    
    # def resolve_instrumentos(self, info):
    #     return Instrumento.objects.all()
    
    def resolve_instrumento(self, info, id):
        return Instrumento.objects.get(pk=id)
    
    def resolve_instrumento_by_sector(self, info, sector_id):
        sector = Sector.objects.get(id=sector_id)
        return Instrumento.objects.filter(sector=sector)
    
    def resolve_entradas(self, info, search=None):
        if search:
            filter = (
                Q(fornecedor__icontains=search) |
                Q(instrumento__nome__icontains=search) |
                Q(provincia__nome__icontains=search) |
                Q(sector__nome__icontains=search)
            )
            return Entrada.objects.filter(filter).order_by('-id')
        return Entrada.objects.all().order_by('-id')
    
    def resolve_entrada(self, info, id):
        return Entrada.objects.get(id=id)
    
    def resolve_entrada_by_province(self, info, province_id):
        provincia = Provincia.objects.get(id=province_id)
        return Entrada.objects.filter(provincia=provincia).order_by('-id')
    
    def resolve_requisicoes(self, info, search=None):
        if search:
            filter = (
                Q(provincia__nome__icontains=search) |
                Q(sector__nome__icontains=search) |
                Q(instrumento__nome__icontains=search) |
                Q(status_requisicao__icontains=search)
            )
            return Requisicao.objects.filter(filter).order_by('-id')
        return Requisicao.objects.all().order_by('-id')
    
    def resolve_requisicao(self, info, id):
        return Requisicao.objects.get(id=id)
    
    def resolve_requisicao_by_province(self, info, provincia_id):
        provincia = Provincia.objects.get(id=provincia_id)
        return Requisicao.objects.filter(provincia=provincia)
    
    def resolve_requisicoes_pendentes(self, info):
        return Requisicao.objects.filter(status_requisicao="Pendente")
    
    def resolve_aprovacoes(self, info):
        return Aprovacao.objects.all().order_by('-id')
    
    def resolve_resumos(self, info):
     
        return Resumo.objects.raw("select 1 AS id, p.nome AS provincia, s.nome AS sector, i.nome AS instrumento, i.stock," \
                                  "i.quantidade_necessaria AS necessidade,  e.data_entrada, e.quantidade, e.fornecedor, r.id AS requisicao_id," \
                                  "r.data_requisicao, r.quantidade AS quantidade_requisicao, r.status_requisicao from si_stock_instrumento i" \
                                  " inner join si_stock_sector s on s.id=i.sector_id" \
                                  " inner join si_stock_provincia p on i.provincia_id=p.id" \
                                  " left join si_stock_entrada e on e.instrumento_id=i.id" \
                                  " left join si_stock_requisicao r on r.instrumento_id=i.id"
                                   )
        
        
    def resolve_resumo_visualizacoes(self, info):
        return ResumoVisualizacao.objects.raw("select 1 AS id, i.nome AS instrumento, sum(e.quantidade) AS ECHO_MISAU, sum(i.quantidade_necessaria) Necessidade," \
                                               "sum(i.stock) AS  Stock_actual from si_stock_entrada e inner join si_stock_instrumento i on i.id=e.instrumento_id group by i.nome"
                                               )
        
# select s.nome as sector, i.nome as instrumento, sum(e.quantidade), e.fornecedor fornecedor, sum(i.quantidade_necessaria) Necessidade, sum(i.stock) as stock 
# from si_stock_instrumento i 
# inner join si_stock_sector s on s.id=i.sector_id 
# inner join  si_stock_entrada e on e.instrumento_id=i.id
# where i.ano=2022
# group by s.id, i.id, e.fornecedor

class CreateSector(graphene.Mutation):
    sector = graphene.Field(SectorType)
    provincia = graphene.Field(ProvinciaType)
      
    class Arguments:
        nome = graphene.String(required=True)
        provincia_id = graphene.Int(required=True)
           
    def mutate(self, info, **kwargs):
        nome = kwargs.get('nome')
        provincia = Provincia.objects.get(id=kwargs.get('provincia_id'))
       
        sector = Sector(
            nome=nome,
            provincia=provincia
        )
        sector.save()
        return CreateSector(sector=sector)
    
         
class CreateInstrumento(graphene.Mutation):
    instrumento = graphene.Field(InstrumentoType)
    provincia = graphene.Field(ProvinciaType)
    sector = graphene.Field(SectorType)
   
        
    class Arguments:
        nome = graphene.String(required=True)
        stock = graphene.Int()
        ano = graphene.Int()
        quantidade_necessaria = graphene.Int()
        provincia_id = graphene.Int(required=True)
        sector_id = graphene.Int(required=True)
        
        
        
    def mutate(self, info, **kwargs):
         nome = kwargs.get('nome')
         stock = kwargs.get('stock')
         ano = kwargs.get('ano')
         quantidade_necessaria = kwargs.get('quantidade_necessaria')
         provincia = Provincia.objects.get(id=kwargs.get('provincia_id'))
         if not provincia:
             raise GraphQLError('Provincia nao encontrada')
         sector = Sector.objects.get(id=kwargs.get('sector_id'))
         if not sector:
             raise GraphQLError('Sector nao encontrado')
         
      
         instrumento = Instrumento(
             nome=nome,
             stock=stock,
             ano=ano,
             quantidade_necessaria=quantidade_necessaria,
             provincia=provincia,
             sector=sector
          
         )
         instrumento.save()
         return CreateInstrumento(instrumento=instrumento)
     
class CreateEntrada(graphene.Mutation):
    entrada = graphene.Field(EntradaType)
    provincia = graphene.Field(ProvinciaType)
    sector = graphene.Field(SectorType)
    instrumento = graphene.Field(InstrumentoType)
    user = graphene.Field(user.schema.UserType)
    
    
    class Arguments:
        data_entrada = graphene.Date(required=True)
        provincia_id = graphene.Int(required=True)
        sector_id = graphene.Int(required=True)
        fornecedor = graphene.String(required=True)
        instrumento_id = graphene.Int(required=True)
        quantidade = graphene.Int(required=True)
        feito_em = graphene.Date()
        user_id = graphene.Int()
        
    def mutate(self, info, **kwargs):
        data_entrada = kwargs.get('data_entrada')
        provincia = Provincia.objects.get(id=kwargs.get('provincia_id'))
        sector = Sector.objects.get(id=kwargs.get('sector_id'))
        fornecedor = kwargs.get('fornecedor')
        instrumento = Instrumento.objects.get(id=kwargs.get('instrumento_id'))
        quantidade = kwargs.get('quantidade')
        feito_por = User.objects.get(id=kwargs.get('user_id'))
        
        entrada = Entrada(
            data_entrada=data_entrada,
            provincia=provincia,
            sector=sector,
            fornecedor=fornecedor,
            instrumento=instrumento,
            quantidade=quantidade,
            feito_por=feito_por
        )
        entrada.save()
        CreateEntrada(entrada=entrada)
        
class CreateRequisicao(graphene.Mutation):
    requisicao = graphene.Field(RequisicaoType)
    provincia = graphene.Field(ProvinciaType)
    sector = graphene.Field(SectorType)
    instrumento = graphene.Field(InstrumentoType)
    user = graphene.Field(user.schema.UserType)
    
    
    class Arguments:
        data_requisicao = graphene.Date(required=True)
        provincia_id = graphene.Int(required=True)
        sector_id = graphene.Int(required=True)
        instrumento_id = graphene.Int(required=True)
        quantidade = graphene.Int(required=True)
        status_requisicao = graphene.String()
        feito_em = graphene.Date()
        user_id = graphene.Int()
        
    def mutate(self, info, **kwargs):
        data_requisicao = kwargs.get('data_requisicao')
        provincia = Provincia.objects.get(id=kwargs.get('provincia_id'))
        sector = Sector.objects.get(id=kwargs.get('sector_id'))
        instrumento = Instrumento.objects.get(id=kwargs.get('instrumento_id'))
        quantidade = kwargs.get('quantidade')
        feito_por = User.objects.get(id=kwargs.get('user_id'))
        
        requisicao = Requisicao(
            data_requisicao=data_requisicao,
            provincia=provincia,
            sector=sector,
            instrumento=instrumento,
            quantidade=quantidade,
            feito_por=feito_por
        )
        requisicao.save()
        CreateRequisicao(requisicao=requisicao)

class CreateAprovacao(graphene.Mutation):
    aprovacao = graphene.Field(AprovacaoType)
    requisicao = graphene.Field(RequisicaoType)
    user = graphene.Field(user.schema.UserType)
    
    
    class Arguments:
        requisicao_id = graphene.Int(required=True)
        tipo_aprovacao = graphene.String(required=True)
        comentario = graphene.String()
        feito_em = graphene.Date()
        user_id = graphene.Int()
        
    def mutate(self, info, **kwargs):
        requisicao = Requisicao.objects.get(id=kwargs.get('requisicao_id'))
        tipo_aprovacao = kwargs.get('tipo_aprovacao')
        comentario = kwargs.get('comentario')
        feito_por = User.objects.get(id=kwargs.get('user_id'))
        
        aprovacao = Aprovacao(
            requisicao=requisicao,
            tipo_aprovacao=tipo_aprovacao,
            comentario=comentario,
            feito_por=feito_por
        )
        aprovacao.save()
        CreateAprovacao(requisicao=requisicao)        
     
class UpdateSector(graphene.Mutation):
    sector = graphene.Field(SectorType)

    class Arguments:
        sector_id = graphene.Int(required=True)
        nome = graphene.String()
        

    def mutate(self, info, **kwargs):
        user = info.context.user
        sector = Sector.objects.get(id=kwargs.get('sector_id'))


        sector.nome = kwargs.get('nome')
        sector.provincia = Provincia.objects.get(id=kwargs.get('provincia_id'))
       

        sector.save()

        return UpdateSector(sector=sector)
     
     
class Mutation(graphene.ObjectType):
    create_sector = CreateSector.Field()
    create_instrumento = CreateInstrumento.Field()
    create_entrada = CreateEntrada.Field()
    create_requisicao = CreateRequisicao.Field()
    create_aprovacao = CreateAprovacao.Field()
         
         
         
