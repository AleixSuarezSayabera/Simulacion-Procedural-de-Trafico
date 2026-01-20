import keyboard
import time

class Menu:
    def __init__(self, tk, w):
        self.tk = tk
        self.w = w
        self.tecla_esc = False
        self.tecla_1 = False
        self.tecla_2 = False
        self.tecla_3 = False
        self.tecla_premuda = False
    
    def pinta(self):
        self.w.delete("all")
        self.w.create_text(400, 100, text="ESCAPA DE LA AP-7", fill="white", font=("Arial", 44, "bold"))
        self.w.create_text(400, 250, text="1 - Joc Normal", fill="yellow", font=("Arial", 22))
        self.w.create_text(400, 310, text="2 - Mode Crear Carretera", fill="yellow", font=("Arial", 22))
        self.w.create_text(400, 370, text="3 - Instruccions", fill="yellow", font=("Arial", 22))
        self.w.create_text(400, 450, text="ESC - Sortir", fill="red", font=("Arial", 18))
    
    def teclat(self):
        if keyboard.is_pressed("1"):
            self.tecla_1 = True
            self.tecla_premuda = True
        elif keyboard.is_pressed("2"):
            self.tecla_2 = True
            self.tecla_premuda = True
        elif keyboard.is_pressed("3"):
            self.tecla_3 = True
            self.tecla_premuda = True
        elif keyboard.is_pressed("esc"):
            self.tecla_esc = True
            self.tecla_premuda = True

    def instruccions(self):
        while keyboard.is_pressed("3"):
            self.w.update()

        sortir = False
        while not sortir:
            self.w.delete("all")
            self.w.create_text(400, 80, text="INSTRUCCIONS", fill="orange", font=("Arial", 30, "bold"))
            text = ("Hi han dos modes de joc:\n"
                     "1. Esquiva el tràfic de l'AP-7.\n"
                     "2. Mode Pintar: Crea el teu camí.\n\n"
                     "Configuració via JSON:\n"
                     "Pots modificar angles, distàncies i el\n"
                     "paràmetre 'lambda' per la quantitat de tràfic.\n")
            
            self.w.create_text(400, 280, text=text, fill="white", font=("Arial", 16), justify="center")
            self.w.create_text(400, 500, text="Prem ESC per tornar al menú", fill="lightgray", font=("Arial", 14))
            self.w.update()
            
            if keyboard.is_pressed("esc"):
                sortir = True
                while keyboard.is_pressed("esc"):
                    self.w.update()
        self.tecla_3 = False
        self.tecla_premuda = False

    def mostrar(self):
        while keyboard.is_pressed("esc"):
            self.w.update()
            time.sleep(1/60)
        while True:
            self.tecla_premuda = False
            while not self.tecla_premuda:
                self.pinta()
                self.teclat()
                self.w.update()
                time.sleep(1/60)
            
            if self.tecla_3:
                self.instruccions()
            else:
                break