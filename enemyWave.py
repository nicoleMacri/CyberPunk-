import pygame
import random
from enemy import Enemy

class EnemyWave:
    """
    Κλάση για την διαχείρηση κυμάτων (waves) εχθρών.
    Περιλαμβάνει μεθόδους για την δημιουργία grid εχθρών, την δημιουργία νέου κύματος εχθρών, την ενημέρωση της κατάστασης των κυμάτων κ.α.

    """
    def __init__(self, scr_width, scr_height, enemies_group, enemy_bullets_group, player_bullets_group, player):
        self.scr_width = scr_width # Πλάτος οθόνης
        self.scr_height = scr_height # Ύψος οθόνης
        self.enemies_group = enemies_group # Group με τους εχθρούς
        self.enemy_bullets_group = enemy_bullets_group # Group με τις σφαίρες εχθρών
        self.player_bullets_group = player_bullets_group # Group με τις σφαίρες παίκτη
        self.player = player  # Αντικείμενο παίκτη

        self.enemies_colors = [
            (245, 230, 18), # LASER_LEMON
            (236, 19, 164), # HOLLYWOOD_CERISE
            (99, 57, 235) # ELECTRIC_INDIGO
        ]

        self.rows = None # Ορίζεται απο την random_grid_size
        self.cols = None # Ορίζεται απο την random_grid_size
        self.spacing_x = 60  # Απόσταση μεταξύ στηλών
        self.spacing_y = 40  # Απόσταση μεταξύ σειρών

        self.row_cooldown = 200  # ms
        self.last_row_switch_time = 0 # Χρόνος αλλαγής της σειράς

        self.enemies_grid = None # 2D λίστα με τους εχθρούς
        self.status_rows = None # Κατάσταση των σειρών
        self.active_row = None # Τρέχουσα ενεργή σειρά

        self.moving_horizontal = False # Flag για την κίνηση αριστερά-δεξιά των εχθρών

        self.grid_offset = 0.0
        self.grid_direction = 1  # 1 για δεξιά, -1 για αριστερά
        self.grid_speed = 2.0  # Ταχύτητα κίνησης του grid αριστερά-δεξιά 
        self.padding = 50

        self.wave_number = 0  # Αριθμός τρέχοντος κύματος εχθρών
        self.enemy_damage = 1  # Βασική ζημιά που προκαλεί κάθε εχθρός

    def random_grid_size(self):
        """
        Μέθοδος για την τυχαία ρύθμιση του μεγέθους του grid εχθρών.
        Ορίζει τυχαίες τιμές για τις σειρές και τις στήλες με αυξανόμενη δυσκολία.
        Η δυσκολία αυξάνεται ανα 3 κύματα εχθρών.

        """
        difficulty = self.wave_number // 3  # Αύξηση δυσκολίας κάθε 3 κύματα
        min_rows = 2 # ελάχιστος αριθμός σειρών και στηλών
        max_rows = 4 # μέγιστος αριθμός σειρών και στηλών

        max_rows = max_rows + difficulty
        max_cols = max_rows + difficulty
        rows_max = min (max_rows, 6) # μέγιστος αριθμός σειρών με όριο το 6
        cols_max = min (max_cols, 6) # μέγιστος αριθμός στηλών με όριο το 6

        self.rows = random.randint(min_rows, rows_max) # Τυχαίος αριθμός σειρών
        self.cols = random.randint(min_rows, cols_max) # Τυχαίος αριθμός στηλών

        

    def enemies_grid_create(self):
        """
        Μέθοδος για την δημιουργία ενός grid εχθρών.
        Επιστρέφει μια 2D λίστα με τους εχθρούς.
        enemies_grid_local: [
            [Enemy00, Enemy01, ...],  # Σειρά 0
            [Enemy10, Enemy11, ...],  # Σειρά 1
            [...],                    # ...
        ]
        
        """

        
        grid_width = (self.cols - 1) * self.spacing_x  # Πλάτος του grid
        grid_height = (self.rows - 1) * self.spacing_y # Ύψος του grid

        start_x = (self.scr_width - grid_width) // 2 # Κεντράρισμα οριζόντια στο κέντρο της οθόνης
        start_y = (self.scr_height - grid_height) // 4 #Κεντράρισμα κάθετα στο άνω μέρος της οθόνης
        
        enemies_grid_local = [] # 2D λίστα με τους εχθρούς
        for row in range (self.rows):
            row_list = [] # Λίστα για την τρέχουσα σειρά
            for col in range (self.cols):
                fin_y = start_y + row * self.spacing_y
                x = start_x + col * self.spacing_x

                # Αρχικοποίηση εχθρού
                enemy = Enemy(x,-100,30,30,
                            color = random.choice(self.enemies_colors),
                            speed = 4.0,
                            move = "down",
                            fin_y=fin_y,
                            row = row,
                            col = col,
                            bullets_group = self.enemy_bullets_group,
                            shoot_delay = 2000,
                            row_height = self.spacing_y, # αυτο δεν χρησιμοποιείται πλέον
                            hp = 1,
                            player_object = self.player)
                
                self.enemies_group.add(enemy) # Προσθήκη του εχθρού στο αντίστοιχο group
                row_list.append(enemy) # Προσθήκη του εχθρού στη σειρά
            enemies_grid_local.append(row_list) # Προσθήκη της σειράς στο grid
        # Επαναφορά της κατάστασης κίνησης του grid
        self.grid_offset = 0.0 
        self.grid_direction = 1
          
        return enemies_grid_local # Επιστροφή του grid εχθρών
    
    def status_rows_init(self):
        """
        Επιστρέφει μια λίστα με την κατάσταση ενεργοποίησης των σειρών.
        status_rows: [ 
            {'activated': False, 'start_time': None},  # Σειρά 0
            {'activated': False, 'start_time': None},  # Σειρά 1
            ...
        ]
        """
        return [{'activated': False, 'start_time': None} for _ in range(self.rows)]
    
    def row_activate(self, idx):
        """
        Μέθοδος για την ενεργοποίηση μιας σειράς εχθρών.
        idx: Δείκτης της σειράς που θα ενεργοποιηθεί.
        """
        #now = pygame.time.get_ticks()
        self.status_rows[idx]['activated'] = True
        #self.status_rows[idx]['start_time'] = now
        for enemy in self.enemies_grid[idx]:
            #enemy.activate(row_height=self.spacing_y)
            enemy.activate()
    
    def new_enemy_wave(self):
        """
        Μέθοδος για την δημιουργία νέου κύματος(wave) εχθρών.
        Ουσιαστικά επαναφέρει το grid εχθρών.
        """
        self.wave_number += 1  # Αύξηση του αριθμού κύματος
        #if self.wave_number % 5 == 0:
        #    self.enemy_damage += 1  # Αύξηση της ζημιάς των εχθρών κάθε 5 κύματα
        self.enemies_group.empty() # Αφαίρεση όλων των εχθρών από το group
        self.enemy_bullets_group.empty() # Αφαίρεση όλων των σφαιρών εχθρών από το group
        self.random_grid_size() # Τυχαία ρύθμιση μεγέθους grid
        self.enemies_grid = self.enemies_grid_create() # Δημιουργία νέου grid εχθρών
        self.status_rows = self.status_rows_init() # Αρχικοποίηση της κατάστασης των σειρών
        self.active_row = self.rows - 1 # Ορισμός της πρώτης σειράς
        self.row_activate(self.active_row) # Ενεργοποίηση της πρώτης σειράς
        self.last_row_switch_time = pygame.time.get_ticks() # Επαναφορά του χρόνου αλλαγής σειράς

        self.player_bullets_group.empty() # Αφαίρεση όλων των σφαιρών παίκτη από το group

    def row_cleared(self, idx):
        """
        Μέθοδος για τον έλεγχο αν μια σειρά εχθρών έχει καθαρίσει.
        idx: Δείκτης της σειράς που θα ελεγχθεί.
        Αν ο εχθρος ειναι alive τότε υπάρχει ενεργός εχθρός στην σειρά άρα η σειρά δεν έχει καθαρίσει.
        """
        for enemy in self.enemies_grid[idx]:
            if enemy.alive:
                return False
        return True
    
    def wave_complete(self):
        """
        Μέθοδος για τον έλεγχο αν το κύμα εχθρών έχει ολοκληρωθεί.
        Ουσιαστικά ελέγχει αν όλες οι σειρές έχουν καθαρίσει.

        """
        return all(self.row_cleared(row) for row in range(self.rows))

    def enemies_grid_move(self):
        """
        Μέθοδος για την κίνηση του grid εχθρών αριστερά-δεξιά.
        """
        
        min_x = float('inf') # Αριστερό άκρο του grid
        max_x = float('-inf') # Δεξί άκρο του grid
        for row in self.enemies_grid:
            for enemy in row:
                if enemy.rect.x < min_x:
                    min_x = enemy.rect.x
                if enemy.rect.x + enemy.rect.width > max_x:
                    max_x = enemy.rect.x + enemy.rect.width

        

        if min_x <= self.padding: # padding αριστερά
            self.grid_direction = 1  # Αλλαγή κατεύθυνσης προς τα δεξιά
        elif max_x >= self.scr_width - self.padding: # padding δεξιά
            self.grid_direction = -1  # Αλλαγή κατεύθυνσης προς τα αριστερά

       

        for enemy_row in self.enemies_grid:
            for enemy in enemy_row:
                enemy.rect.x += self.grid_direction * self.grid_speed
                if hasattr(enemy, 'x'):
                    enemy.x = enemy.rect.x

        self.moving_horizontal = True  # Ορισμός του flag ότι οι εχθροί κινούνται αριστερά-δεξιά

    
    def enemies_final_position(self):
        """
        Μέθοδος για τον έλεγχο αν όλοι οι εχθροί έχουν φτάσει στην τελική τους θέση.
        Επιστρέφει True αν όλοι οι εχθροί έχουν φτάσει στην τελική τους θέση, αλλιώς False.
        """
        for enemy_row in self.enemies_grid:
            for enemy in enemy_row:
                if not enemy.movement_done and enemy.alive:
                    return False
        return True
    

    def update(self):
        """
        Μέθοδος για την ενημέρωση της κατάστασης των κυμάτων εχθρών.
        Καλείται στην κύρια λούπα του παιχνιδιού.
        """
        now = pygame.time.get_ticks() 

        # Έλεγχος αν όλοι οι εχθροί έχουν φτάσει στην τελική τους θέση ώστε να ξεκινήσει η κίνηση τους
        if self.enemies_final_position() or self.moving_horizontal:
            self.enemies_grid_move()

        # Πυροβολισμοί εχθρών από την ενεργή σειρά
        for enemy in list(self.enemies_group):
            if enemy.row == self.active_row and enemy.alive and enemy.movement_done:
                enemy.shoot()
        
        # Έλεγχος αν το κύμα έχει ολοκληρωθεί
        if self.wave_complete():
            self.new_enemy_wave() # Δημιουργία νέου κύματος εχθρών
            return

        # Έλεγχος αν η ενεργή σειρά έχει καθαρίσει
        if self.row_cleared(self.active_row):
            # Μετακίνηση στην επόμενη σειρά αν υπάρχει
            if self.active_row - 1 >= 0:
                # Έλεγχος αν έχει περάσει ο χρόνος cooldown για την αλλαγή σειράς
                if now - self.last_row_switch_time >= self.row_cooldown:
                    self.active_row -= 1 # Μετακίνηση στην επόμενη σειρά
                    self.row_activate(self.active_row) # Ενεργοποίηση της επόμενης σειράς
                    self.last_row_switch_time = now
            # Διαφορετικά, αν δεν υπάρχουν άλλες σειρές, δημιουργία νέου κύματος        
            else:
                self.new_enemy_wave() # Δημιουργία νέου κύματος εχθρών