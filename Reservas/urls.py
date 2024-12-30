from django.urls import path
from . import api

urlpatterns = [
    path('agendasala', api.agendasala_list.as_view()),
    path('agendasala/<int:pk>', api.agendasala_detail.as_view()),
    path('agendasala_quadro', api.agendasala_quadro),
    path('lastick/<str:resource>', api.lastick),
]