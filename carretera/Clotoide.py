import math
from carretera.Tram import Tram

class Clotoide:
    def __init__(self, x0, y0, theta0, L, theta_final, ample=100, ds=10.0):
        self.x0=x0
        self.y0=y0
        self.theta0=theta0
        self.L=L
        self.theta_final=theta_final
        self.ample=ample
        self.ds=ds

        self.delta_theta=theta_final-theta0

        self.A2=(L*L)/(2*abs(self.delta_theta)) 
        #La clotoide es una corba que compleix el següent, la seva curvatura creix linealment segons la distància
        #recorreguda, això a l'hora de construïr carreteres és útil, ya que si partim d'un tram recte, i enganxem
        #aquest amb una clotoide, el moviment de volant que farem és lineal, no farem moviments bruscos.

        #Per fer aquest càlcul de la clotoide, utilitzo que aquesta queda determinada per la seva longitud d'arc (L) desitjada
        #i l'angle al que es vol arribar
        #Es compleix en general que l'increment de theta segons s és theta=s^2/2A^2
        #La corvatura de la clotoide creix linealment amb escala 1/A^2

        self.signo = 1 if self.delta_theta > 0 else -1
        self.trams = self._generar_trams()

    def _generar_trams(self):
        trams = []
        x=self.x0
        y=self.y0
        s=0
        while s<self.L: #integració númerica de theta amb Euler, fins a arribar a L
            theta=self.theta0+self.signo*(s*s)/(2*self.A2)
            #aqui utilitzo que theta=theta0+s^2/2A^2, sabent l'angle local solament cal anar sumant els diferents vectors
            #de cada pas per calcular els punts x,y de la clotoide

            dx=self.ds*math.cos(theta)
            dy=self.ds*math.sin(theta)
            x_seguent=x+dx
            y_seguent=y+dy

            long = math.dist((x, y), (x_seguent, y_seguent))
            trams.append(Tram(x, y, long, self.ample, theta))

            x,y=x_seguent,y_seguent
            s+=self.ds
        return trams