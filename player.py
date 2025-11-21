import pygame
from entities import Entities

class Player(Entities):
    def __init__(self, scr_width, scr_height, width, height, color, speed):
        start_x = int((scr_width - width)/ 2)
        start_y = int(scr_height - height - 10)
        
        super().__init__(start_x, start_y, width, height, color, speed)


    def shooting(self):
        # Ειδική λογική για τον παίκτη κατά τον πυροβολισμό
        print("Player is shooting!")
    
    def score_point(self):
        # Λογική για την απόκτηση πόντου
        print("Player scored a point!")

    # Μέθοδος για χειρισμό εισόδου χρήστη και κίνησης του παίκτη
    def import_handler(self, SCREEN_WIDTH):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shooting()  # Ενέργεια πυροβολισμού
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left(self.speed)  # Ενέργεια κίνησης αριστερά
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right(self.speed)  # Ενέργεια κίνησης δεξιά
        #Περιορισμός του ορθογωνίου να μην βγαίνει εκτός οθόνης
        if self.rect.left < 50:
            self.rect.left = 50
        if self.rect.right > SCREEN_WIDTH - 50:
            self.rect.right = SCREEN_WIDTH - 50
    