import pygame

class Entities(pygame.sprite.Sprite):
    """
    Βάση κλάση για όλα τα οντότητες στο παιχνίδι. Κληρονομεί την pygame.sprite.Sprite., έχει
    image και rect attributes τα οποία χρησιμοποιούνται για τη διαχείριση και την απεικόνιση
    των οντοτήτων στο παιχνίδι, μεταξύ άλλων σε group sprites. 
    Περιέχει βασικές μεθόδους και χαρακτηριστικά που θα χρησιμοποιηθούν από τις υποκλάσεις.

    """
    # Αρχικοποίηση της κλάσης με βασικά χαρακτηριστικά
    def __init__(self, x, y, width, height,
                 speed, *groups):
        # *groups επιτρέπει να προσθέσουμε ενα αντικείμενο σε πολλαπλές ομάδες sprite
        # Κλήση του constructor της γονικής κλάσης
        super().__init__(*groups) 
        # Για ομαλή κίνηση χρησιμοποιούμε float για τις συντεταγμένες
        self._x = float(x)
        self._y = float(y)
        self.w = int(width)
        self.h = int(height)
        #self.color = color
        self.speed = float(speed)

        # Δημιουργία της εικόνας και του ορθογωνίου (rect) για την οντότητα
        self.image = pygame.Surface((self.w, self.h)) # τεστ θα πρέπει να αλλάξει
        #self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(self._x, self._y))

        # flag για την κατάσταση της οντότητας
        self.alive = True
    
    # Συγρχρονισμός της θέσης
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = int(self._x)
    
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = int(self._y)

    
       
    # Μέθοδος για σχεδίαση του αντικειμένου
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # Μέθοδοι κίνησης
    def move_left(self, speed=None):
        s = speed if speed is not None else self.speed
        self._x -= s 
        self.rect.x = int(self._x)

    def move_right(self, speed=None):
        s = speed if speed is not None else self.speed
        self._x += s
        self.rect.x = int(self._x)

    def move_up(self, speed=None):
        s = speed if speed is not None else self.speed
        self._y -= s
        self.rect.y = int(self._y)

    def move_down(self, speed=None):
        s = speed if speed is not None else self.speed
        self._y += s
        self.rect.y = int(self._y)

    def update(self, *args, **kwargs):
        """
        Βασική μέθοδος για την ενημέρωση κάθε frame. Οι υποκλάσεις μποροούν να την 
        επεκτείνουν για να προσθέσουν επιπλέον λειτουργικότητα. Τα args και kwargs
        επιτρέπουν την περαιτέρω παραμετροποίηση της ενημέρωσης
        """
        # Συγχρονισμός της θέσης του rect με τις συντεταγμένες x και y
        self.rect.topleft = (int(self._x), int(self._y)) 
        

