#________________________

     #MODULOS IMPORTADOS             ----------   CONTROLADOR  -----------
#_________________________

from tkinter import Tk
import vista
import observador

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

        # Obsercador inicio/cerrado
        observador.Observador.notificar("La aplicacion ha sido iniciada")


class ObservaAplica():
    def cerrar_aplicacion():
            
        # Notificar al observador que la aplicación ha sido cerrada
        observador.Observador.notificar("La aplicacion ha sido cerrada")
        
        # Cerrar la aplicación
        root.quit()



if __name__ == "__main__":
    root = Tk()
    aplicacion = Controller(root)
    root.protocol("WM_DELETE_WINDOW", ObservaAplica.cerrar_aplicacion)
    root.mainloop()



