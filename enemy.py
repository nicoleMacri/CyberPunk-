import pygame
import random
from entities import Entities

class Enemy(Entities):
    alive = True
    def __init__(self, x, y, width, height, color, speed):
        super().__init__(x, y, width, height, color, speed)

    # Μέθοδος για την αυτοματοποιημένη κίνηση του εχθρού
    def auto_move(self):   
        while self.alive:
            self.rect.x += self.speed # Κίνηση προς τα δεξιά
            # Επαναφορά της θέσης του εχθρού όταν βγει εκτός οθόνης δεξια
            if self.rect.left > 600:  # Υποθέτοντας ότι το πλάτος της οθόνης είναι 800
                self.rect.right = 0
                self.rect.y = random.randint(50, 600)  # Τυχαία νέα θέση y εντός οθόνης
        
   

    