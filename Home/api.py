import json
import redis
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Configuração do Redis
redis_client = redis.StrictRedis(host="10.0.0.139", port=6379, db=0, decode_responses=True)

# Nome do jogo no Redis
GAME_KEY = "jogo_da_velha"

# Inicializa o estado de um jogo
def initialize_game(game_id):
    board = ["-"] * 9  # Tabuleiro vazio
    turn = "X"         # Jogador X começa
    redis_client.hmset(f"game_{game_id}", {"board": json.dumps(board), "turn": turn, "winner": ""})

# Busca o estado de um jogo específico
def get_game(game_id):
    game_data = redis_client.hgetall(f"game_{game_id}")
    if not game_data:
        initialize_game(game_id)  # Inicializa o jogo se não existir
        game_data = redis_client.hgetall(f"game_{game_id}")
    game_data["board"] = json.loads(game_data["board"])
    return game_data

# Atualiza as funções para usar game_id
@csrf_exempt
def make_move(request, game_id):
    if request.method == "POST":
        data = json.loads(request.body)
        player = data.get("player")
        position = data.get("position")

        # Busca o estado do jogo
        game = get_game(game_id)
        board = game["board"]
        turn = game["turn"]
        winner = game["winner"]

        # Validações
        if winner:
            
            return JsonResponse({"error": f"O jogo já acabou! Vencedor: {winner}"}, status=400)
        if turn != player:
            return JsonResponse({"error": "Não é a vez desse jogador!"}, status=400)
        if board[position] != "-":
            return JsonResponse({"error": "Posição já ocupada!"}, status=400)

        # Atualiza o tabuleiro
        board[position] = player
        winner = check_winner(board)
        # Atualiza o turno e salva no Redis
        turn = "O" if turn == "X" else "X"
        redis_client.hmset(f"game_{game_id}", {"board": json.dumps(board), "turn": turn, "winner": winner})

        return JsonResponse({"board": board, "turn": turn, "winner": winner})

    return JsonResponse({"error": "Método não permitido"}, status=405)

@csrf_exempt
def reset_game(request, game_id):
    if request.method == "POST":
        initialize_game(game_id)
        return JsonResponse({"message": f"Jogo {game_id} reiniciado com sucesso!"})

    return JsonResponse({"error": "Método não permitido"}, status=405)

def get_game_state(request, game_id):
    game = get_game(game_id)
    return JsonResponse(game)

def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6],             # Diagonais
    ]
    for combo in winning_combinations:
        if board[combo[0]] != "-" and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            print(board[combo[0]])
            return board[combo[0]]  # Retorna o vencedor (X ou O)
    if "-" not in board:
        return "Empate"
    return ""