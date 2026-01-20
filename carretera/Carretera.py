import math
import random
import numpy as np
from coche.Cotxe import Cotxe
from carretera.Tram import Tram
from carretera.Clotoide import Clotoide
from carretera.Osculador import Osculador
from carretera.Gir import Gir

class Carretera:
    def __init__(self, x_inicial, y_inicial,lmbda,angle_gir,R_min,R_max,L_c_min,L_c_max,L_min,L_max):
        self.x_actual=x_inicial
        self.y_actual=y_inicial
        self.lmbda=lmbda
        self.theta_actual=math.pi/2
        self.cotxes=[]
        self.trams=[]
        self.primer_tram = None
        self.ultim_tram = None
        self.angle_gir=angle_gir
        self.R_min=R_min
        self.R_max=R_max
        self.L_c_min=L_c_min
        self.L_c_max=L_c_max
        self.L_min=L_min
        self.L_max=L_max

        self.generar_tram(False)
        self.generar_gir(True)

        for _ in range(3):
            self.generar_tram(True)
            self.generar_gir(True)

    def generar_gir(self,bots):
        delta_theta=random.uniform(-self.angle_gir, self.angle_gir)
        theta_final=self.theta_actual + delta_theta

        R = random.uniform(self.R_min, self.R_max)
        L_c_inicial=random.uniform(self.L_c_min, self.L_c_max)
        L_c_final=random.uniform(self.L_c_min, self.L_c_max)

        gir=Gir(self.x_actual, self.y_actual, self.theta_actual, theta_final,
                R, L_c_inicial, L_c_final,ample=200, ds=10)
        self.connectar(gir.trams)
        if bots==True:
            num_cotxes=np.random.poisson(self.lmbda)
            for _ in range(num_cotxes):
                tram_aleatori=random.choice(gir.trams)
                dist=random.uniform(0, tram_aleatori.long)
                bot=self.generar_cotxe(tram_aleatori, dist)
                tram_aleatori.cotxes.append(bot)

        self.x_actual=gir.x_final
        self.y_actual=gir.y_final
        self.theta_actual=gir.theta_final_real

    def generar_tram(self,bots):
        long=random.uniform(self.L_min,self.L_max)
        tram_nou=Tram(self.x_actual,self.y_actual,long,200,self.theta_actual)

        if self.ultim_tram:
            self.ultim_tram.seguent = tram_nou
            tram_nou.anterior = self.ultim_tram
        else:
            self.primer_tram = tram_nou
        
        self.ultim_tram = tram_nou
        self.trams.append(tram_nou)
        self.x_actual=tram_nou.x_final
        self.y_actual=tram_nou.y_final
        if bots==True:
            num_cotxes=np.random.poisson(self.lmbda)
            distancies=[random.uniform(0, tram_nou.long) for _ in range(num_cotxes)]
            for dist in distancies:
                bot=self.generar_cotxe(tram_nou, dist)
                tram_nou.cotxes.append(bot)

    def generar_cotxe(self,tram,dist):
        carril=random.randint(-2, 2)
        t=dist/tram.long
        x_centre=tram.x + t*(tram.x_final-tram.x)
        y_centre=tram.y + t*(tram.y_final-tram.y)
        v=random.randint(10,15)
        w=random.uniform(20,40)
        h=random.uniform(18,23)
        llista_colors = ["white", "black", "grey", "lightblue", 
                 "red", "navy", "blue", "darkred"]
        color=random.choice(llista_colors) 
        bot=Cotxe(x_centre,y_centre,w,h,tram,color,v)
        bot.carril_actual=carril
        bot.distancia_en_tram=dist
        self.cotxes.append(bot)
        return bot

    def connectar(self, nous_trams):
        for i, tram in enumerate(nous_trams):
            if i>0:
                nous_trams[i-1].seguent=tram
                tram.anterior = nous_trams[i-1]
            if i==0 and self.ultim_tram:
                self.ultim_tram.seguent=tram
                tram.anterior=self.ultim_tram
            if i==len(nous_trams)-1:
                self.ultim_tram=tram

            self.trams.append(tram)
            if not self.primer_tram:
                self.primer_tram=tram

    def eliminar_trams(self, n):
        for _ in range(n):
            tram_fora=self.trams.pop(0)
            for c in list(tram_fora.cotxes):
                if c in list(self.cotxes):
                    self.cotxes.remove(c)
            self.primer_tram=tram_fora.seguent
            self.primer_tram.anterior=None

    def obtindre_punts(self, wv):
        punts_esq = []
        punts_dre = []
        for t in self.trams:
            v_esq=wv.worldToViewXY(t.v00[0], t.v00[1])
            v_dre=wv.worldToViewXY(t.v10[0], t.v10[1])
            punts_esq.append((v_esq.x, v_esq.y))
            punts_dre.append((v_dre.x, v_dre.y))

        t_ultim = self.trams[-1]
        v_final_esq = wv.worldToViewXY(t_ultim.v01[0], t_ultim.v01[1])
        v_final_dre = wv.worldToViewXY(t_ultim.v11[0], t_ultim.v11[1])
        punts_esq.append((v_final_esq.x, v_final_esq.y))
        punts_dre.append((v_final_dre.x, v_final_dre.y))

        return punts_esq + punts_dre[::-1]
    
    def pinta(self, w, wv):
        punts = self.obtindre_punts(wv)
        punts_plans = [coord for p in punts for coord in p]
        w.create_polygon(punts_plans, fill="grey", outline="black")
        for t in self.trams:
            t.pinta(w,wv)



    def mou(self):
        for c in list(self.cotxes):
            if c.v==0:
                self.cotxes.remove(c)
                c.tram_actual.cotxes.remove(c)
            else:
                c.mou()

    def colisio(self,jugador):
        if jugador.tram_actual in self.trams:
            for c in jugador.tram_actual.cotxes:
                if c == jugador or c not in self.cotxes:
                    continue
                if c.carril_actual == jugador.carril_actual:
                    dist = abs(c.distancia_en_tram - jugador.distancia_en_tram)
                    if dist < 40:  # ⭐ Colisión del jugador
                        return True
        for c1 in self.cotxes:
            if c1.tram_actual not in self.trams:
                continue
            for c2 in c1.tram_actual.cotxes:
                if c1 == c2: 
                    continue
                if c1.carril_actual == c2.carril_actual:
                    dist = c2.distancia_en_tram - c1.distancia_en_tram
                    if c1 != jugador and c2 != jugador:
                        if 0 < dist < 60: 
                            c1.canvi_carril()
                        if -60 < dist < 0:
                            c2.canvi_carril()