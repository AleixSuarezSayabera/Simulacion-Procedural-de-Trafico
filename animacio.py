from tkinter import *

from juego.joc import Joc
from juego.ModeCrear import ModeCrear
from juego.Menu import Menu



tk = Tk()
w = Canvas(tk, width=800, height=600, bg="green")
w.pack()
while True:
    menu = Menu(tk, w)
    menu.mostrar()
        
    if menu.tecla_esc:
        break
    elif menu.tecla_1:
        joc = Joc("carretera.json", w)
        joc.bucle()
    elif menu.tecla_2:
        mode_pintar = ModeCrear("carretera.json", w)
        mode_pintar.bucle()
    elif menu.tecla_3:
        menu.instruccions()