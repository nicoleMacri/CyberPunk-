import pygame
from enemy import Enemy

class BossEnemy(Enemy):
    """
    Κλάση για τον υπερεχθρό.
    Προς το παρόν, κληρονομεί απλά από την κλάση Enemy χωρίς επιπλέον λειτουργικότητα.
    Η επιπλέον λειτουργικότητα θα προστεθεί αργότερα.
    """
    def __init__(self, x, y):
        super().__init__(x=x, y=y, width=100, height=100, color=(255, 0, 255), speed=2.0,)

        self.hp = 50  # Ο υπερεχθρός έχει περισσότερη υγεία