from api.models import Topico, Parroquia, HechoTopico
from api.serializers import TopicoSerializer, ParroquiaSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from .models import Archivo
from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Sum, F
from dateutil.relativedelta import relativedelta
import datetime
import pandas as pd


class GetTopicos(APIView):
    def get(self, request):
        qs = Topico.objects.all()
        serializer = TopicoSerializer(qs, many=True)
        return Response({"data": serializer.data})


class GetParroquias(APIView):
    def get(self, request):
        qs = Parroquia.objects.all()
        serializer = ParroquiaSerializer(qs, many=True)
        return Response({"data": serializer.data})


class GetParroquiasJSON(APIView):
    def get(self, request):
        qs = Parroquia.objects.all()
        data = dict()
        for parroquia in qs:
            data.__setitem__(parroquia.codigo, parroquia.nombre)
        return Response({"data": data})


class GetHechosForMap(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        fecha_inicio = (
            datetime.datetime.strptime(data.get("fecha_inicio"), "%Y-%M-%d").date()
            if len(data.get("fecha_inicio")) > 0
            else None
        )
        fecha_fin = (
            datetime.datetime.strptime(data.get("fecha_fin"), "%Y-%M-%d").date()
            if len(data.get("fecha_fin")) > 0
            else None
        )
        topico_codigo = int(data.get("topico_id"))

        if not fecha_inicio and not fecha_fin:
            hechos_qs = HechoTopico.objects.filter(topico__codigo=topico_codigo)
        elif fecha_inicio and not fecha_fin:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo=topico_codigo, fecha__fecha_completa__gte=fecha_inicio
            )
        elif not fecha_inicio and fecha_fin:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo=topico_codigo, fecha__fecha_completa__lte=fecha_fin
            )
        else:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo=topico_codigo,
                fecha__fecha_completa__gte=fecha_inicio,
                fecha__fecha_completa__lte=fecha_fin,
            )

        primer_hecho = hechos_qs.order_by("fecha__fecha_completa").first()
        ultimo_hecho = hechos_qs.order_by("fecha__fecha_completa").last()
        primera_fecha = primer_hecho.fecha.fecha_completa if primer_hecho else None
        ultima_fecha = ultimo_hecho.fecha.fecha_completa if ultimo_hecho else None

        num_dias = (
            (ultima_fecha - primera_fecha).days if primera_fecha and ultima_fecha else 0
        )

        parroquias_counts = hechos_qs.values(codigo=F("parroquia__codigo")).annotate(
            total=Sum("total_tweets")
        )
        total = (hechos_qs.aggregate(total=Sum("total_tweets"))).get("total")
        return Response(
            {
                "data": {
                    "parroquias_counts": list(parroquias_counts),
                    "total": total,
                    "num_dias": num_dias,
                }
            }
        )


class GetHechosForDistribution(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        fecha_inicio = (
            datetime.datetime.strptime(data.get("fecha_inicio"), "%Y-%M-%d").date()
            if len(data.get("fecha_inicio")) > 0
            else None
        )
        fecha_fin = (
            datetime.datetime.strptime(data.get("fecha_fin"), "%Y-%M-%d").date()
            if len(data.get("fecha_fin")) > 0
            else None
        )
        topico_codigos = [int(codigo) for codigo in data.get("topicos")]

        if not fecha_inicio and not fecha_fin:
            hechos_qs = HechoTopico.objects.filter(topico__codigo__in=topico_codigos)
        elif fecha_inicio and not fecha_fin:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo__in=topico_codigos,
                fecha__fecha_completa__gte=fecha_inicio,
            )
        elif not fecha_inicio and fecha_fin:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo__in=topico_codigos, fecha__fecha_completa__lte=fecha_fin
            )
        else:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo__in=topico_codigos,
                fecha__fecha_completa__gte=fecha_inicio,
                fecha__fecha_completa__lte=fecha_fin,
            )

        topicos_counts = hechos_qs.values(codigo=F("topico__codigo")).annotate(
            total=Sum("total_tweets")
        )
        total = (hechos_qs.aggregate(total=Sum("total_tweets"))).get("total")

        return Response(
            {
                "data": {
                    "topicos_counts": list(topicos_counts),
                    "total": total,
                }
            }
        )


