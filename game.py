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
pygame.mixer.init()

# Ορισμός καταστάσεων παιχνιδιού
MENU = 0
GAME = 1
PAUSE = 2
HISHSCORES = 3
GAMEOVER = 4

current_state = MENU # Αρχική κατάσταση παιχνιδιού
sound_on = True #?

# Ορισμός mode παιχνιδιού
ONE_PLAYER = 0
TWO_PLAYERS = 1
game_mode = ONE_PLAYER

# Ορισμός χρωμάτων
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUSSIAN_VIOLET = (52, 27, 95)
HOLLYWOOD_CERISE = (236, 19, 164)
AUREOLIN = (245, 230, 18)
ELECTRIC_INDIGO = (99, 57, 235)
SKY_BLUE = (94, 217, 242)

# Ρυθμίσεις παραθύρου
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER RUNNER")
backgrpund_img = pygame.image.load("background.jpg").convert()

# Ρυθμίσεις ρολογιού
clock = pygame.time.Clock() 

# Ρυθμίσεις γραμματοσειράς 
FONT_LARGE = pygame.font.Font("BlockCraftMedium-PVLzd.otf", 72)
FONT_MEDIUM = pygame.font.Font("BlockCraftMedium-PVLzd.otf", 46)
FONT_SMALL = pygame.font.Font("BlockCraftMedium-PVLzd.otf", 24) 

# Ρυθμίσεις κουμπιών για το μενού
btn_w = 300
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
player2_bullets_group = pygame.sprite.Group()
enemy_bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

# Αρχικοποιήση αντικειμένων παίκτη
player1 = None
player2 = None

