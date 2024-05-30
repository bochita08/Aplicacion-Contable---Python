
#________________________

     #MODULOS IMPORTADOS             ----------   DECORADORES -----------
#_________________________

import datetime
from tkinter.messagebox import showerror

#_______________________________________

     #DECORADORES PARA REGISTRO ERRORES EN.TXT
#________________________________________
     #REGISTROS DE ERRORES(errores.txt) / OPERACIONES DEL USUARIO (root.txt)
#_________________________

# Definimos la clase ManejoErrores.
class ManejoErrores:
    
    # Movimientos errores.
    @staticmethod
    def manejar_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                mensaje = f"Se ha producido un error: {str(e)}"
                ManejoErrores.registrar_error(mensaje)
                showerror("Error", mensaje)
        return wrapper
    
    #Funcion Union con de manejo de infromacion & guardado para uso como decorador.
    @staticmethod
    def manejar_movimiento(func):
        def wrapper(*args, **kwargs):
            try:
                resultado = func(*args, **kwargs)
                ManejoErrores.registrar_movimiento(resultado)
                return resultado
            except Exception as e:
                mensaje = f"Se ha producido un error: {str(e)}"
                ManejoErrores.registrar_error(mensaje)
                showerror("Error", mensaje)
        return wrapper

    #REGISTROS DE ERRORES(errores.txt) / OPERACIONES DEL USUARIO (root.txt).

    @staticmethod
    def registrar_error(mensaje):
        with open("errores.txt", "a") as log:
            log.write(f"{datetime.datetime.now()}: Error - {mensaje}\n")


    @staticmethod
    def registrar_movimiento(mensaje):
        if mensaje:
            with open("root.txt", "a") as log:
                log.write(f"{datetime.datetime.now()}: {mensaje}\n")



