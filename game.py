"""
Βασική δομή παιχνιδιού CYBER RUNNER
Περιλαμβάνει την αρχικοποίηση του παραθύρου, τη δημιουργία αντικειμένων παίκτη, εχθρών,
σφαιρών και power-ups, καθώς και την κύρια λούπα του παιχνιδιού για την επεξεργασία εισόδου,
την ενημέρωση της κατάστασης των αντικειμένων και τη σχεδίαση τους.

"""
import pygame
import random
from ui import Button

# Εισαγωγή κλάσεων 
from player import Player
from enemy import Enemy
from powerups import PowerUp
from enemyWave import EnemyWave

# Αρχικοποίηση της βιβλιοθήκης Pygame
pygame.init()

# Ορισμός καταστάσεων παιχνιδιού
MENU = 0
GAME_ONE_player1 = 1
GAME_TWO_player1 = 2
PAUSE = 3
HISHSCORES = 4
GAMEOVER = 5

current_state = MENU
sound_on = True 

# Ορισμός χρωμάτων
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUSSIAN_VIOLET = (52, 27, 95)
HOLLYWOOD_CERISE = (236, 19, 164)
AUREOLIN = (245, 230, 18)
ELECTRIC_INDIGO = (99, 57, 235)
SKY_BLUE = (94, 217, 242)

# Ρυθμίσεις παραθύρου
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER RUNNER")
backgrpund_img = pygame.image.load("background.jpg").convert()

# Ρυθμίσεις ρολογιού
clock = pygame.time.Clock() 

# Ρυθμίσεις γραμματοσειράς 
FONT_LARGE = pygame.font.Font("BlockCraftMedium-PVLzd.otf", 72)
FONT_MEDIUM = pygame.font.Font("BlockCraftMedium-PVLzd.otf", 46)
FONT_SMALL = pygame.font.Font("BlockCraftMedium-PVLzd.otf", 24) 

# Δημιουργία κουμπίων για το μενού
btn_w = 200
btn_h = 50
center_x = SCREEN_WIDTH // 2 - btn_w // 2

menu_buttons =  [
    Button(center_x, 250, btn_w, btn_h, "NEW GAME - ONE player", FONT_SMALL, ELECTRIC_INDIGO, WHITE),
    Button(center_x, 320, btn_w, btn_h, "NEW GAME - TWO player", FONT_SMALL, ELECTRIC_INDIGO, WHITE),
    Button(center_x, 390, btn_w, btn_h,"HIGHSCORES", FONT_SMALL, ELECTRIC_INDIGO, WHITE),
    Button(center_x, 460, btn_w, btn_h, "EXIT", FONT_SMALL, ELECTRIC_INDIGO, WHITE),
    ]

# Δημιουργία groups για τα sprites 
player1_bullets_group = pygame.sprite.Group()
enemy_bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

# Αρχικοποιήση αντικειμένου παίκτη
player1 = Player(SCREEN_WIDTH, SCREEN_HEIGHT, 40, 40 , SKY_BLUE, 5)
#player2 = Player(SCREEN_WIDTH, SCREEN_HEIGHT, 40, 40 , AUREOLIN, 5)

# Δημιουργία του wave manager
wave_manager = EnemyWave(SCREEN_WIDTH, SCREEN_HEIGHT, enemies_group, enemy_bullets_group, player1_bullets_group, player1)
wave_manager.new_enemy_wave() # Δημιουργία νέου κύματος εχθρών

game_over = False

# ------------------------------------
# --------- GAME MAIN LOOP -----------
# ------------------------------------
done = False
while not done:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
          if event.type == pygame.QUIT:
            done = True


    if current_state == MENU:
        for i,button in enumerate(menu_buttons):
            if button.is_clicked(event):
                if i == 0:  # NEW GAME - ONE player1
                    current_state = GAME_ONE_player1
                elif i == 1:  # NEW GAME - TWO player1
                    # Λογική για νέο παιχνίδι δύο παικτών (αν υποστηρίζεται)
                    current_state = GAME_TWO_player1
                elif i == 2:  # HIGHSCORES
                    current_state = HISHSCORES
                elif i == 3:  # EXIT
                    done = True
            
        screen.fill(BLACK)
        title_text = FONT_LARGE.render("CYBER RUNNER", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        for button in menu_buttons:
            button.draw(screen)

    elif current_state == GAME_ONE_player1:
    # Επεξεργασία εισόδου χρήστη
        if not game_over:
            player1.import_handler(SCREEN_WIDTH, player1_bullets_group)
        
            #----- UPDATES -----
            if not game_over:
                player1_bullets_group.update() # Ενημέρωση όλων των σφαιρών του παίκτη
                enemy_bullets_group.update() # Ενημέρωση όλων των σφαιρών των εχθρών
                enemies_group.update() # Ενημέρωση όλων των εχθρών 
                wave_manager.update() # Ενημέρωση του wave manager
        
            #----- Collisions ----- 
            hits = pygame.sprite.groupcollide(enemies_group, player1_bullets_group, False, True)
            for enemy, bullets in hits.items():
                enemy.take_damage(damage=len(bullets))
            
            if pygame.sprite.spritecollideany(player1, enemy_bullets_group):
                player1.take_damage(damage=wave_manager.enemy_damage)
                # Λογική για αφαίρεση της σφαίρας που χτύπησε τον παίκτη
                collided_bullets = pygame.sprite.spritecollide(player1, enemy_bullets_group, True)
            
            if player1.health <= 0:
                print("GAME OVER!")
                game_over = True
                current_state = GAMEOVER
                
            
        # ----- ΣΧΕΔΙΑΣΗ -----
        screen.blit(backgrpund_img, (0, 0))  # Σχεδίαση φόντου
        player1.draw(screen) # Σχεδίαση παίκτη

        score_text = FONT_MEDIUM.render(f"{player1.score}", True, HOLLYWOOD_CERISE)
        screen.blit(score_text, (10, 10)) # Σχεδίαση score παίκτη

        health_text = FONT_MEDIUM.render(f"{player1.health}", True, RUSSIAN_VIOLET)
        screen.blit(health_text, (SCREEN_WIDTH - 30 , 10)) # Σχεδίαση ζωής παίκτη

        enemies_group.draw(screen) # Σχεδίαση εχθρών
        player1_bullets_group.draw(screen) # Σχεδίαση σφαιρών παίκτη
        enemy_bullets_group.draw(screen) # Σχεδίαση σφαιρών εχθρών
    

    elif current_state == GAME_TWO_player1:
        pass # Λογική για το παιχνίδι δύο παικτών 

    elif current_state == GAMEOVER:
        #screen.fill(BLACK)
        game_over_text = FONT_LARGE.render("GAME OVER", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    # Ενημέρωση της οθόνης
    pygame.display.flip()
    clock.tick(60)

