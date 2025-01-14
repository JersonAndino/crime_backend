from django.db import models
from collections import OrderedDict
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Fecha(models.Model):
    fecha_completa = models.DateField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    semana = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Fecha'
        verbose_name_plural = 'Fechas'

    def __str__(self):
        return str(self.fecha_completa)
    
    @staticmethod
    def get_ultima_fecha():
        ultima_fecha = Fecha.objects.all().order_by('id').last()
        return ultima_fecha
    
class Topico(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField()
    descripcion = models.TextField()
    
    class Meta:
        verbose_name = 'Topico'
        verbose_name_plural = 'Topicos'

    def __str__(self):
        return self.nombre
    
class Parroquia(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField()
    descripcion = models.TextField()
    
    class Meta:
        verbose_name = 'Parroquia'
        verbose_name_plural = 'Parroquias'

    def __str__(self):
        return self.nombre
    
class HechoTopico(models.Model):
    fecha = models.ForeignKey('Fecha', on_delete=models.CASCADE, blank=True, null=True)
    topico = models.ForeignKey('Topico', on_delete=models.CASCADE, blank=True, null=True)
    parroquia = models.ForeignKey('Parroquia', on_delete=models.CASCADE, blank=True, null=True)
    total_tweets = models.IntegerField()
    
    class Meta:
        verbose_name = 'Hecho'
        verbose_name_plural = 'Hechos'

    def __str__(self):
        return str(self.total_tweets)

class AuditMixin(models.Model):
    usuario_creacion = models.ForeignKey(User, null=True, blank=True,related_name='%(class)s_usuario_creacion',
                                         help_text='Usuario que crea el registro', on_delete=models.CASCADE)
    usuario_modificacion = models.ForeignKey(User, null=True, blank=True,related_name='%(class)s_usuario_modificacion',
                                             help_text='Usuario que modifica el registro', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(editable=True, default=now,
                                          blank=True, null=True,
                                          help_text='Fecha cuando se crea el registro')
    fecha_modificacion = models.DateTimeField(default=now, blank=True,
                                              help_text='Fecha cuando se modifica el registro')


    def save(self, *args, **kwargs):
        if self.pk is None:
            self.fecha_creacion = now()
        else:
            self.fecha_modificacion = now()
        return super(AuditMixin, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(AuditMixin, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

class Archivo(AuditMixin):
    TOPICO = 'TOPICO'
    PARROQUIA = 'PARROQUIA'
    HECHO = 'HECHO'
    DATA = 'DATA'

    TIPOS=OrderedDict((
        (TOPICO,'Topicos'),
        (PARROQUIA, 'Parroquias'),
        (HECHO, 'Hechos'),
        (DATA, 'Data Recolectada'),
    ))
    
    archivo = models.FileField('Archivo', max_length=128,
                               upload_to='media',
                               null=True, blank=True)
    tipo = models.CharField(max_length=20, blank=False, null=False, choices=TIPOS.items(), default=HECHO)
    cargado = models.BooleanField(null=True, blank=True, default=False)
    usuario_carga = models.ForeignKey(User, null=True, blank=True,related_name='%(class)s_usuario_carga',
                                         help_text='Usuario que cargo este archivo a la base de datos', on_delete=models.CASCADE)
    fecha_carga = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

    def __str__(self):
        return self.tipo
    
class RegistroActualizacion(AuditMixin):
    archivo = models.ForeignKey('Archivo', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Actualizacion'
        verbose_name_plural = 'Actualizaciones'

    def __str__(self):
        return self.fecha_creacion
    