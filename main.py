import pygame
import random
import word

pygame.init()
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 170, 0)
GRAY = (160, 160, 160)
WORD_FONT = pygame.font.SysFont(None, 60)
MSG_FONT = pygame.font.SysFont(None, 40)
SMALL_FONT = pygame.font.SysFont(None, 28)
word_to_guess = random.choice(word.words).upper()
guessed = []
hangman_status = 0
max_wrong = 6
game_over = False
message = ""

def draw_hangman(win, status):
    t = 5
    base_y = HEIGHT // 2 + 130
    cx = WIDTH // 2
    pygame.draw.line(win, BLACK, (cx - 100, base_y), (cx + 100, base_y), t)
    pygame.draw.line(win, BLACK, (cx - 80, base_y), (cx - 80, base_y - 300), t)
    pygame.draw.line(win, BLACK, (cx - 80, base_y - 300), (cx + 60, base_y - 300), t)
    pygame.draw.line(win, BLACK, (cx + 60, base_y - 300), (cx + 60, base_y - 250), t)
    if status > 0:
        pygame.draw.circle(win, BLACK, (cx + 60, base_y - 230), 20, t)
    if status > 1:
        pygame.draw.line(win, BLACK, (cx + 60, base_y - 210), (cx + 60, base_y - 130), t)
    if status > 2:
        pygame.draw.line(win, BLACK, (cx + 60, base_y - 190), (cx + 30, base_y - 160), t)
    if status > 3:
        pygame.draw.line(win, BLACK, (cx + 60, base_y - 190), (cx + 90, base_y - 160), t)
    if status > 4:
        pygame.draw.line(win, BLACK, (cx + 60, base_y - 130), (cx + 30, base_y - 90), t)
    if status > 5:
        pygame.draw.line(win, BLACK, (cx + 60, base_y - 130), (cx + 90, base_y - 90), t)

def display_word():
    disp = ""
    for l in word_to_guess:
        disp += l + " " if l in guessed else "_ "
    text = WORD_FONT.render(disp.strip(), True, BLACK)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 120))
    win.blit(text, rect)

def draw_stats():
    correct = sum([1 for l in word_to_guess if l in guessed])
    wrong = hangman_status
    stats = SMALL_FONT.render(f"Correct: {correct} | Wrong: {wrong}", True, BLACK)
    win.blit(stats, (20, 20))

def draw_letters():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cols = 13
    start_x = 40
    start_y = HEIGHT - 80
    gap = 40
    for i, letter in enumerate(alphabet):
        color = GREEN if letter in guessed and letter in word_to_guess else RED if letter in guessed else BLACK
        text = SMALL_FONT.render(letter, True, color)
        row = i // cols
        col = i % cols
        x = start_x + col * gap
        y = start_y + row * 35
        win.blit(text, (x, y))

def show_message(msg, color=BLACK, y_offset=0):
    text = MSG_FONT.render(msg, True, color)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    win.blit(text, rect)

def show_retry_quit():
    text = SMALL_FONT.render("Press R to Retry    ESC to Quit", True, BLACK)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    win.blit(text, rect)

def reset_game():
    global word_to_guess, guessed, hangman_status, game_over, message
    word_to_guess = random.choice(word.words).upper()
    guessed = []
    hangman_status = 0
    game_over = False
    message = ""

def redraw_game():
    win.fill(WHITE)
    draw_hangman(win, hangman_status)
    display_word()
    draw_letters()
    draw_stats()
    if not game_over:
        footer = SMALL_FONT.render(" ", True, BLACK)
        rect = footer.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        win.blit(footer, rect)
    if game_over:
        # Create blurred background
        temp = win.copy()
        w, h = temp.get_size()
        small = pygame.transform.smoothscale(temp, (w//8, h//8))
        blurred = pygame.transform.smoothscale(small, (w, h))
        win.fill(WHITE)  # clear
        win.blit(blurred, (0,0))
        # Draw overlays
        color = GREEN if message == "You Win!" else RED
        show_message(message, color, -20)
        show_retry_quit()
    pygame.display.update()

run = True
clock = pygame.time.Clock()
while run:
    clock.tick(60)
    redraw_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
            else:
                if event.unicode.isalpha():
                    l = event.unicode.upper()
                    if l not in guessed:
                        guessed.append(l)
                        if l not in word_to_guess:
                            hangman_status += 1
                            if hangman_status >= max_wrong:
                                message = f"You Lose! Word: {word_to_guess}"
                                game_over = True
                        elif all(c in guessed for c in word_to_guess):
                            message = "You Win!"
                            game_over = True
pygame.quit()
