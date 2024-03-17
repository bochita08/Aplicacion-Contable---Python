#________________________

     #MODULOS IMPORTADOS          ----------   VISTA -----------
#_________________________

from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
from tkinter.messagebox import *
from modelo import FuncionesBotonera

#________________________

     #VISTA VISTA VISTA
#_________________________

class VistaPrincipal(Frame):
    def __init__(self, window):
        super().__init__(window)
        self.root = window
        self.root.title("Registro De Clientes - Estudio Contable 🏛️ ")
        self.root.configure(bg="#3157FF")
        self.objeto_botones = FuncionesBotonera()
        self.crear_interfaz()

        style = ttk.Style()
        style.configure('Treeview', background='#D6ECFA', foreground='black', font=('Arial', 10, 'bold'))

        # Agregar reloj en la parte inferior con grid
        self.clock = Clock(self.root)
        self.clock.grid(row=500, column=0, columnspan=7, sticky="we")

   
    def crear_interfaz(self):
        row_offset = 1

        self.titulo = Label(self.root, text="Plantilla de clientes - Ingrese sus datos", font=("Arial", 16, "bold"), fg="black", bg="white")
        self.titulo.grid(row=0, column=0, columnspan=6, pady=(10, 10), sticky="we")

        # Variables de control
        self.a_val = StringVar()
        self.b_val = StringVar()
        self.c_val = StringVar()
        self.d_val = StringVar()
        self.e_val = StringVar()

        self.entrada1 = self.crear_fila_entrada("Nombre", self.a_val, width=30)
        self.entrada2 = self.crear_fila_entrada("Apellido", self.b_val, width=30)
        self.entrada3 = self.crear_fila_entrada("Rubro/Oficio", self.c_val, width=30)
        self.entrada4 = self.crear_fila_entrada("CUIT/CUIL", self.d_val, width=30)
        self.entrada5 = self.crear_fila_entrada_contrasena("Clave Fiscal", self.e_val, width=30)

#________________________

    #TREEVIEWS
#_________________________

        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
        self.tree.column("#0", width=40, minwidth=40, anchor=W)

        for col in ("col1", "col2", "col3", "col4", "col5"):
            self.tree.column(col, width=150, minwidth=150, anchor=W)
        
        self.tree.column("col1", width=150, minwidth=150, anchor=W)
        self.tree.column("col2", width=150, minwidth=150, anchor=W)
        self.tree.column("col3", width=150, minwidth=150, anchor=W)
        self.tree.column("col4", width=150, minwidth=150, anchor=W)
        self.tree.column("col5", width=150, minwidth=150, anchor=W)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Nombre")
        self.tree.heading("col2", text="Apellido")
        self.tree.heading("col3", text="Rubro / Oficio")
        self.tree.heading("col4", text="CUIT / CUIL")
        self.tree.heading("col5", text="Clave Fiscal")
        self.tree.grid(row=row_offset + 5, column=0, columnspan=6, pady=(10, 10))
        
        # Agregar imagenes
        self.imagen = PhotoImage(file="cpn.png", width=300, height=500)
        self.imagen_label = Label(self.root, image=self.imagen, bg="white")
        self.imagen_label.grid(row=0, column=6, rowspan=8, padx=5, pady=5, sticky="e")
    
        self.imagen_afip = PhotoImage(file="afip.png")
        self.label_imagen_afip = Label(self.root, image=self.imagen_afip, bg="white")
        self.label_imagen_afip.grid(row=row_offset, column=2, rowspan=5, padx=(0, 10), pady=(0, 10), sticky="W")
    
        # Integración de la clase Botones
        self.botones = Botones(self.root, self.objeto_botones, self.a_val, self.b_val, self.c_val, self.d_val, self.e_val, self.tree)
        
        # Agregar reloj en la parte inferior con grid
        self.clock = Clock(self.root)
        self.clock.place(x=0, y=500, relwidth=1, anchor="e")  # Colocar el reloj en la derecha
        
        # Función para crear una fila de entrada con un nombre y campo correspondiente
    def crear_fila_entrada(self, nombre, textvariable, width):
        frame = Frame(self.root, bg="white")
        frame.grid()
        label = Label(frame, text=nombre, bg="black", fg="white", width=20)
        label.grid(row=3, column=0, sticky=W)
        entry = Entry(frame, textvariable=textvariable, width=width)
        entry.grid(row=3, column=1, sticky=W)
        return frame

    # Función para crear una fila de entrada CONTRASEÑA correspondiente
    def crear_fila_entrada_contrasena(self, nombre, textvariable, width, show_char='*'):
        frame = Frame(self.root, bg="white")
        frame.grid()
        label = Label(frame, text=nombre, bg="black", fg="white", width=20)
        label.grid(row=4, column=0, sticky=W)
        entry = Entry(frame, textvariable=textvariable, width=width, show=show_char)
        entry.grid(row=4, column=4, sticky=W, padx=(0, 5))

        # Opcion de veo o no ver la clave fiscal
        show_password_var = BooleanVar()
        show_password_checkbox = Checkbutton(text="Mostrar contraseña", variable=show_password_var, command=lambda:self.objeto_botones.toggle_password(show_password_var, entry, show_char))
        show_password_checkbox.grid(row=5, column=1, sticky=W, padx=(5, 0))

