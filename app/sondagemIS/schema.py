import graphene 
from graphene_django import DjangoObjectType
from sondagemIS.models import Intervencao, Inquerito, FaixaEtaria, ServicoPrevencao, ServicoCuidadosTratamento, SectorClinico
from assistencia_tecnica.models import Provincia, Distrito, UnidadeSanitaria
from app.permissions import is_authenticated, paginate
from django.db.models import Q

class ProvinciaSondagemType(DjangoObjectType):
    class Meta:
        model = Provincia
        
class DistritoSondagemType(DjangoObjectType):
    class Meta:
        model = Distrito
        
class UnidadeSanitariaSondagemType(DjangoObjectType):
    class Meta:
        model = UnidadeSanitaria
        
class IntervencaoType(DjangoObjectType):
    class Meta:
        model = Intervencao
        
class FaixaEtariaType(DjangoObjectType):
    class Meta:
        model = FaixaEtaria
        
class InqueritoType(DjangoObjectType):
    class Meta:
        model = Inquerito
        
class ServicoPrevencaoType(DjangoObjectType):
    class Meta:
        model = ServicoPrevencao
        
class ServicoCuidadosTratamentoType(DjangoObjectType):
    class Meta:
        model = ServicoCuidadosTratamento
        
class SectorClinicoType(DjangoObjectType):
    class Meta:
        model = SectorClinico
        

class Query(graphene.ObjectType):
    provincias = graphene.List(ProvinciaSondagemType)
    provincia = graphene.Field(ProvinciaSondagemType, id=graphene.Int())
    distritos = graphene.List(DistritoSondagemType)
    distrito_by_province = graphene.List(DistritoSondagemType, provincia_id=graphene.Int())
    unidades_sanitarias = graphene.List(UnidadeSanitariaSondagemType)
    us_by_district = graphene.List(UnidadeSanitariaSondagemType, distrito_id=graphene.Int())
    intervencoes = graphene.List(IntervencaoType)
    faixas_etarias = graphene.List(FaixaEtariaType)
    inqueritos = graphene.Field(paginate(InqueritoType), page=graphene.Int(), search=graphene.String())
    servicos_prevencaos = graphene.List(ServicoPrevencaoType)
    servicos_cuidados = graphene.List(ServicoCuidadosTratamentoType)
    sectores_clinicos = graphene.List(SectorClinicoType)

    def resolve_provincias(self, info):
        return Provincia.objects.all()

    def resolve_distritos(self, info):
        return Distrito.objects.all()
    
    def resolve_distrito_by_province(self, info, provincia_id):
        provincia = Provincia.objects.get(id=provincia_id)
        return Distrito.objects.filter(provincia=provincia)
      
    
    def resolve_unidades_sanitarias(self, info):
        return UnidadeSanitaria.objects.all()
    
    def resolve_us_by_district(self, info, distrito_id):
        distrito = Distrito.objects.get(id=distrito_id)
        return Distrito.objects.filter(distrito=distrito)
    
    def resolve_intervencoes(self, info):
        return Intervencao.objects.all()
    
    def resolve_faixas_etarias(self, info):
        return FaixaEtaria.objects.all()
    
    def resolve_inqueritos(self, info, search=None):
        if search:
            filter = (
                Q(provincia__nome__icontains=search) |
                Q(distrito__nome__icontains=search) |
                Q(unidade_sanitaria__nome__icontains=search) |
                Q(nome__icontains=search)
            )
            return Inquerito.objects.filter(filter).order_by('-id')
        return Inquerito.objects.all().order_by('-id')
    
    def resolve_servicos_prevencaos(self, info):
        return ServicoPrevencao.objects.all()
    
    def resolve_servicos_cuidados(self, info):
        return ServicoCuidadosTratamento.objects.all()
    
    def resolve_sectores_clinicos(self, info):
        return SectorClinico.objects.all()
    
    
class CreateInquerito(graphene.Mutation):
    inquerito = graphene.Field(InqueritoType)
    provincia = graphene.Field(ProvinciaSondagemType)
    distrito = graphene.Field(DistritoSondagemType)
    unidade_sanitaria = graphene.Field(UnidadeSanitariaSondagemType)
    intervencao = graphene.Field(IntervencaoType)
    faixa_etaria = graphene.Field(FaixaEtariaType)
    sector_clinico = graphene.Field(SectorClinicoType)
    servico_prevencao = graphene.Field(ServicoPrevencaoType)
    servico_cuidado_tratamento = graphene.Field(ServicoCuidadosTratamentoType)
        
    class Arguments:
        nome = graphene.String(required=True)
        provincia_id = graphene.Int(required=True)
        distrito_id = graphene.Int(required=True)
        unidade_sanitaria_id = graphene.Int(required=True)
        data_inquerito = graphene.Date(required=True)
        intervencao_id = graphene.Int(required=True)
        outra_razao = graphene.String()
        faixa_etaria_id = graphene.Int(required=True)
        sector_clinico_id = graphene.Int(required=True)
        servico_prevencao_id = graphene.Int(required=True)
        servico_cuidado_tratamento_id = graphene.Int(required=True)
        
    def mutate(self, info, **kwargs):
        nome = kwargs.get('nome')
        provincia = Provincia.objects.get(id=kwargs.get('provincia_id'))
        distrito = Distrito.objects.get(id=kwargs.get('distrito_id'))
        unidade_sanitaria = UnidadeSanitaria.objects.get(id=kwargs.get('unidade_sanitaria_id'))
        data_inquerito = kwargs.get('data_inquerito')
        intervencao = Intervencao.objects.get(id=kwargs.get('intervencao_id'))
        outra_razao = kwargs.get('outra_razao')
        faixa_etaria = FaixaEtaria.objects.get(id=kwargs.get('faixa_etaria_id'))
        sector_clinico = SectorClinico.objects.get(id=kwargs.get('sector_clinico_id'))
        servico_prevencao = ServicoPrevencao.objects.get(id=kwargs.get('servico_prevencao_id'))
        servico_cuidado_tratamento = ServicoCuidadosTratamento.objects.get(id=kwargs.get('servico_cuidado_tratamento_id'))
        
        inquerito = Inquerito(
            nome = nome,
            provincia=provincia,
            distrito=distrito,
            unidade_sanitaria=unidade_sanitaria,
            data_inquerito=data_inquerito,
            razoes_procura_servicos=intervencao,
            outra_razao = outra_razao,
            faixa_etaria=faixa_etaria,
            sector_clinico=sector_clinico,
            servico_prevencao_recebeu=servico_prevencao,
            servico_cuidado_tratamento_recebeu=servico_cuidado_tratamento
        )
        inquerito.save()
        CreateInquerito(inquerito=inquerito)
        
        
class Mutation(graphene.ObjectType):
    create_inquerito = CreateInquerito.Field()