# Ρυθμίσεις backgound ήχου
pygame.mixer.music.load("assets/background_music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Αναπαραγωγή σε βρόχο

game_over = False


# Συνάρτηση για την έναρξη νέου παιχνιδιού
def new_game():
    global player1, player2, game_over, wave_manager
    # Επαναφορά μεταβλητών παιχνιδιού
    game_over = False

    # Δημιουργία νέου παίκτη1
    player1 = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, 40, 40, SKY_BLUE, 5, controls="arrows" , image_path="assets/Cyborg_idle_.png")
    
    # Δημιουργία νέου παίκτη2 (αν υποστηρίζεται)
    if game_mode == TWO_PLAYERS:
        player2 = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, 40, 40, ELECTRIC_INDIGO, 5, controls="wasd", image_path="assets/Punk_idle_.png")
    else:
        player2 = None
    
    # Επαναφορά των groups των sprites
    player1_bullets_group.empty()
    player2_bullets_group.empty()
    enemy_bullets_group.empty()
    enemies_group.empty()

    # Επαναφορά του wave manager
    wave_manager = EnemyWave(SCREEN_WIDTH, SCREEN_HEIGHT, enemies_group, enemy_bullets_group, player1_bullets_group, player1)
    wave_manager.new_enemy_wave() # Δημιουργία νέου κύματος εχθρών

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
                    game_mode = ONE_PLAYER
                    current_state = GAME
                    new_game()
                elif i == 1:  # NEW GAME - TWO player1
                    # Λογική για νέο παιχνίδι δύο παικτών (αν υποστηρίζεται)
                    current_state = GAME
                    game_mode = TWO_PLAYERS
                    new_game()
                elif i == 2:  # HIGHSCORES
                    current_state = HISHSCORES
                elif i == 3:  # EXIT
                    done = True
            
        screen.fill(BLACK)
        title_text = FONT_LARGE.render("CYBER RUNNER", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        for button in menu_buttons:
            button.draw(screen)

    elif current_state == GAME and not game_over:
        # Επεξεργασία εισόδου χρήστη
        player1.import_handler(SCREEN_WIDTH, player1_bullets_group)
        
        if game_mode == TWO_PLAYERS:
            player2.import_handler(SCREEN_WIDTH, player2_bullets_group)

        #----- UPDATES -----
        player1_bullets_group.update() # Ενημέρωση όλων των σφαιρών του παίκτη
        player2_bullets_group.update() # Ενημέρωση όλων των σφαιρών του παίκτη 2 (αν υπάρχει)
        enemy_bullets_group.update() # Ενημέρωση όλων των σφαιρών των εχθρών
        enemies_group.update() # Ενημέρωση όλων των εχθρών 
        wave_manager.update() # Ενημέρωση του wave manager
        
        #----- COLLISIONS AND DAMAGE ----- 
        
        # Έλεγχος σύγκρουσης σφαιρών εχθρών με τον παίκτη
        if player1 and player1.alive:
            collided_bullets_p1 = pygame.sprite.spritecollide(player1, enemy_bullets_group, True)
            for bullet in collided_bullets_p1:
                player1.take_damage(damage=wave_manager.enemy_damage)
        
        # Έλεγχος σύγκρουσης σφαιρών εχθρών με τον παίκτη 2 (αν υπάρχει)
        if player2 and player2.alive:
            collided_bullets_p2 = pygame.sprite.spritecollide(player2, enemy_bullets_group, True)
            for bullet in collided_bullets_p2:
                player2.take_damage(damage=wave_manager.enemy_damage)


        # Έλεγχος σύγκρουσης σφαιρών του παίκτη με εχθρούς
        hits = pygame.sprite.groupcollide(enemies_group, player1_bullets_group, False, True) # Έλεγχος σύγκρουσης σφαιρών του παίκτη με εχθρούς
        for enemy, bullets in hits.items():
            enemy.take_damage(damage=len(bullets)) # Αφαίρεση ζωής από τον εχθρό για κάθε σφαίρα που τον χτύπησε

        # Έλεγχος σύγκρουσης σφαιρών του παίκτη 2 με εχθρούς (αν υπάρχει παίκτης 2)
        if player2:
            hits2 = pygame.sprite.groupcollide(enemies_group, player2_bullets_group, False, True)
            for enemy, bullets in hits2.items():
                enemy.take_damage(damage=len(bullets)) 
   
        # ----- GAME OVER ΕΛΕΓΧΟΣ -----
        if game_mode == ONE_PLAYER:
            if player1.health <= 0:
                current_state = GAMEOVER
        else: # TWO PLAYERS mode
            if (player1.health <= 0) or (player2 and player2.health <= 0):
                current_state = GAMEOVER
            
                
            
        # ----- ΣΧΕΔΙΑΣΗ -----
        #screen.blit(backgrpund_img, (0, 0))  # Σχεδίαση φόντου
        screen.fill(BLACK)
        player1.draw(screen) # Σχεδίαση παίκτη
        if game_mode == TWO_PLAYERS and player2:
            player2.draw(screen) # Σχεδίαση παίκτη 2

        score_text = FONT_MEDIUM.render(f"{player1.score}", True, HOLLYWOOD_CERISE)
        screen.blit(score_text, (10, 10)) # Σχεδίαση score παίκτη

        health_text = FONT_MEDIUM.render(f"{player1.health}", True, RUSSIAN_VIOLET)
        screen.blit(health_text, (SCREEN_WIDTH - 30 , 10)) # Σχεδίαση ζωής παίκτη

        #health_text2 = FONT_MEDIUM.render(f"{player2.health}", True, RUSSIAN_VIOLET)
        # screen.blit(health_text2, (SCREEN_WIDTH - 30 , 60)) # Σχεδίαση ζωής παίκτη 2

        enemies_group.draw(screen) # Σχεδίαση εχθρών
        player1_bullets_group.draw(screen) # Σχεδίαση σφαιρών παίκτη
        player2_bullets_group.draw(screen) # Σχεδίαση σφαιρών παίκτη 2 (αν υπάρχει)
        enemy_bullets_group.draw(screen) # Σχεδίαση σφαιρών εχθρών
    



    elif current_state == HISHSCORES:
        print("HIGHSCORES state")
        pass # Λογική για την εμφάνιση των υψηλών σκορ

    elif current_state == GAMEOVER:
        #screen.fill(BLACK)
        game_over_text = FONT_LARGE.render("GAME OVER", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    # Ενημέρωση της οθόνης
    pygame.display.flip()
    clock.tick(60)

