import keyboard
import time
import json

from .joc import Joc
from carretera.Carretera import Carretera

from worldview.VPoint import *
from worldview.WPoint import *
from worldview.WorldView import *

class ModeCrear:
    def __init__(self, json, w):
        self.w=w
        self.json=json
        self.carretera=self.crear_carretera()
        self.ample_pantalla=8000
        self.altura_pantalla=6000
        
        self.x=0
        self.y=0
        self.camera_velocitat=150
        self.pantalla()
        self.tecla_amunt=False
        self.tecla_avall=False
        self.tecla_esq=False
        self.tecla_dre=False
        self.tecla_espai=False
        self.sortir=False
        for _ in range(20):
            self.carretera.generar_tram(True)
            self.carretera.generar_gir(True)
    
    def crear_carretera(self):
        f=open(self.json, "r")
        dades=json.load(f)
        return Carretera(dades['cars']['start_position']['x'],dades['cars']['start_position']['y'],dades['carretera']['lambda'],
                        dades['carretera']['angle_gir'],dades['carretera']['R_min'],dades['carretera']['R_max'],
                        dades['carretera']['L_c_min'],dades['carretera']['L_c_max'],
                        dades['carretera']['L_min'],dades['carretera']['L_max'])
    
    def pantalla(self):
        punt_dl_pantalla_x=self.x-self.ample_pantalla/2
        punt_dl_pantalla_y=self.y-self.altura_pantalla/2
        punt_ur_pantalla_x=self.x+self.ample_pantalla/2
        punt_ur_pantalla_y=self.y+self.altura_pantalla/2
        
        self.wv = WorldView(WPoint(punt_dl_pantalla_x, punt_dl_pantalla_y),WPoint(punt_ur_pantalla_x, punt_ur_pantalla_y),
            VPoint(0, 0),VPoint(800, 600),angle=0)
    
    def teclat(self):
        if keyboard.is_pressed("up arrow"):
            self.y += self.camera_velocitat
        
        if keyboard.is_pressed("down arrow"):
            self.y -= self.camera_velocitat
        
        if keyboard.is_pressed("left arrow"):
            self.x -= self.camera_velocitat
        
        if keyboard.is_pressed("right arrow"):
            self.x += self.camera_velocitat
        
        if keyboard.is_pressed("space"):
            if not self.tecla_espai:
                self.carretera.generar_tram(True)
                self.carretera.generar_gir(True)
                self.tecla_espai = True
        else:
            self.tecla_espai = False

        if keyboard.is_pressed("d"):
            self.carretera.eliminar_trams(10)

        
        if keyboard.is_pressed("esc"):
            self.sortir = True
    
    def actualitzar_camera(self):
        nueva_wMin_x = self.x - (self.ample_pantalla / 2)
        nueva_wMin_y = self.y - (self.altura_pantalla / 2)
        
        self.wv.wMin.x = nueva_wMin_x
        self.wv.wMin.y = nueva_wMin_y
        self.wv.wMax.x = nueva_wMin_x + self.ample_pantalla
        self.wv.wMax.y = nueva_wMin_y + self.altura_pantalla
    
    def pinta(self):
        self.w.delete("all")
        self.carretera.pinta(self.w, self.wv)
        for cotxe in self.carretera.cotxes:
            cotxe.pinta(self.w, self.wv)

        self.w.create_rectangle(5, 5, 180, 120, fill="black", stipple="gray50")
        titulo_font = ("Arial", 12, "bold")
        texto_font = ("Arial", 10)
        self.w.create_text(15, 15, text="CONTROLS", fill="orange", font=titulo_font, anchor="nw")
        controles = [
            "• ESPAI: Generar tram i gir",
            "• D: Eliminar trams",
            "• ESC: Tornar al menú"
        ]
        for i, texto in enumerate(controles):
            self.w.create_text(15, 45 + (i * 20), text=texto, fill="white", font=texto_font, anchor="nw")
    
    def executar_frame(self):
        if self.sortir:
            return False
        self.teclat()
        self.actualitzar_camera()
        self.carretera.mou()
        self.pinta()
        return True
    
    def bucle(self):
        while self.executar_frame():
            self.w.update()
            time.sleep(1 / 60)