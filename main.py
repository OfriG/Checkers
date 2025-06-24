# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60

pygame.init()  # Initialize pygame
pygame.font.init()  # Initialize font module

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def draw_winner(win, color):
    font = pygame.font.SysFont(None, 72)
    text = f"{'RED' if color == RED else 'WHITE'} WINS!"
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    win.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)  # Display message for 3 seconds

def draw_message(win, message):
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT - 30))
    # Clear previous area
    pygame.draw.rect(win, (0, 0, 0), (0, HEIGHT - 60, WIDTH, 60))
    win.blit(text_surface, text_rect)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, WHITE, game)
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                
                # Check if it's right click (Boost) or middle click (Twice)
                use_boost = event.button == 3
                use_twice = event.button == 2  # Middle click for Twice
                
                if game.turn == RED:
                    if use_boost and game.boost_used[RED]:
                        draw_message(WIN, "You already used your Boost!")
                    elif use_twice and game.twice_used[RED]:
                        draw_message(WIN, "You already used your Twice!")
                    else:
                        game.select(row, col, use_boost, use_twice)

        game.update()
        
        # Game messages
        if game.boost_just_used[RED]:
            draw_message(WIN, "Boost used!")
        elif game.boost_just_used[WHITE]:
            draw_message(WIN, "AI used Boost!")
        elif game.twice_pending[RED]:
            draw_message(WIN, "You get another turn (Twice)!")
        elif game.twice_pending[WHITE]:
            draw_message(WIN, "AI gets another turn (Twice)!")
        elif game.just_got_king:
            draw_message(WIN, "King crowned!")
        
        # Check winner
        winner = game.winner()
        if winner is not None:
            draw_winner(WIN, winner)
            run = False

    pygame.quit()

main()