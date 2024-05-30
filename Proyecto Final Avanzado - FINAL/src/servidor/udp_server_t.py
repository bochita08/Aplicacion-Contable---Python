#________________________

     #MODULOS IMPORTADOS             ----------   OBSERVADOR  -----------
#_________________________

import socketserver
from pathlib import Path
import binascii

# global HOST
global PORT

#________________________

#           ----------   SERVER  -----------
#_________________________

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Bienvenido a mi aplicacion Contable realizada con Python")
        data = self.request[0].strip()
        socket = self.request[1]

        # ####################################################
        #   Hexa
        # ####################################################
        binary_field = bytearray(data)
        print("Si viene como bytearray")
        print("Valor recibido: ", binascii.hexlify(binary_field).decode("utf-8"))

        print("--------------------------------------")
        # ####################################################
        #   String
        # ####################################################
    
        print(data)
        print("--------------------------------------")

        # ####################################################
        #   Paquete e
        # ####################################################

        value2 = 0xA0
        packed_data_2 = bytearray()
        packed_data_2 += value2.to_bytes(1, "big")
        socket.sendto(packed_data_2, self.client_address)
        print("--Mensaje Enviado--")


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
