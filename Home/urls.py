from django.urls import path
from . import api 

urlpatterns = [
    path("make_move/<str:game_id>/", api.make_move),
    path("get_game_state/<str:game_id>/", api.get_game_state),
    path("reset_game/<str:game_id>/", api.reset_game),
]