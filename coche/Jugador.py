import math
import time
import keyboard
from .Cotxe import Cotxe
from worldview.WorldView import *
from carretera.Tram import Tram

class Jugador(Cotxe):
    def __init__(self, x, y, w, h,carretera,vides,increment,v=0):
        super().__init__(x, y, w, h, carretera.primer_tram, v)
        self.carretera=carretera
        self.v=20
        self.v_max=20
        self.acceleracio=0.2
        self.vides=vides
        self.puntuacio=0
        self.increment=increment
        self.invulnerable=False
        self.temps_en_cd=0
        self.duracio_cd=2.0
        self.carril_actual=0
        self.game_over = False
        self.tecla_esq = False
        self.tecla_dre = False
        self.tecla_esc=False

    def gestionar_carretera(self):
        if self.distancia_recorreguda() > 2000:
            self.carretera.eliminar_trams(4)
        
        if self.distancia_per_recorrer() < 2000:
            self.carretera.generar_tram(True)
            self.carretera.generar_gir(True)
        
    def gestionar_colisions(self):
        temps = time.time()
        if not self.invulnerable:
            if self.carretera.colisio(self):
                self.vides-=1
                self.v=5
                self.invulnerable=True
                self.temps_en_cd=temps
                
                if self.vides <= 0:
                    print("GAME OVER")
                    self.game_over = True
        else:
            if temps - self.temps_en_cd > self.duracio_cd:
                self.invulnerable = False
        
        if not self.carretera.colisio(self) and self.v < self.v_max:
            self.v += self.acceleracio
    
    def tecla_esqu(self):
        if self.carril_actual<2:
            self.carril_actual+=1

    def tecla_dret(self):
        if self.carril_actual>-2:
            self.carril_actual-=1

    def teclat(self):
        if keyboard.is_pressed("esc"):
            if not self.tecla_esc:
                self.game_over=True
                self.tecla_esc = True
        else:
            self.tecla_esc = False

        if keyboard.is_pressed("left arrow"):
            if not self.tecla_esq:
                self.tecla_esqu()
                self.tecla_esq = True
        else:
            self.tecla_esq = False

        if keyboard.is_pressed("right arrow"):
            if not self.tecla_dre:
                self.tecla_dret()
                self.tecla_dre = True
        else:
                self.tecla_dre = False

    def pinta(self, w, wv):
        half_w = self.w / 2
        half_h = self.h / 2
        
        esquinas = [
            (-half_w, -half_h),
            (half_w, -half_h),
            (half_w, half_h),
            (-half_w, half_h)
        ]
        
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        
        puntos_vista = []
        for vx, vy in esquinas:
            rx = vx * cos_a - vy * sin_a
            ry = vx * sin_a + vy * cos_a
            p = wv.worldToViewXY(self.x + rx, self.y + ry)
            puntos_vista.extend([p.x, p.y])
        
        w.create_polygon(puntos_vista, fill='red', outline='maroon', width=2)
        
        x_linea = 0.25 * self.w
        
        rx1 = x_linea * cos_a - (-half_h) * sin_a
        ry1 = x_linea * sin_a + (-half_h) * cos_a
        p1 = wv.worldToViewXY(self.x + rx1, self.y + ry1)
        
        rx2 = x_linea * cos_a - half_h * sin_a
        ry2 = x_linea * sin_a + half_h * cos_a
        p2 = wv.worldToViewXY(self.x + rx2, self.y + ry2)
        
        w.create_line(p1.x, p1.y, p2.x, p2.y, fill='navy', width=3)
    