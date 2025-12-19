import pygame
from entities import Entities
from bullet import Bullet

#def load_player_frames(img,frame_width, frame_height):
#    """
#    βοηθητική συνάρτηση για την φόρτωση των frames του παίκτη απο sprite sheet.
#    Επιστρέφει μια λίστα με τα frames.
#    """
#    frames = []
#    sheet_width = img.get_width()
#
#    for x in range(0, sheet_width, frame_width):
#        frame = img.subsurface(pygame.Rect(x, 0, frame_width, frame_height))
#        frames.append(frame)
#    return frames


class Player(Entities):
    """
    Κλάση για τον παίκτη που κληρονομεί από την κλάση Entities.
    Περιέχει μεθόδους για τον χειρισμό της κίνησης και των ενεργειών 
    του παίκτη. Δέχεται *groups προαιρετικά για να προστεθεί σε ομάδες sprite. (Ισως
    να μην είναι απαραίτητο εδώ).
    """
    def __init__(self, scr_width, scr_height, width, height, 
                 speed, controls, image_path, *groups):
        start_x = int((scr_width - width)/ 2)
        start_y = int(scr_height - height - 10)
        
        super().__init__(start_x, start_y, width, height, 
                         speed, *groups)

        # Επιπλέον χαρακτηριστικά για τον πυροβολισμό από τον παίκτη
        self.fire_delay = 250  # Χρόνος καθυστέρησης μεταξύ πυροβολισμών σε milliseconds
        self.last_fire_time = 0  # Χρόνος του τελευταίου πυροβολισμού

        self.score = 0  # Αρχική βαθμολογία του παίκτη
        self.max_health = 5  # Μέγιστη υγεία του παίκτη
        self.health = 5  # Αρχική υγεία του παίκτη
        self.controls = controls  # Πλήκτρα ελέγχου του παίκτη

        # ----- sprite παικτή -----
        self.image = pygame.image.load(image_path).convert_alpha() # Φόρτωση εικόνας με διαφάνεια

        w = int(self.image.get_width() * 1.5)  # Κλιμάκωση πλάτους
        h = int(self.image.get_height() * 1.5)  # Κλιμάκωση ύψους
        self.image = pygame.transform.scale(self.image, (w, h))  # Κλιμάκωση εικόνας

        self.rect = self.image.get_rect() 
        self.rect.center =(self.x,self.y) # Κεντράρισμα του rect στην αρχική θέση

        # ----- ρυθμίσεις για ήχο παίκτη -----
        self.shoot_sound = pygame.mixer.Sound("assets/plaeyer_shooting.wav")
        self.shoot_sound.set_volume(0.2)  # Ρύθμιση έντασης ήχου

        # ----- animation παίκτη -----
        #self.animations = {
        #    "idle": load_player_frames(pygame.image.load("assets/Cyborg_idle.png").convert_alpha(), 32, 32),
        #    "attack": load_player_frames(pygame.image.load("assets/Cyborg_attack3.png").convert_alpha(), 32, 32),
        #}

        #self.current_animation = "idle"
        #self.animation_index = 0
        #self.animation_speed = 0.15  # Ταχύτητα animation
        #self.image = self.animations[self.current_animation][0] # Αρχική εικόνα animation
        #self.last_frame_update = pygame.time.get_ticks()

    def shooting(self, bullets_group=None):
        now = pygame.time.get_ticks()
        if now - self.last_fire_time < self.fire_delay:
            return None # Δεν επιτρέπεται ο πυροβολισμός ακόμα
        
        bullet = Bullet.from_shooter( 
            self,
            width=4,
            height=10,
            speed=10.0,
            vx=0.0,
            vy=-1.0
        )

        if bullets_group is not None:
            bullets_group.add(bullet)

        self.last_fire_time = now
        self.shoot_sound.play()  # Αναπαραγωγή ήχου πυροβολισμού
        #self.set_animation("attack")
        print("Player is shooting!")
        return bullet
        
    
    def score_point(self):
        # Λογική για την απόκτηση πόντου
        self.score += 1
        print("Player scored a point! Score:", self.score)

    # Μέθοδος για χειρισμό εισόδου χρήστη και κίνησης του παίκτη
    def import_handler(self, SCREEN_WIDTH, bullets_group=None):
        keys = pygame.key.get_pressed()
        if self.controls == "wasd":
            if keys[pygame.K_w]:
                self.shooting(bullets_group)  # Ενέργεια πυροβολισμού
            if keys[pygame.K_a]:
                self.move_left(None)  # Χρησιμοποιεί self.speed ως default
            if keys[pygame.K_d]:
                self.move_right(None)  # Χρησιμοποιεί self.speed ως default
        elif self.controls == "arrows":
            if keys[pygame.K_UP]:
                self.shooting(bullets_group)  # Ενέργεια πυροβολισμού
            if keys[pygame.K_LEFT]:
                self.move_left(None)  # Χρησιμοποιεί self.speed ως default
            if keys[pygame.K_RIGHT]:
                self.move_right(None)  # Χρησιμοποιεί self.speed ως default
        #Περιορισμός του ορθογωνίου να μην βγαίνει εκτός οθόνης
        margin = 50
        left_boundary = margin
        right_boundary = SCREEN_WIDTH - margin - self.w
        if self.x < left_boundary:
            self.x = left_boundary
        if self.x > right_boundary:
            self.x = right_boundary

    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print("player defeated")

 #
 #         self.current_animation = animation_name
 #           self.animation_index = 0
 #           print(f"Player animation changed to: {animation_name}")
 #           #self.last_frame_update = pygame.time.get_ticks()
    
 #   def animate(self):
 #       now = pygame.time.get_ticks()
 #       if now - self.last_frame_update < 100:  # Χρόνος μεταξύ καρέ σε milliseconds
 #           return
        
 #           self.last_frame_update = now

 #       frames = self.animations[self.current_animation]
 #       self.animation_index += 1

 #       if self.animation_index >= len(frames):
 #           if self.current_animation == "attack":
 #               self.set_animation("idle")
 #           self.animation_index = 0
    
 #       self.image = frames[int(self.animation_index)]

 #   def update(self):
        #self.import_handler(SCREEN_WIDTH, bullets_group)
 #       self.animate()

 #   def draw(self, screen):
 #       screen.blit(self.image, self.rect)