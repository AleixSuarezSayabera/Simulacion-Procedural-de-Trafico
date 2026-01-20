import math
import random
from worldview.WorldView import *
from carretera.Tram import Tram

class Cotxe:
    def __init__(self, x, y, w, h, tram_inicial, color,v=0):
        self.color=color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.tram_actual=tram_inicial
        self.angle=self.tram_actual.theta
        self.distancia_en_tram=0
        self.carril_actual=0

    def mou(self):
        if self.tram_actual.seguent is None:
            self.v = 0 
            return
        
        long_tram = self.tram_actual.long
        self.distancia_en_tram += self.v

        while self.distancia_en_tram >= long_tram:
            self.distancia_en_tram -= long_tram

            if self.tram_actual.seguent is None:
                return
            
            if self in self.tram_actual.cotxes:
                self.tram_actual.cotxes.remove(self)
            
            self.tram_actual = self.tram_actual.seguent
            self.tram_actual.cotxes.append(self)

            self.angle = self.tram_actual.theta
            long_tram = self.tram_actual.long

        if long_tram > 0:
            t = self.distancia_en_tram/long_tram
            x_centre=self.tram_actual.x + t*(self.tram_actual.x_final-self.tram_actual.x)
            y_centre=self.tram_actual.y + t*(self.tram_actual.y_final-self.tram_actual.y)
            distancia_al_centre=self.carril_actual*(self.tram_actual.ample/5)
            angle_perp=self.tram_actual.theta+math.pi/2
            self.x=x_centre+distancia_al_centre*math.cos(angle_perp)
            self.y=y_centre+distancia_al_centre*math.sin(angle_perp)

    def distancia_recorreguda(self):
        dist_recorreguda=0
        tram_aux=self.tram_actual
        while tram_aux.anterior is not None:
            tram_aux=tram_aux.anterior
            dist_recorreguda+=tram_aux.long
        return dist_recorreguda
    
    def canvi_carril(self):
        if random.choice([True, False]):
            if self.carril_actual < 2:
                self.carril_actual += 1
            elif self.carril_actual > -2:
                self.carril_actual -= 1
        else:
            if self.carril_actual > -2:
                self.carril_actual -= 1
            elif self.carril_actual < 2:
                self.carril_actual += 1
    
    def distancia_per_recorrer(self):
        dist_per_recorrer=0
        tram_aux=self.tram_actual
        while tram_aux.seguent is not None:
            tram_aux=tram_aux.seguent
            dist_per_recorrer+=tram_aux.long
        return dist_per_recorrer
    


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

        
        w.create_polygon(puntos_vista, fill=self.color, outline='black')
        x_linea = 0.25 * self.w
        
        rx1 = x_linea * cos_a - (-half_h) * sin_a
        ry1 = x_linea * sin_a + (-half_h) * cos_a
        p1 = wv.worldToViewXY(self.x + rx1, self.y + ry1)
        
        rx2 = x_linea * cos_a - half_h * sin_a
        ry2 = x_linea * sin_a + half_h * cos_a
        p2 = wv.worldToViewXY(self.x + rx2, self.y + ry2)
        
        w.create_line(p1.x, p1.y, p2.x, p2.y, fill='black', width=2)