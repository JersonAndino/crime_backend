from django.contrib import admin
from django.contrib import messages
import datetime
from api.models import (
    Fecha,
    Topico,
    Parroquia,
    HechoTopico,
    Archivo,
    RegistroActualizacion,
)
from api.exceptions import ErrorProcesandoArchivo, ErrorProcesandoArchivoTipoError
from api.utils import load_data_desde_csv


# Register your models here.
class FechaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha_completa")
    # search_fields = ('title', 'code', 'country__name')
    list_filter = ("fecha_completa",)

    # raw_id_fields = ('fecha_completa',)
    def completar_fechas(self, request, queryset):
        ultima_fecha = Fecha.get_ultima_fecha().fecha_completa
        today = datetime.datetime.today().date()
        fechas_to_create = list()
        while True:
            ultima_fecha += datetime.timedelta(days=1)
            if ultima_fecha <= today:
                fechas_to_create.append(Fecha(fecha_completa=ultima_fecha, anio=ultima_fecha.year, semana=ultima_fecha.isocalendar().week))
            else:
                break

        Fecha.objects.bulk_create(fechas_to_create)

    completar_fechas.short_description = "Completar Fechas"
    actions = [completar_fechas]


class TopicoAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo", "nombre", "descripcion")
    # search_fields = ('title', 'code', 'country__name')
    list_filter = ("nombre",)
    # raw_id_fields = ('fecha_completa',)


class ParroquiaAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo", "nombre", "descripcion")
    # search_fields = ('title', 'code', 'country__name')
    list_filter = ("nombre",)
    # raw_id_fields = ('fecha_completa',)


class HechoTopicoAdmin(admin.ModelAdmin):
    list_display = ("id", "topico", "parroquia", "total_tweets")
    # search_fields = ('title', 'code', 'country__name')
    list_filter = ("topico",)
    # raw_id_fields = ('fecha_completa',)


class ArchivoAdmin(admin.ModelAdmin):
    list_display = ("id", "archivo", "tipo", "cargado", "usuario_carga", "fecha_carga")
    # search_fields = ('title', 'code', 'country__name')
    list_filter = ("tipo",)

    # raw_id_fields = ('fecha_completa',)
    def procesar_archivo(self, request, queryset):
        
        try:
            print("[INICIANDO ACTUALIZACION]")

            if len(queryset) > 1:
                self.message_user(
                    request,
                    "Solo puede aplicar una actualizacion a la vez",
                    messages.ERROR,
                )
                raise ErrorProcesandoArchivo

            obj_archivo = queryset[0]
            user = request.user
            
            loaded = False

            if obj_archivo.tipo == "TOPICO":
                loaded = load_data_desde_csv(obj_archivo.archivo, Topico)
            elif obj_archivo.tipo == "PARROQUIA":
                loaded = load_data_desde_csv(obj_archivo.archivo, Parroquia)
            elif obj_archivo.tipo == "HECHO":
                loaded = load_data_desde_csv(obj_archivo.archivo, HechoTopico)
            elif obj_archivo.tipo == "DATA":
                print("data")
            else:
                self.message_user(
                    request,
                    "El archivo no tiene un tipo definido, debe seleccionar un tipo para ser procesado",
                    messages.ERROR,
                )
                raise ErrorProcesandoArchivoTipoError
            if loaded:
                obj_archivo.cargado = True
                obj_archivo.usuario_carga = user
                obj_archivo.fecha_carga = datetime.datetime.now()
                obj_archivo.save()
                self.message_user(
                    request,
                    "Archivo procesado exitosamente",
                    messages.SUCCESS,
                )
            else:
                self.message_user(
                    request,
                    "Ocurrio un error en el procesamiento del archivo",
                    messages.ERROR,
                )
            print("TERMINANDO ACTUALIZACION")
        except Exception as e:
            print(e)

    procesar_archivo.short_description = "Procesar archivo"
    actions = [procesar_archivo]


class RegistroActualizacionAdmin(admin.ModelAdmin):
    list_display = ("id", "archivo", "fecha_creacion")
    # search_fields = ('title', 'code', 'country__name')
    list_filter = ("fecha_creacion",)
    # raw_id_fields = ('fecha_completa',)


admin.site.register(Fecha, FechaAdmin)
admin.site.register(Topico, TopicoAdmin)
admin.site.register(Parroquia, ParroquiaAdmin)
admin.site.register(HechoTopico, HechoTopicoAdmin)
admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(RegistroActualizacion, RegistroActualizacionAdmin)
