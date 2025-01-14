from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('topicos/', views.GetTopicos.as_view(), name='topicos'),
    path('parroquias/', views.GetParroquias.as_view(), name='parroquias'),
    path('hechos_map/', views.GetHechosForMap.as_view(), name='hechos_map'),
    path('hechos_distribucion/', views.GetHechosForDistribution.as_view(), name='hechos_distribucion'),
    path('hechos_analitica/', views.GetHechosForAnalitics.as_view(), name='hechos_analitics'),
    path('hechos_comparativa/', views.GetHechosForComparative.as_view(), name='hechos_comparative'),
]