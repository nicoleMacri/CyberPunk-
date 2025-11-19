import pygame

# Εισαγωγή κλάσεων Player και Enemy 
from player import Player
from enemy import Enemy

# Αρχικοποίηση της βιβλιοθήκης Pygame
pygame.init()

# Ορισμός χρωμάτων
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUSSIAN_VIOLET = (52, 27, 95)
HOLLYWOOD_CERISE = (236, 19, 164)
AUREOLIN = (245, 230, 18)
ELECTRIC_INDIGO = (99, 57, 235)
SKY_BLUE = (94, 217, 242)

# Ρυθμίσεις παραθύρου
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER RUNNER")

# Ρυθμίσεις γραμματοσειράς
FONT_LARGE = pygame.font.SysFont('Arial', 72) # Θα αλλαχθεί με καποία που ταιρίαζει πιο πολύ στο θέμα
FONT_MEDIUM = pygame.font.SysFont('Arial', 36)
FONT_SMALL = pygame.font.SysFont('Arial', 24)

# Ρυθμίσεις ρολογιού
clock = pygame.time.Clock() 

# Δημιουργία αντικειμένου Player
player = Player( SCREEN_WIDTH, SCREEN_HEIGHT, 50, 50, SKY_BLUE, 5)

# Δημιουργία αντικειμένου Enemy 
enemy = Enemy(100, 100, 50, 50, ELECTRIC_INDIGO, 3)






# Μέθοδος για χειρισμό εισόδου χρήστη και κίνησης του παίκτη
def import_handler():
    speed = player.speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.shooting()  # Ενέργεια πυροβολισμού
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left(speed)  # Ενέργεια κίνησης αριστερά
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right(speed)  # Ενέργεια κίνησης δεξιά
    #Περιορισμός του ορθογωνίου να μην βγαίνει εκτός οθόνης
    if player.rect.left < 50:
        player.rect.left = 50
    if player.rect.right > SCREEN_WIDTH - 50:
        player.rect.right = SCREEN_WIDTH - 50
    

# Κύρια λούπα παιχνιδιού
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    import_handler()
    enemy.auto_move() # Αρχική κίνηση του εχθρού
    enemy2.auto_move() # Αρχική κίνηση του εχθρού 2
    screen.fill(RUSSIAN_VIOLET)
    player.draw(screen)
    enemy.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)