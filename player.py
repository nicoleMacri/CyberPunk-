import pygame
from entities import Entities
from bullet import Bullet


class Player(Entities):
    """
    Κλάση για τον παίκτη που κληρονομεί από την κλάση Entities.
    Περιέχει μεθόδους για τον χειρισμό της κίνησης και των ενεργειών 
    του παίκτη. Δέχεται *groups προαιρετικά για να προστεθεί σε ομάδες sprite. (Ισως
    να μην είναι απαραίτητο εδώ).
    """
    def __init__(self, scr_width, scr_height, width, height, color, speed, *groups):
        start_x = int((scr_width - width)/ 2)
        start_y = int(scr_height - height - 10)
        
        super().__init__(start_x, start_y, width, height, color, speed, *groups)

        # Επιπλέον χαρακτηριστικά για τον πυροβολισμό από τον παίκτη
        self.fire_delay = 250  # Χρόνος καθυστέρησης μεταξύ πυροβολισμών σε milliseconds
        self.last_fire_time = 0  # Χρόνος του τελευταίου πυροβολισμού

        self.score = 0  # Αρχική βαθμολογία του παίκτη

    def shooting(self, bullets_group=None):
        now = pygame.time.get_ticks()
        if now - self.last_fire_time < self.fire_delay:
            return None # Δεν επιτρέπεται ο πυροβολισμός ακόμα
        
        bullet = Bullet.from_shooter( 
            self,
            width=4,
            height=10,
            color=(255, 0, 0),
            speed=10.0,
            vx=0.0,
            vy=-1.0
        )

        if bullets_group is not None:
            bullets_group.add(bullet)

        self.last_fire_time = now
        return bullet
    
        print("Player is shooting!")
    
    def score_point(self):
        # Λογική για την απόκτηση πόντου
        self.score += 1
        print("Player scored a point! Score:", self.score)

    # Μέθοδος για χειρισμό εισόδου χρήστη και κίνησης του παίκτη
    def import_handler(self, SCREEN_WIDTH, bullets_group=None):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shooting(bullets_group)  # Ενέργεια πυροβολισμού
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left(None)  # Χρησιμοποιεί self.speed ως default
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right(None)  # Χρησιμοποιεί self.speed ως default
        #Περιορισμός του ορθογωνίου να μην βγαίνει εκτός οθόνης
        margin = 50
        left_boundary = margin
        right_boundary = SCREEN_WIDTH - margin - self.w
        if self.x < left_boundary:
            self.x = left_boundary
        if self.x > right_boundary:
            self.x = right_boundary