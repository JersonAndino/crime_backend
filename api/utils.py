import pandas as pd
import traceback
from api.models import (
    Fecha, 
    Topico,
    Parroquia,
    HechoTopico
)

def process_row_topico(row):
    return Topico(codigo = row['codigo'], nombre = row['nombre'], descripcion = row['descripcion'])

def process_row_parroquia(row):
    return Parroquia(codigo = row['codigo'], nombre = row['nombre'])

def process_row_hecho(row, fechas, parroquias, topicos):
    fecha = fechas.get(str(row['fecha']))
    fecha_key = str(row['fecha'])
    parroquia = parroquias.get(row['parroquia'])
    topico = topicos.get(row['topico'])
    return HechoTopico(fecha = fecha, parroquia = parroquia, topico = topico, total_tweets = row['total'])

def load_data_desde_csv(path, model):
    try:
        df = pd.read_csv(path, header=None)
        if model == Topico:
            df.columns = ['codigo', 'nombre', 'descripcion']
            create = df.apply(process_row_topico, axis=1).to_list()
            Topico.objects.bulk_create(create)
        elif model == Parroquia:
            df.columns = ['codigo', 'nombre']
            create = df.apply(process_row_parroquia, axis=1).to_list()
            Parroquia.objects.bulk_create(create)
        elif model == HechoTopico:
            df.columns = ['fecha', 'topico', 'parroquia', 'total']
            fechas = {'{}{}{}'.format(fecha.fecha_completa.year, fecha.fecha_completa.month if fecha.fecha_completa.month > 9 else f'0{fecha.fecha_completa.month}', fecha.fecha_completa.day if fecha.fecha_completa.day > 9 else f'0{fecha.fecha_completa.day}'): fecha for fecha in Fecha.objects.all()}
            parroquias = {parroquia.codigo: parroquia for parroquia in Parroquia.objects.all()}
            topicos = {topico.codigo: topico for topico in Topico.objects.all()}
            create = df.apply(process_row_hecho, axis=1, args=(fechas, parroquias, topicos)).to_list()
            HechoTopico.objects.bulk_create(create)
        return True
    except Exception as e:
        traceback.print_exc()
        return False
    