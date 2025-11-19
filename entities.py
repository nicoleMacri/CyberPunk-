import pygame

class Entities:
    # Αρχικοποίηση της κλάσης με βασικά χαρακτηριστικά
    def __init__(self, x, y, width, height, color, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed

       
    # Μέθοδος για σχεδίαση του αντικειμένου
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    # Μέθοδοι κίνησης
    def move_left(self, speed):
        self.rect.x -= speed
    def move_right(self, speed):
        self.rect.x += speed
    def move_up(self, speed):
        self.rect.y -= speed
    def move_down(self, speed):
        self.rect.y += speed

    # Μέθοδος για πυροβολισμό
    def shooting(self):
        # Placeholder for shooting logic
        print("Shooting action executed")

