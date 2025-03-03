from django.urls import path
from . import api

urlpatterns = [
    path('menu', api.Menu_list.as_view()),
    path('menu/<str:pk>', api.Menu_detail.as_view()),

    path('submenu', api.Submenu_list.as_view()),
    path('submenu/<str:pk>', api.Submenu_detail.as_view()),

    path('app', api.App_list.as_view()),
    path('app/<str:pk>', api.App_detail.as_view()),
    
    path('tabela/<str:table>', api.tabela),
    path('resource/<str:name>', api.resource),
    path('select/<str:resource>', api.select),
    
]