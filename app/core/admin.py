from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from import_export.admin import ImportExportMixin

from assistencia_tecnica.models import Provincia, Distrito, UnidadeSanitaria, Sector, Area, Indicador, FichaAssistenciaTecnica
from users.models import User
from si_stock.models import Provincia as ProvinciaStock, Sector as SectorStock, Instrumento, Entrada, Requisicao, Aprovacao, Resumo, ResumoVisualizacao, Necessidade
from sondagemIS.models import Intervencao, FaixaEtaria, ServicoPrevencao, ServicoCuidadosTratamento, SectorClinico, Inquerito


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

class ProvinciaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome']


class DistritoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'provincia']


class UnidadeSanitariaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'distrito']


class SectorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome']


class AreaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'sector']


class IndicadorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'area']


class FichaAssistenciaTecnicaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome_responsavel', 'nome_provedor', 'problemas_identificados',
                    'tipo_problema', 'atcividades_realizar_resolver_problema']


class ProvinciaAdminStock(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome']


class SectorAdminStock(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'provincia', 'nome']
    list_filter = ('nome', 'provincia',)


class InstrumentoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'provincia', 'sector',
                    'nome', 'stock', 'ano', 'quantidade_necessaria']
    list_filter = ('provincia', 'sector', 'nome',)


class NecessidadeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'provincia', 'sector',
                    'instrumento', 'ano', 'quantidade']
    list_filter = ('provincia', 'sector',)


class EntradaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'data_entrada', 'fornecedor',
                    'quantidade', 'provincia', 'instrumento']
    list_filter = ('provincia',)


class LevantamentoDepositoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'data_levantamento',
                    'provincia', 'instrumento', 'quantidade']


class RequisicaoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'data_requisicao', 'provincia',
                    'instrumento', 'quantidade', 'status_requisicao']


class AprovacaoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'requisicao', 'tipo_aprovacao', 'comentario']


class ResumoAdmin(admin.ModelAdmin):
    list_display = ['provincia', 'sector', 'instrumento', 'data_entrada', 'quantidade',
                    'stock', 'necessidade', 'data_requisicao', 'quantidade_requisicao', 'status_requisicao']
    list_filter = ('provincia', 'sector',)


class IntervencaoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome']


class InqueritoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'provincia', 'distrito', 'unidade_sanitaria',
                    'data_inquerito', 'razoes_procura_servicos', 'faixa_etaria', 'sector_clinico']


class TxCurrCounterAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'date', 'hour', 'value']


admin.site.register(User, UserAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Distrito, DistritoAdmin)
admin.site.register(UnidadeSanitaria, UnidadeSanitariaAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Indicador, IndicadorAdmin)
admin.site.register(FichaAssistenciaTecnica, FichaAssistenciaTecnicaAdmin)
admin.site.register(ProvinciaStock, ProvinciaAdminStock)
admin.site.register(SectorStock, SectorAdminStock)
admin.site.register(Instrumento, InstrumentoAdmin)
admin.site.register(Necessidade, NecessidadeAdmin)
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(Requisicao, RequisicaoAdmin)
admin.site.register(Aprovacao, AprovacaoAdmin)
admin.site.register(Resumo, ResumoAdmin)
admin.site.register(Intervencao, IntervencaoAdmin)
admin.site.register(FaixaEtaria)
admin.site.register(SectorClinico)
admin.site.register(ServicoCuidadosTratamento)
admin.site.register(ServicoPrevencao)
admin.site.register(Inquerito, InqueritoAdmin)


admin.site.site_header = 'ECHO SYSTEMS'
