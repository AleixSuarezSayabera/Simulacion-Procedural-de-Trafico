#La carpeta base sempre és la mateixa per a tots els fitxers, així que si volem importar WPoint i VPoint, encara que aquest fitxer  
#estigui a la mateixa carpeta que WPoint i VPoint, hem d'indicar que està a la subcarpeta worldview
from worldview.WPoint import *
from worldview.VPoint import *

# --- Clase principal WorldView ---

class WorldView:
    """
    Classe que gestiona la finestra de Pantalla (VX/VY) i la finestra del Món (WX/WY), 
    amb mètodes per transformar punts entre tots dos sistemes de coordenades.
    """

    #Constructor que rep 2 WPoint i 2 VPoint
    def __init__(self, wMin, wMax, vMin, vMax,angle=0):
        self.wMin = wMin
        self.wMax = wMax
        self.vMin = vMin
        self.vMax = vMax
        self.rotacio=angle
        self.centre_rotacio=None
       
    #Mostra totes les dades quan fem un print d'aun objecte d'aquesta classe
    def __repr__(self) :
        s = f"World=({self.wMin.x},{self.wMin.y}) a ({self.wMax.x},{self.wMax.y}) "
        s += f"View=({self.vMin.x},{self.vMin.y}) a ({self.vMax.x},{self.vMax.y})"
        return s

    # --- Transformacions -------------------
    def set_rotation(self, angle, x_centre, y_centre):
        self.rotacio = angle
        self.centre_rotacio = (x_centre, y_centre)

    #Transfromada Word to View  (món a pantalla)
    def worldToView(self, Wp: WPoint) -> VPoint:

        if self.rotacio != 0 and self.centre_rotacio:
            x=Wp.x-self.centre_rotacio[0]
            y=Wp.y-self.centre_rotacio[1]
            cos_r=math.cos(-self.rotacio)
            sin_r=math.sin(-self.rotacio)
            x_rot=x*cos_r-y*sin_r
            y_rot=x*sin_r+y*cos_r

            Wp = WPoint(x_rot + self.centre_rotacio[0], 
                       y_rot + self.centre_rotacio[1])
        
        wy = self.wMax.y - Wp.y
       
        scale_x = (self.vMax.x - self.vMin.x) / (self.wMax.x - self.wMin.x) if (self.wMax.x - self.wMin.x) != 0 else 0.0
        scale_y = (self.vMax.y - self.vMin.y) / (self.wMax.y - self.wMin.y) if (self.wMax.y - self.wMin.y) != 0 else 0.0

        vx = int((Wp.x - self.wMin.x) * scale_x + self.vMin.x)
        vy = int(wy * scale_y + self.vMin.y)
        return VPoint(vx, vy)

    #Permet transformar a partir de 2 valors x,y en lloc d'un WPoint 
    def worldToViewXY(self, x: float, y: float) -> VPoint:      
        return self.worldToView(WPoint(x, y))

    #Transfromada View to World (pantalla a món)
    def viewToWorld(self, Vp: VPoint) -> WPoint:
        vy = self.vMax.y - Vp.y

        denom_x = (self.vMax.x - self.vMin.x)
        denom_y = (self.vMax.y - self.vMin.y)

        wx = ((Vp.x - self.vMin.x) * (self.wMax.x - self.wMin.x) / denom_x) + self.wMin.x if denom_x != 0 else self.wMin.x
        wy = ((vy - self.vMin.y) * (self.wMax.y - self.wMin.y) / denom_y) + self.wMin.y if denom_y != 0 else self.wMin.y

        return WPoint(wx, wy)

    #Permet transformar a partir de 2 valors x,y en lloc d'un VPoint
    def viewToWorldXY(self, x: int, y: int) -> WPoint:
        return self.viewToWorld(VPoint(x, y))
    
    #Permet desplaçar la finestra del World (món)
    def translateWindow(self,dx,dy):
        self.wMin.x+=dx
        self.wMax.x+=dx
        self.wMin.y+=dy
        self.wMax.y+=dy
