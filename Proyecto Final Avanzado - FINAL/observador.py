#________________________

     #MODULOS IMPORTADOS             ----------   OBSERVADOR  -----------
#_________________________

import datetime

#________________________

     #OBSERVADOR - ANOTA: check.txt (inicio/cerrado).
#_________________________

#Utiliza clase ObservaAplica en controlador para ejecutar.

class Observador:
    @staticmethod
    def notificar(evento):
        timestamp = datetime.datetime.now()
        with open("check.txt", "a") as log:
            log.write(f"{timestamp}: {evento}\n")

