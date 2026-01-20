import math
from carretera.Tram import Tram

class Osculador:
    def __init__(self, x0, y0, theta0, R, theta_final, ample=100, ds=10.0):
        self.x0=x0
        self.y0=y0
        self.theta0=theta0
        self.R=R
        self.theta_final=theta_final
        self.ample=ample
        self.ds=ds

        self.delta_theta=theta_final-theta0

        self.signo = 1 if self.delta_theta > 0 else -1
        self.L=abs(self.delta_theta)*R

        self.trams=self._generar_trams()

    def _generar_trams(self):
        trams=[]

        x=self.x0
        y=self.y0
        theta=self.theta0

        s=0
        while s < self.L: #l'idea d'aquest càlcul és la mateixa que la de la clotoide, utilitzo que theta=tehta0+ds/R
            theta = self.theta0+self.signo*(s/self.R)

            dx=self.ds*math.cos(theta)
            dy=self.ds*math.sin(theta)

            x_seguent=x+dx
            y_seguent=y+dy

            long=math.dist((x,y),(x_seguent,y_seguent))
            trams.append(Tram(x,y,long,self.ample,theta))
            x,y=x_seguent,y_seguent
            s+=self.ds

        return trams