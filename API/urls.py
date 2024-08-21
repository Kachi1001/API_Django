from django.urls import path
from Lancamento_obra import view as Lancamento_obra
from Reservas import view as Reservas
from media import view as media

urlpatterns = [
    path('executar_funcao_geraViewJunta', Lancamento_obra.executar_funcao_geraViewJunta, name='executar_funcao_geraViewJunta'),
    path('tabela/<str:table>', Lancamento_obra.tabela, name='tabela'),
    path('cadastrar', Lancamento_obra.cadastrar, name='cadastrar'),
    path('get_table', Lancamento_obra .get_table, name='get_table'),
    path('get_data', Lancamento_obra.get_data, name='get_data'),
    path('deletar', Lancamento_obra.deletar, name='deletar'),
    path('update-supervisor-status/', Lancamento_obra.update_supervisor_status, name='update_supervisor_status'),
    path('update', Lancamento_obra.update, name='update'),

    path('upload/', media.upload_file, name='upload_file'),
    
    path('salas', Reservas.salas, name='API_salas'),
]