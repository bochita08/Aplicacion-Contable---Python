#________________________

     #MODULOS IMPORTADOS          ----------   CLIENTE 1 -----------
#_________________________

import socket
import sys

     #Configuracion HOST/PUERTO
#_________________________

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#_________________________
# MENSAJE
#_________________________

mensaje = "Esta aplicacion es para el uso de control de clientes para un estudio contable."

sock.sendto(mensaje.encode("UTF-8"), (HOST, PORT))
received = sock.recvfrom(1024)

# ===== ENVIO Y RECEPCIÓN DE DATOS =================
 
print(received )
# ===== FIN ENVIO Y RECEPCIÓN DE DATOS =================