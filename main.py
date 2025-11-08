import pygame
import sys
import time
from constants import *
from game import Game

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guitar Hero")
clock = pygame.time.Clock()

# --- Fonts ---
font = pygame.font.SysFont("Impact", 30)
big_font = pygame.font.SysFont("Impact", 40)
title_font = pygame.font.SysFont("Impact", 50)

# --- Game object ---
game = Game()

# --- Notes chart example ---
note_chart = [
    {"time": 1.0, "key": "R"},
    {"time": 1.5, "key": "G"},
    {"time": 2.0, "key": "B"},
    {"time": 2.5, "key": "Y"},
    {"time": 3.0, "key": "P"},
    {"time": 3.5, "key": "R"},
    {"time": 4.0, "key": "G"},
]
game.load_notes(note_chart)

# --- Game states ---
STATE_START = "start_screen"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "end_screen"
game_state = STATE_START
hit_feedback = ""
feedback_timer = 0
feedback_x = 0  # where the feedback should appear

# --- Draw start screen ---
def draw_start_screen():
    screen.fill(BLACK)
    title = title_font.render("Guitar Hero", True, WHITE)
    song = big_font.render("Eye of the Tiger", True, WHITE)
    info = font.render("Press ENTER to Start", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(song, (SCREEN_WIDTH//2 - song.get_width()//2, SCREEN_HEIGHT//2 - 40))
    screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT//2 + 40))

# --- Draw hollow hit zones (only during gameplay) ---
def draw_hit_zone():
    lane_positions = [SCREEN_WIDTH//2 - 120 + i*60 for i in range(5)]  # 5 lanes closer together & centered
    for lane_index, x in enumerate(lane_positions):
        pygame.draw.circle(
            screen,
            LANE_COLORS[lane_index],
            (x, HIT_Y),
            NOTE_RADIUS,
            4  # thickness makes it hollow
        )
        # Update lane X for notes
        LANE_X[lane_index] = x

# --- Draw end screen ---
def draw_end_screen():
    screen.fill(BLACK)
    title = title_font.render("Song Complete!", True, WHITE)
    score_text = big_font.render(f"Score: {game.score}", True, WHITE)
    combo_text = font.render(f"Max Combo: {game.max_combo}", True, WHITE)
    hits_text = font.render(f"Total Hits: {game.total_hits}", True, WHITE)
    misses_text = font.render(f"Total Misses: {game.total_misses}", True, WHITE)
    restart_text = font.render("Press ENTER to Restart", True, WHITE)

    # Center all texts
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 200))
    screen.blit(combo_text, (SCREEN_WIDTH//2 - combo_text.get_width()//2, 280))
    screen.blit(hits_text, (SCREEN_WIDTH//2 - hits_text.get_width()//2, 320))
    screen.blit(misses_text, (SCREEN_WIDTH//2 - misses_text.get_width()//2, 360))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 480))

# --- Main loop ---
running = True
while running:
    delta_time = clock.tick(FPS) / 1000

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_state == STATE_START and event.key == pygame.K_RETURN:
                game.start()
                game_state = STATE_PLAYING

            elif game_state == STATE_PLAYING:
                if event.key == pygame.K_p:
                    game.toggle_pause()
                else:
                    result = game.handle_input(event.unicode)
                    if result:
                        hit_feedback = result
                        feedback_timer = 0.5
                        # Show feedback above the corresponding lane
                        for note in game.active_notes:
                            if note.hit and KEY_MAPPING[note.lane_index] == event.unicode:
                                feedback_x = LANE_X[note.lane_index]

            elif game_state == STATE_GAME_OVER and event.key == pygame.K_RETURN:
                # Reset game for restart
                game.notes.clear()
                game.active_notes.clear()
                game.particles.clear()
                game.score = 0
                game.combo = 0
                game.max_combo = 0
                game.total_hits = 0
                game.total_misses = 0
                game.load_notes(note_chart)
                game.start()
                hit_feedback = ""
                feedback_timer = 0
                game_state = STATE_PLAYING

    # --- Update game ---
    if game_state == STATE_PLAYING:
        game.update()
        if all(note.hit for note in game.notes):
            game_state = STATE_GAME_OVER

    # --- Draw ---
    screen.fill(BLACK)

    if game_state == STATE_START:
        draw_start_screen()
    elif game_state == STATE_PLAYING:
        draw_hit_zone()
        game.draw(screen)
    elif game_state == STATE_GAME_OVER:
        draw_end_screen()  # no hit zones here

    # --- Scoreboard ---
    if game_state == STATE_PLAYING:
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        combo_text = font.render(f"Combo: {game.combo}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(combo_text, (10, 50))

    # --- Feedback ---
    if feedback_timer > 0:
        feedback_surface = big_font.render(hit_feedback, True, WHITE)
        screen.blit(feedback_surface, (feedback_x - feedback_surface.get_width()//2, HIT_Y - 80))
        feedback_timer -= delta_time

    pygame.display.flip()

pygame.quit()
sys.exit()
