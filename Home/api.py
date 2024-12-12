from Site_django import util
from . import models, serializers
  
class pendencia_detail(util.RUD):
    queryset = models.Pendencia.objects.all()
    serializer_class = serializers.Pendencia
  