class GetHechosForAnalitics(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        fecha_inicio = (
            datetime.datetime.strptime(data.get("fecha_inicio"), "%Y-%M-%d").date()
            if len(data.get("fecha_inicio")) > 0
            else None
        )
        fecha_fin = (
            datetime.datetime.strptime(data.get("fecha_fin"), "%Y-%M-%d").date()
            if len(data.get("fecha_fin")) > 0
            else None
        )
        parroquia_codigos = [int(codigo) for codigo in data.get("parroquias")]
        topico_codigos = [int(codigo) for codigo in data.get("topicos")]

        if not fecha_inicio and not fecha_fin:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo__in=topico_codigos,
                parroquia__codigo__in=parroquia_codigos,
            )
        elif fecha_inicio and not fecha_fin:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo__in=topico_codigos,
                parroquia__codigo__in=parroquia_codigos,
                fecha__fecha_completa__gte=fecha_inicio,
            )
        elif not fecha_inicio and fecha_fin:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo__in=topico_codigos,
                parroquia__codigo__in=parroquia_codigos,
                fecha__fecha_completa__lte=fecha_fin,
            )
        else:
            hechos_qs = HechoTopico.objects.filter(
                topico__codigo__in=topico_codigos,
                parroquia__codigo__in=parroquia_codigos,
                fecha__fecha_completa__gte=fecha_inicio,
                fecha__fecha_completa__lte=fecha_fin,
            )
        parroquias_counts = hechos_qs.values(
            parroquia_codigo=F("parroquia__codigo"), topico_codigo=F("topico__codigo")
        ).annotate(total=Sum("total_tweets"))
        parroquias_codigos = set(
            [hecho.get("parroquia_codigo") for hecho in parroquias_counts]
        )
        parroquias_topicos_counts = list()
        for parroquia in parroquias_codigos:
            topicos_codigos = (
                hechos_qs.filter(parroquia__codigo=parroquia)
                .order_by("topico__codigo")
                .values(codigo=F("topico__codigo"))
                .annotate(total=Sum("total_tweets"))
            )
            parroquias_topicos_counts.append(
                {"codigo": parroquia, "topicos": list(topicos_codigos)}
            )

        return Response(
            {"data": {"parroquias_topicos_counts": parroquias_topicos_counts}}
        )


class GetHechosForComparative(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        fecha_inicio = (
            datetime.datetime.strptime(data.get("fecha_inicio"), "%Y-%m-%d").date()
            if len(data.get("fecha_inicio")) > 0
            else None
        )
        parroquia_codigo = int(data.get("selected_parroquia"))
        topico_codigo = int(data.get("selected_topico"))
        meses = int(data.get("meses"))
        
        fecha_top = fecha_inicio + datetime.timedelta(days=meses * 4 * 7)
        fecha_bottom = fecha_inicio - datetime.timedelta(days=meses * 4 * 7 - 1)

        hechos_qs = HechoTopico.objects.filter(
            topico__codigo=topico_codigo,
            parroquia__codigo=parroquia_codigo,
            fecha__fecha_completa__gte=fecha_bottom,
            fecha__fecha_completa__lte=fecha_top,
        )

        hechos_antes = hechos_qs.filter(fecha__fecha_completa__lte=fecha_inicio)
        hechos_despues = hechos_qs.filter(fecha__fecha_completa__gt=fecha_inicio)

        semanas_counts_antes = list()
        semanas_counts_despues = list()

        while True:
            fechas = [fecha_bottom, fecha_bottom + datetime.timedelta(days=6)]
            fecha_bottom += datetime.timedelta(days=7)
            total = hechos_qs.filter(
                fecha__fecha_completa__gte=fechas[0],
                fecha__fecha_completa__lte=fechas[1],
            ).aggregate(total=Sum("total_tweets"))
            if fechas[1] <= fecha_inicio:
                semanas_counts_antes.append(
                    total if total.get("total") else {"total": 0}
                )
            else:
                semanas_counts_despues.append(
                    total if total.get("total") else {"total": 0}
                )
            if fecha_bottom > fecha_top:
                break
        
        total_antes = hechos_antes.aggregate(total=Sum("total_tweets"))
        total_despues = hechos_despues.aggregate(total=Sum("total_tweets"))
        
        return Response(
            {
                "data": {
                    "totales_antes": semanas_counts_antes,
                    "totales_despues": semanas_counts_despues,
                    "total_antes": total_antes.get('total') if total_antes.get('total') else 0,
                    "total_despues": total_despues.get('total') if total_antes.get('total') else 0,
                }
            }
        )

class FileUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get('file')
        tipo = request.data.get('type')

        if not file or not tipo:
            return Response({'error': 'Faltan campos requeridos: archivo o tipo'}, status=HTTP_400_BAD_REQUEST)

        if tipo not in dict(Archivo.TIPOS).keys():
            return Response({'error': 'Tipo de archivo no válido'}, status=HTTP_400_BAD_REQUEST)

        archivo = Archivo(
            usuario_creacion=request.user,
            archivo=file,
            tipo=tipo,
            usuario_carga=request.user,
            fecha_carga=now(),
        )

        archivo.save()

        return Response({'message': 'Archivo subido exitosamente'}, status=HTTP_201_CREATED)