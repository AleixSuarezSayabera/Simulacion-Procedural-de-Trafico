import math
from carretera.Clotoide import Clotoide
from carretera.Osculador import Osculador

#La idea del gir és dividir-ho en tres parts, clotoide-cercle osculador-clotoide
#per fer això nomès necesitem la longitud de cada clotoide, el radi del cercle i l'angle de gir total
#aquest angle cal repartir-ho entre el cercle i les clotoides de forma que el gir sigui el més suau posible

class Gir:
    def __init__(self, x0, y0, theta0, theta_final, R, L_c_inicial, L_c_final, ample=100, ds=10):
        self.x0=x0
        self.y0=y0
        self.theta0=theta0
        self.theta_final=theta_final
        self.R=R
        self.L_c_inicial=L_c_inicial
        self.L_c_final=L_c_final
        self.ample=ample
        self.ds=ds

        self.delta_theta = theta_final - theta0
        self.signe = 1 if self.delta_theta > 0 else -1

        self.delta_theta_c_inicial=(L_c_inicial/(2*R))*self.signe
        self.delta_theta_c_final=(L_c_final/(2*R))*self.signe

        self.delta_theta_R = self.delta_theta - self.delta_theta_c_inicial - self.delta_theta_c_final
        self.L_R = abs(self.delta_theta_R)*R

        self.trams = []
        self._generar()

    def _generar(self):
        c_inicial = Clotoide(self.x0, self.y0,
                             self.theta0,self.L_c_inicial,
                             self.theta0+self.delta_theta_c_inicial,
                             self.ample, self.ds)
        self.trams.extend(c_inicial.trams)
        x1=c_inicial.trams[-1].x_final
        y1=c_inicial.trams[-1].y_final 
        theta1=c_inicial.trams[-1].theta

        osc = Osculador(x1, y1, theta1,
                        self.R,
                        theta1+self.delta_theta_R,
                        self.ample, self.ds)
        self.trams.extend(osc.trams)
        x2=osc.trams[-1].x_final
        y2=osc.trams[-1].y_final
        theta2=osc.trams[-1].theta

        c_final=Clotoide(x2, y2, theta2,
                        self.L_c_final,
                        theta2 + self.delta_theta_c_final,
                        self.ample, self.ds)
        self.trams.extend(c_final.trams)
        self.x_final=c_final.trams[-1].x_final
        self.y_final=c_final.trams[-1].y_final
        self.theta_final_real=c_final.trams[-1].theta