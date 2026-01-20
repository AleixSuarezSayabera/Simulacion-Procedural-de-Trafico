import math

from worldview.LinearEquation import *
from worldview.WPoint import *

class Tram:
    def __init__(self,x,y,long,ample,theta):
        self.x=x
        self.y=y
        self.long=long
        self.theta=theta
        self.ample=ample
        p_inicial=WPoint(x, y)
        self.obstacles=[]
        self.cotxes=[]
        self.recta_centre = LinearEquation(theta, p_inicial)

        self.x_final=x+long*math.cos(theta)
        self.y_final=y+long*math.sin(theta)

        self.anterior=None
        self.seguent=None
        angle_perp = self.theta + math.pi / 2
        dx = (self.ample / 2) * math.cos(angle_perp)
        dy = (self.ample / 2) * math.sin(angle_perp)
        
        self.v00 = (self.x - dx, self.y - dy)
        self.v10 = (self.x + dx, self.y + dy)
        self.v11 = (self.x_final + dx, self.y_final + dy)
        self.v01 = (self.x_final - dx, self.y_final - dy)


    def pinta(self, w, wv): 
        v1 = wv.worldToViewXY(self.x, self.y)
        v2 = wv.worldToViewXY(self.x_final, self.y_final)
        w.create_line(v1.x,v1.y,v2.x,v2.y, fill="white", width=2)
        