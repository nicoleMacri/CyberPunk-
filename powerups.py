from entities import Entities

class PowerUp(Entities):
    def __init__(self, x, y, width, height, color, speed):
        super().__init__(x, y, width, height, color, speed)
    
    # Μέθοδος για την ενεργοποίηση του power-up
    def activate(self):
        self.move_down(self.speed)
        print("Power-up activated for player!") 
    
    # Μέθοδος για την απενεργοποίηση του power-up
    def deactivate(self):
        print("Power-up deactivated for player!")
    
    