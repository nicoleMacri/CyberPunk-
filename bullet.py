import pygame
from entities import Entities

class Bullet(Entities): 
    """
    Κλάση για τα αντικείμενα σφαίρας που κληρονομεί από την κλάση Entities.
    - Η σφαίρα κινείται με βάση ένα velocity vector (vx,vy) πολλαπλασιασμένο με την ταχύτητά της.
    - Μπορεί να προστεθεί λογική για την αφαίρεση της σφαίρας όταν βγει εκτός οθόνης.
    - Θα προσθεσούν οι για έλεγχο collision κλπ.
    - Δέχεται *groups προαιρετικά για να προστεθεί σε ομάδες sprite.
    """
    def __init__(self, x, y, width, height, color, speed,  vx, vy, owner=None, *groups):
        """
        Arguments:
        x, y: Αρχικές συντεταγμένες της σφαίρας.
        width, height: Διαστάσεις της σφαίρας.
        color: Χρώμα της σφαίρας.
        speed: Ταχύτητα κίνησης της σφαίρας.
        vx, vy: Συνιστώσες της κατεύθυνσης κίνησης (velocity vector).
        owner: Αναφορά στον κάτοχο της σφαίρας (π.χ. Player ή Enemy).
        *groups: Προαιρετικά, ομάδες sprite στις οποίες θα προστεθεί η
        """
        super().__init__(x, y, width, height, color, speed, *groups)
        # επιπλέον χαρακτηριστικά για τη σφαίρα
        self.vx = float(vx)
        self.vy = float(vy)
        self.owner = owner  # Μπορεί να είναι Player ή Enemy

    def update(self, *args, **kwargs):
        """
        Ενημερώνει τη θέση της σφαίρας με βάση το velocity vector και την ταχύτητα ανα frame.

        """
        # Μετακίνηση της σφαίρας βάσει του velocity vector
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        super().update(*args, **kwargs) # Ενημέρωση του rect με κλήση της υπερκλάσης
        #ΤΟDO: Να προστεθεί λογική για να αφαιρεθεί η σφαίρα αν βγει εκτός οθόνης
    
    @classmethod
    def from_shooter(cls, shooter, width, height, color, speed, vx, vy, *groups):
        """
        Δημιουργεί μια σφαίρα που εκτοξεύεται από έναν shooter (Player ή Enemy).

        Arguments:
        shooter: Το αντικείμενο που εκτοξεύει τη σφαίρα (π.χ. Player ή Enemy).
        width, height: Διαστάσεις της σφαίρας.
        color: Χρώμα της σφαίρας.
        speed: Ταχύτητα κίνησης της σφαίρας.
        vx, vy: Συνιστώσες της κατεύθυνσης κίνησης (velocity vector).
        *groups: Προαιρετικά, ομάδες sprite στις οποίες θα προστεθεί η σφαίρα.

        Returns:
        Μια νέα instance της κλάσης Bullet.
        """
        # Υπολογισμός αρχικής θέσης της σφαίρας (κέντρο πάνω από τον shooter)
        bx = shooter.x + shooter.w // 2 - width // 2
        by = shooter.y - height  # Πάνω από τον shooter
        return cls(bx, by, width, height, color, speed, vx, vy, owner=shooter, *groups)