#________________________

     #MODULOS IMPORTADOS             ----------   CONTROLADOR  -----------
#_________________________

from tkinter import Tk
import vista
#________________________

     #CONTROLADOR / LANZAMIENTO
#_________________________

class Controller():
    def __init__(self, root_w):
        self.root = root_w

        # Ejecucion vista de la aplicacion
        self.objeto_vista = vista.VistaPrincipal(self.root)

        # Agregar reloj en la parte inferior
        self.clock = vista.Clock(self.root)

if __name__ == "__main__":
    root = Tk()
    aplicacion = Controller(root)
    root.mainloop()

