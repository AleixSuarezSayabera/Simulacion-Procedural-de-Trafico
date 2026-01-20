from tkinter import *
import time
import json
import keyboard
import math

from coche.Cotxe import Cotxe
from coche.Jugador import Jugador

from carretera.Tram import Tram
from carretera.Carretera import Carretera

from worldview.VPoint import *
from worldview.WPoint import *
from worldview.WorldView import *


class Joc:
    def __init__(self, json,w):
        self.json=json
        self.w=w
        self.jugador = self.lectura_json()
        self.carretera = self.jugador.carretera
        
        self.ample_pantalla = 1200
        self.altura_pantalla = 800
        
        self.pantalla()

    def lectura_json(self):
        f = open(self.json, "r")
        dades = json.load(f)
        f.close()
        aux = Carretera(dades['cars']['start_position']['x'],dades['cars']['start_position']['y'],dades['carretera']['lambda'],
                        dades['carretera']['angle_gir'],dades['carretera']['R_min'],dades['carretera']['R_max'],
                        dades['carretera']['L_c_min'],dades['carretera']['L_c_max'],
                        dades['carretera']['L_min'],dades['carretera']['L_max'])
        jugador=Jugador(dades['cars']['start_position']['x'], dades['cars']['start_position']['y'],
                        dades['cars']['width'],dades['cars']['height'],aux,dades['cars']['vides'],
                        dades['cars']['increment'],dades['cars']['velocitat'])
        return jugador
    
    def pantalla(self):
        dx = self.jugador.x
        dy = self.jugador.y
        
        punt_dl_pantalla_x=dx-self.ample_pantalla/2
        punt_dl_pantalla_y=dy-self.altura_pantalla/2
        punt_ur_pantalla_x=dx+self.ample_pantalla/2
        punt_ur_pantalla_y=dy+self.altura_pantalla/2
        
        self.wv = WorldView(WPoint(punt_dl_pantalla_x, punt_dl_pantalla_y), WPoint(punt_ur_pantalla_x, punt_ur_pantalla_y),
               VPoint(0, 0), VPoint(800, 600),angle=0)
    

    def actualitzar_camera(self):
        self.jugador.mou()
        self.jugador.puntuacio+=self.jugador.v
        self.jugador.v_max += self.jugador.increment

        self.carretera.mou()

        self.wv.set_rotation(self.jugador.angle-math.pi/2, self.jugador.x, self.jugador.y)
        
        nova_wMin_x = self.jugador.x-(self.ample_pantalla/2)
        nova_wMin_y = self.jugador.y-(self.altura_pantalla/2)
        
        self.wv.wMin.x = nova_wMin_x
        self.wv.wMin.y = nova_wMin_y
        self.wv.wMax.x = nova_wMin_x+self.ample_pantalla
        self.wv.wMax.y = nova_wMin_y+self.altura_pantalla
    
    
    def pinta(self):
        self.w.delete("all")

        self.carretera.pinta(self.w, self.wv)
        self.jugador.pinta(self.w, self.wv)
        
        for cotxe in self.carretera.cotxes:
            cotxe.pinta(self.w, self.wv)
        
        self.w.create_rectangle(10, 10, 220, 90, fill="black", stipple="gray50")
        
        color_vides = "red" if self.jugador.vides <= 1 else "white"
        self.w.create_text(20, 30, text=f"VIDES: {self.jugador.vides}", 
                           fill=color_vides, font=("Arial", 18, "bold"), anchor="nw")
        
        self.w.create_text(20, 60, text=f"PUNTUACIÓ: {self.jugador.puntuacio:.1f}", 
                           fill="yellow", font=("Arial", 14, "bold"), anchor="nw")
    
    def executar_frame(self):
        if self.jugador.game_over:
            return False
        
        self.jugador.teclat()
        self.actualitzar_camera()
        self.jugador.gestionar_carretera()
        self.jugador.gestionar_colisions()
        self.pinta()
        
        return True
    
    def bucle(self):
        while self.executar_frame():
            self.w.update()
            time.sleep(1/60)