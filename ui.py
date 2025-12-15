import pygame
"""
Έδω περιέχονται κλάσεις για την διαχείρση του UI του παιχνιδιού.
"""
class Button:
    """
    Κλάση που αναπαριστά ένα κουμπί στο UI.
    Περιλαμβάνει μεθόδους για την σχεδίαση του κουμπιού, τον έλεγχο αν έχει πατηθεί κ.α.
    """
    def __init__(self, x, y, width, height, txt, font, bg_clr, txt_clr):
        self.rect = pygame.Rect(x, y, width, height)  # Ορθογώνιο του κουμπιού
        self.txt = txt  # Κείμενο του κουμπιού
        self.font = font  # Γραμματοσειρά
        self.bg_clr = bg_clr  # Χρώμα φόντου
        self.txt_clr = txt_clr  # Χρώμα κειμένου

    def draw(self, screen):
        """ Σχεδιάζει το κουμπί στην οθόνη. """
        pygame.draw.rect(screen, self.bg_clr, self.rect)  # Σχεδίαση φόντου κουμπιού
        text_surf = self.font.render(self.txt, True, self.txt_clr)  # Δημιουργία επιφάνειας κειμένου
        text_rect = text_surf.get_rect(center=self.rect.center)  # Κεντράρισμα κειμένου στο κουμπί
        screen.blit(text_surf, text_rect)  # Σχεδίαση κειμένου

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False