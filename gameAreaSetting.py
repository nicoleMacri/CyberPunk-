import pygame

class GameArea:
    def __init__(self, width, height, left, top):
        self.width = width
        self.height = height
        self.left = left
        self.top = top

        self.right = left + width
        self.bottom = top + height

        self.rect = pygame.Rect(left, top, width, height)