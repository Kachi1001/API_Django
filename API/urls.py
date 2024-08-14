from django.urls import path
from . import views
from . import teste

urlpatterns = [
    path('executar_funcao_geraViewJunta', views.executar_funcao_geraViewJunta, name='executar_funcao_geraViewJunta'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('salas', views.salas, name='API_salas'),
    path('get_table', views.get_table, name='get_table'),
    path('get_data', views.get_data, name='get_data'),
    path('deletar', views.deletar, name='deletar'),
    path('update-supervisor-status/', views.update_supervisor_status, name='update_supervisor_status'),
    
    path('update', views.update, name='update'),

    path('upload/', views.upload_file, name='upload_file'),
    
    path('teste', teste, name='testes')
]