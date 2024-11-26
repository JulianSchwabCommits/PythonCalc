import pygame
import sys

# Pygame initialisieren
pygame.init()

# Farben definieren
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
GRAU = (128, 128, 128)
ORANGE = (255, 165, 0)

# Fenster-Einstellungen
BREITE = 400
HOEHE = 600
BILDSCHIRM = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Taschenrechner")

# Schrift initialisieren
SCHRIFT = pygame.font.Font(None, 36)

class Taschenrechner:
    def __init__(self):
        self.aktuelle_eingabe = "0"
        self.erste_zahl = None
        self.operator = None
        self.neue_eingabe = True
        self.display_text = "0"

    def taste_gedrueckt(self, taste):
        if taste.isdigit() or taste == ".":
            if self.neue_eingabe:
                self.aktuelle_eingabe = taste
                self.neue_eingabe = False
            else:
                self.aktuelle_eingabe += taste
            self.display_text = self.aktuelle_eingabe
        elif taste in ["+", "-", "*", "/"]:
            self.erste_zahl = float(self.aktuelle_eingabe)
            self.operator = taste
            self.neue_eingabe = True
            self.display_text = f"{self.erste_zahl} {self.operator}"
        elif taste == "=":
            if self.erste_zahl is not None and self.operator is not None:
                zweite_zahl = float(self.aktuelle_eingabe)
                if self.operator == "+":
                    ergebnis = self.erste_zahl + zweite_zahl
                elif self.operator == "-":
                    ergebnis = self.erste_zahl - zweite_zahl
                elif self.operator == "*":
                    ergebnis = self.erste_zahl * zweite_zahl
                elif self.operator == "/":
                    ergebnis = self.erste_zahl / zweite_zahl if zweite_zahl != 0 else "Error"
                
                self.aktuelle_eingabe = str(ergebnis)
                self.display_text = f"{self.erste_zahl} {self.operator} {zweite_zahl} = {ergebnis}"
                self.erste_zahl = None
                self.operator = None
                self.neue_eingabe = True
        elif taste == "C":
            self.aktuelle_eingabe = "0"
            self.erste_zahl = None
            self.operator = None
            self.neue_eingabe = True
            self.display_text = "0"

def hauptprogramm():
    rechner = Taschenrechner()
    
    # Tasten definieren
    tasten = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
        ["C"]
    ]

    while True:
        BILDSCHIRM.fill(SCHWARZ)
        
        # Display-Bereich zeichnen
        pygame.draw.rect(BILDSCHIRM, GRAU, (10, 10, BREITE-20, 80))
        display_text = SCHRIFT.render(rechner.display_text, True, WEISS)
        text_rect = display_text.get_rect()
        text_rect.right = BREITE - 20
        text_rect.centery = 50
        BILDSCHIRM.blit(display_text, text_rect)

        # Tasten zeichnen
        taste_hoehe = 80
        for y, reihe in enumerate(tasten):
            for x, taste in enumerate(reihe):
                taste_breite = (BREITE - 50) // 4 if len(reihe) > 1 else BREITE - 20
                taste_x = 10 + x * (taste_breite + 10)
                taste_y = 100 + y * (taste_hoehe + 10)
                
                farbe = ORANGE if taste in ["+", "-", "*", "/", "="] else GRAU
                pygame.draw.rect(BILDSCHIRM, farbe, (taste_x, taste_y, taste_breite, taste_hoehe))
                
                taste_text = SCHRIFT.render(taste, True, WEISS)
                text_rect = taste_text.get_rect(center=(taste_x + taste_breite//2, taste_y + taste_hoehe//2))
                BILDSCHIRM.blit(taste_text, text_rect)

        # Events verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                maus_pos = pygame.mouse.get_pos()
                for y, reihe in enumerate(tasten):
                    for x, taste in enumerate(reihe):
                        taste_breite = (BREITE - 50) // 4 if len(reihe) > 1 else BREITE - 20
                        taste_x = 10 + x * (taste_breite + 10)
                        taste_y = 100 + y * (taste_hoehe + 10)
                        
                        if (taste_x <= maus_pos[0] <= taste_x + taste_breite and 
                            taste_y <= maus_pos[1] <= taste_y + taste_hoehe):
                            rechner.taste_gedrueckt(taste)

        pygame.display.flip()

if __name__ == "__main__":
    hauptprogramm()
