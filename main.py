import pygame
import random
from word import word_list

pygame.init()

WIDTH = 600
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont('arial', 48, bold=True)
SMALL_FONT = pygame.font.SysFont('arial', 28)

def draw_hangman(win, status):
    pole_thickness = 8  
    base_x = WIDTH // 2 - 100  
    base_y = 460

    pygame.draw.line(win, BLACK, (base_x, base_y), (base_x + 200, base_y), pole_thickness)
    pygame.draw.line(win, BLACK, (base_x + 100, base_y), (base_x + 100, 150), pole_thickness)
    pygame.draw.line(win, BLACK, (base_x + 100, 150), (base_x + 200, 150), pole_thickness)
    pygame.draw.line(win, BLACK, (base_x + 200, 150), (base_x + 200, 180), pole_thickness)

    if status > 0:  
        pygame.draw.circle(win, BLACK, (base_x + 200, 210), 25, pole_thickness)
    if status > 1:  
        pygame.draw.line(win, BLACK, (base_x + 200, 235), (base_x + 200, 320), pole_thickness)
    if status > 2:  
        pygame.draw.line(win, BLACK, (base_x + 200, 250), (base_x + 160, 280), pole_thickness)
    if status > 3:  
        pygame.draw.line(win, BLACK, (base_x + 200, 250), (base_x + 240, 280), pole_thickness)
    if status > 4:  
        pygame.draw.line(win, BLACK, (base_x + 200, 320), (base_x + 175, 370), pole_thickness)
    if status > 5:  
        pygame.draw.line(win, BLACK, (base_x + 200, 320), (base_x + 225, 370), pole_thickness)

def draw_window(word, guessed, hangman_status):
    win.fill(WHITE)
    draw_hangman(win, hangman_status)

    display_word = ""
    for letter in word:
        display_word += letter + " " if letter in guessed else "_ "
    text = FONT.render(display_word.strip(), True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, 540))
    win.blit(text, text_rect)

    pygame.display.update()

def show_message(message):
    win.fill(WHITE)
    text = FONT.render(message, True, BLACK)
    retry_text = SMALL_FONT.render("Press R to retry or Q to quit", True, BLACK)

    win.blit(text, text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 20)))
    win.blit(retry_text, retry_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 40)))
    pygame.display.update()

def main():
    word = random.choice(word_list).upper()
    guessed = []
    hangman_status = 0
    MAX_TRIES = 6
    run = True
    game_over = False

    while run:
        if not game_over:
            draw_window(word, guessed, hangman_status)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    letter = event.unicode.upper()
                    if letter.isalpha() and letter not in guessed:
                        guessed.append(letter)
                        if letter not in word:
                            hangman_status += 1
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()  # restart game
                        return
                    elif event.key == pygame.K_q:
                        run = False

        if not game_over:
            won = all(letter in guessed for letter in word)
            if won:
                show_message("You Won!")
                game_over = True
            elif hangman_status == MAX_TRIES:
                show_message(f"You Lost! Word: {word}")
                game_over = True

    pygame.quit()


if __name__ == "__main__":
    main()