#________________________

     #BOTONERA
#_________________________
#________________________________________
     #DECLARACION DE LOS DISTINTOS BOTONES
#_________________________

class Botones():
    def __init__(self, root, objeto_botones, a_val, b_val, c_val, d_val, e_val, tree):
        self.root = root
        self.objeto_botones = objeto_botones
        self.a_val = a_val
        self.b_val = b_val
        self.c_val = c_val
        self.d_val = d_val
        self.e_val = e_val
        self.tree = tree
        self.crear_botones()

    def crear_botones(self):
        row_offset = 1

     #ALTA
#_________________________
        self.boton_alta = self.crear_boton("Agregar Cliente", lambda:self.objeto_botones.alta(self.a_val, self.b_val, self.c_val, self.d_val, self.e_val, self.tree))
        self.boton_alta.grid(row=row_offset + 6, column=0, padx=(0, 10), pady=10)

     #ACTUALIZAR
#_________________________
        self.objeto_botones.actualizar_treeview(self.tree)  # Llamar a esta función para mostrar los datos

     #MODIFICAR
#_________________________
        self.boton_modificar = self.crear_boton("Modificar Cliente", lambda:self.objeto_botones.modificar(self.tree, self.a_val, self.b_val, self.c_val, self.d_val, self.e_val))
        self.boton_modificar.grid(row=row_offset + 6, column=2, padx=(0, 10), pady=10)

     #BORRAR
#_________________________
        self.boton_borrar = self.crear_boton("Eliminar Cliente", lambda:self.objeto_botones.borrar(self.tree))
        self.boton_borrar.grid(row=row_offset + 6, column=3, padx=(0, 10), pady=10)

     #MAXIMIZAR O MINIMIZAR
#_________________________
        self.boton_maximizar_minimizar = self.crear_boton("Max/Min", lambda:self.objeto_botones.maximizar_minimizar_ventana(self.tree))
        self.boton_maximizar_minimizar.grid(row=row_offset + 6, column=4, padx=(0, 10), pady=10)

     #INGRESO A AFIP
#_________________________        
        self.boton_afip = self.crear_boton("Ingreso a AFIP", self.objeto_botones.abrir_afip, bg="red", fg="white", font=('Arial', 14, 'bold'))
        self.boton_afip.grid(row=row_offset, column=3, rowspan=5, padx=(0, 10), pady=(0, 10), sticky="W")

     #CONSULTA
#_________________________        
  
        self.boton_consulta = self.crear_boton("Consultar Cliente", lambda:self.objeto_botones.consultar(self.tree, self.a_val, self.b_val, self.c_val, self.d_val, self.e_val))
        self.boton_consulta.grid(row=row_offset + 6, column=1, padx=(0, 10), pady=10)

    def crear_boton(self, text, command=None, **kwargs):
        default_kwargs = dict(bg="black", fg="white", font=('Arial', 10, 'bold'))
        default_kwargs.update(kwargs)
        return Button(self.root, text=text, command=command, **default_kwargs)
    
#__________________________________
    
     #DETALLE RELOJ INFERIOR CON FECHA
#_________________________  
    
class Clock(tk.Label):
    def __init__(self, parent):
        tk.Label.__init__(self, parent, font=('Arial', 12, 'bold'))
        self.parent = parent
        self.time_string = tk.StringVar()
        self.time_string.set(self.get_current_time())
        self.configure(textvariable=self.time_string)

        self.update_clock()

    def get_current_time(self):
        return time.strftime('%d/%m/%Y  -  %H:%M:%S')

    def update_clock(self):
        self.time_string.set(self.get_current_time())
        self.after(1000, self.update_clock)
