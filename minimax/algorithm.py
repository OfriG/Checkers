from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

def minimax(position, depth, max_player, game,
            boost_available={"RED": True, "WHITE": True},
            alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(boost_available), position

    color = WHITE if max_player else RED
    boost = boost_available["WHITE"] if max_player else boost_available["RED"]

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game, boost):
            new_boost = boost_available.copy()
            if boost:
                new_boost["WHITE"] = False

            evaluation = minimax(move, depth-1, False, game, new_boost, alpha, beta)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game, boost):
            new_boost = boost_available.copy()
            if boost:
                new_boost["RED"] = False

            evaluation = minimax(move, depth-1, True, game, new_boost, alpha, beta)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game, boost_available=True, twice_available=False):
    moves = []
    for piece in board.get_all_pieces(color):
        # Regular moves
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            # If got king in this move, can use Twice
            just_got_king = not temp_piece.king and (move[0] == 0 or move[0] == board.board.__len__() - 1)
            if twice_available or just_got_king:
                # Extra turn
                for piece2 in new_board.get_all_pieces(color):
                    valid_moves2 = new_board.get_valid_moves(piece2)
                    for move2, skip2 in valid_moves2.items():
                        temp_board2 = deepcopy(new_board)
                        temp_piece2 = temp_board2.get_piece(piece2.row, piece2.col)
                        new_board2 = simulate_move(temp_piece2, move2, temp_board2, game, skip2)
                        moves.append(new_board2)
            else:
                moves.append(new_board)
        # Boost move (if allowed)
        if boost_available:
            boost_moves = board.get_valid_moves(piece, allow_boost=True)
            for move, skip in boost_moves.items():
                if move not in valid_moves:  # Only real Boost moves
                    temp_board = deepcopy(board)
                    temp_piece = temp_board.get_piece(piece.row, piece.col)
                    new_board = simulate_move(temp_piece, move, temp_board, game, skip)
                    moves.append(new_board)
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)

