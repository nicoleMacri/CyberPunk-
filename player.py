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

    