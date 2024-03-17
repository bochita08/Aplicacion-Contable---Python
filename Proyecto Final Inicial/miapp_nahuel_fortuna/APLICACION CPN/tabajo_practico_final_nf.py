#________________________

     #MODULOS IMPORTADOS
#_________________________
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import sqlite3
import re
import webbrowser
#________________________

     #MODELO PROPIO REGISTRO DE CLLIENTES
     #SOLO DE INGRESO A AFIP
#________________________________________
     #FUNCIONES 
#_________________________

#Conexion y creacion de tabla clientes con control de conexion.
def conexion():
    con = sqlite3.connect('base_contable.db')
    return con 

def crear_tabla(con):
    cursor = con.cursor()
    sql = "CREATE TABLE IF NOT EXISTS clientes(id INTEGER PRIMARY KEY AUTOINCREMENT, nombre varchar(50) NOT NULL, apellido varchar(50) NOT NULL, rubro varchar(200) NOT NULL, cuit integer NOT NULL, clave_fiscal varchar(30) NOT NULL)"
    cursor.execute(sql)
    con.commit()

try:
    con = conexion()
    crear_tabla(con)
except sqlite3.Error as e:
    print("ERROR DE CONEXION:", e)

def maximizar_minimizar_ventana():
    if tree.winfo_ismapped():
        tree.grid_remove()  # Ocultar la Treeview si está visible
    else:
        tree.grid()  # Mostrar la Treeview si está oculta


def validar_campos_vacios(a, b, c, d, e):
    if not a or not b or not c or not d or not e:
        mostrar_mensaje("Error", "Por favor, complete todos los campos antes de agregar un nuevo cliente.")
        return False
    return True

# Función de validación para permitir solo números
def validate_numeros(text):
    return text.isdigit() or text == ""

#ALTA
def alta(nombre, apellido, rubro, cuit, clave_fiscal, tree):
    if not validar_campos_vacios(nombre, apellido, rubro, cuit, clave_fiscal):
        return

    cadena = nombre
    patron = "^[A-Za-záéíóú]*$"
    if(re.match(patron, cadena)):
        con = conexion()
        cursor = con.cursor()
        data = (nombre, apellido, rubro, cuit, clave_fiscal)
        sql = "INSERT INTO clientes(nombre, apellido, rubro, cuit, clave_fiscal) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        print("Cliente cargado correctamente🤝")
        mostrar_mensaje("Éxito", "Cliente cargado correctamente")
        actualizar_treeview(tree)
    else:
        mostrar_mensaje("Error", "Lo siento... Ocurrió un ERROR, vuelva a intentarlo.")

#BORRAR
def borrar(tree):
    valor = tree.selection()
    if not valor:
        mostrar_mensaje("Error", "Por favor, seleccione un cliente para eliminar.")
        return

    respuesta = askquestion("Confirmar", "¿Estás seguro que deseas eliminar este cliente?")
    if respuesta == 'yes':
        item = tree.item(valor)
        mi_id = item['text']

        con = conexion()
        cursor = con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM clientes WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)
        mostrar_mensaje("Éxito", "Cliente eliminado correctamente")

#ACTUALIZAR
def actualizar_treeview(mi_tree_view):
    records = mi_tree_view.get_children()
    for element in records:
        mi_tree_view.delete(element)
    
    sql = "SELECT * FROM clientes ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        mi_tree_view.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5]))

#VENTANAS
def mostrar_mensaje(titulo, mensaje):
    showinfo(titulo, mensaje)

#MODIFICAMOS
def modificar(tree, a_val, b_val, c_val, d_val, e_val):
    valor = tree.selection()
    if not valor:
        mostrar_mensaje("Error", "Por favor, seleccione un cliente para modificar.")
        return

    item = tree.item(valor)
    mi_id = item['text']

    con = conexion()
    cursor = con.cursor()
    data = (a_val.get(), b_val.get(), c_val.get(), d_val.get(), e_val.get(), mi_id)
    sql = "UPDATE clientes SET nombre=?, apellido=?, rubro=?, cuit=?, clave_fiscal=? WHERE id=?;"
    cursor.execute(sql, data)
    con.commit()
    mostrar_mensaje("Éxito", "Cliente modificado correctamente")
    actualizar_treeview(tree)

#CONSULTA
def consultar(tree, a_val, b_val, c_val, d_val, e_val):
    valor = tree.selection()
    if not valor:
        mostrar_mensaje("Error", "Por favor, seleccione un cliente para consultar.")
        return

    item = tree.item(valor)
    mi_id = item['text']

    con = conexion()
    cursor = con.cursor()
    sql = "SELECT * FROM clientes WHERE id=?;"
    cursor.execute(sql, (mi_id,))
    cliente = cursor.fetchone()

    a_val.set(cliente[1])
    b_val.set(cliente[2])
    c_val.set(cliente[3])
    d_val.set(cliente[4])
    e_val.set(cliente[5])

def crear_marco_contenedor():
    marco_contenedor = Frame(root, bg="white")
    marco_contenedor.grid(row=row_offset + 5, column=0, columnspan=6, pady=(10, 10))
    

    # Configurar estilo del Treeview
    style = ttk.Style()
    style.configure('Treeview', background='#D6ECFA', foreground='black', font=('Arial', 10, 'bold'))

    # Crear Treeview dentro del marco contenedor
    tree = ttk.Treeview(marco_contenedor)
    tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
    tree.column("#0", width=40, minwidth=40, anchor=W)
    tree.column("col1", width=150, minwidth=150, anchor=W)
    tree.column("col2", width=150, minwidth=150, anchor=W)
    tree.column("col3", width=150, minwidth=150, anchor=W)
    tree.column("col4", width=150, minwidth=150, anchor=W)
    tree.column("col5", width=150, minwidth=150, anchor=W)

    tree.heading("#0", text="ID")
    tree.heading("col1", text="Nombre")
    tree.heading("col2", text="Apellido")
    tree.heading("col3", text="Rubro / Oficio")
    tree.heading("col4", text="CUIT / CUIL")
    tree.heading("col5", text="Clave Fiscal")
    tree.grid(row=0, column=0, columnspan=6, pady=(10, 10), padx=(10, 10), sticky="nsew")

    return tree
# Función para crear una fila de entrada con un nombre y campo correspondiente
def crear_fila_entrada(row, nombre, textvariable, width):
    label = Label(root, text=nombre, bg="black", fg="white")
    label.grid(row=row, column=0, sticky=W)
    entry = Entry(root, textvariable=textvariable, width=width, validate="key", validatecommand=(validate_numeros, "%P"))
    entry.grid(row=row, column=1, sticky=W)
    return entry

def crear_fila_entrada_contrasena(row, nombre, textvariable, width, show_char='*'):
    label = Label(root, text=nombre, bg="black", fg="white")
    label.grid(row=row, column=0, sticky=W)
    entry = Entry(root, textvariable=textvariable, width=width, show=show_char)
    entry.grid(row=row, column=1, sticky=W)
    
    show_password_var = BooleanVar()
    show_password_checkbox = Checkbutton(root, text="Mostrar contraseña", variable=show_password_var, command=lambda: toggle_password(show_password_var, entry, show_char))
    show_password_checkbox.grid(row=row, column=2, sticky=W)

    return entry

def toggle_password(show_password_var, entry, show_char):
    if show_password_var.get():
        entry.config(show="")
    else:
        entry.config(show=show_char)

#FUNCION PARA - Botón para ingresar a AFIP
def abrir_afip():
    webbrowser.open("https://www.afip.gob.ar/landing/default.asp")
#________________________

     #VISTA VISTA VISTA
#_________________________

root = Tk()
root.title("🏛️Registro De Clientes - Estudio Contable ")
root.configure(bg="#3157FF")  

# Agregar imagenes
row_offset = 1
imagen = PhotoImage(file="cpn.png", width=250, height=450)
imagen_label = Label(root, image=imagen, bg="white")
imagen_label.grid(row=0, column=6, rowspan=8, padx=5, pady=5, sticky="e")

imagen_afip = PhotoImage(file="afip.png")
label_imagen_afip = Label(root, image=imagen_afip, bg="white")
label_imagen_afip.grid(row=row_offset, column=2, rowspan=5, padx=(0, 10), pady=(0, 10), sticky="W")

titulo = Label(root, text="Plantilla de clientes - Ingrese sus datos", font=("Arial", 16, "bold"), fg="black", bg="white")
titulo.grid(row=0, column=0, columnspan=6, pady=(10, 10), sticky="we")

# Variables de control
a_val = StringVar()
b_val = StringVar()
c_val = StringVar()
d_val = StringVar() 
e_val = StringVar() 

# Crear filas de entrada, variando la de
entrada1 = crear_fila_entrada(row_offset + 0, "Nombre", a_val, 30)
entrada2 = crear_fila_entrada(row_offset + 1, "Apellido", b_val, 30)
entrada3 = crear_fila_entrada(row_offset + 2, "Rubro/Oficio", c_val, 30)
entrada4 = crear_fila_entrada(row_offset + 3, "CUIT/CUIL", d_val, 30)
entrada5 = crear_fila_entrada_contrasena(row_offset + 4, "Clave Fiscal", e_val, 30)





#________________________

     #TREEVIEWS
#_________________________
tree = ttk.Treeview(root)
tree = crear_marco_contenedor()
tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
tree.column("#0", width=40, minwidth=40, anchor=W)
tree.column("col1", width=150, minwidth=150, anchor=W)
tree.column("col2", width=150, minwidth=150, anchor=W)
tree.column("col3", width=150, minwidth=150, anchor=W)
tree.column("col4", width=150, minwidth=150, anchor=W)
tree.column("col5", width=150, minwidth=150, anchor=W)

tree.heading("#0", text="ID")
tree.heading("col1", text="Nombre")
tree.heading("col2", text="Apellido")
tree.heading("col3", text="Rubro / Oficio")
tree.heading("col4", text="CUIT / CUIL")
tree.heading("col5", text="Clave Fiscal")
tree.grid(row=row_offset + 5, column=0, columnspan=6, pady=(10, 10))

#________________________

     #BOTONERA
#_________________________
boton_alta = Button(root, text="Agregar Cliente", command=lambda:alta(a_val.get(), b_val.get(), c_val.get(), d_val.get(), e_val.get(), tree), bg="black", fg="white", font=('Arial', 10, 'bold'))
boton_alta.grid(row=row_offset + 6, column=0, padx=(0, 10), pady=10)

boton_consulta = Button(root, text="Consultar Cliente", command=lambda:consultar(tree, a_val, b_val, c_val, d_val, e_val), bg="black", fg="white", font=('Arial', 10, 'bold'))
boton_consulta.grid(row=row_offset + 6, column=1, padx=(0, 10), pady=10)

boton_modificar = Button(root, text="Modificar Cliente", command=lambda:modificar(tree, a_val, b_val, c_val, d_val, e_val), bg="black", fg="white", font=('Arial', 10, 'bold'))
boton_modificar.grid(row=row_offset + 6, column=2, padx=(0, 10), pady=10)

boton_borrar = Button(root, text="Eliminar Cliente", command=lambda:borrar(tree), bg="black", fg="white", font=('Arial', 10, 'bold'))
boton_borrar.grid(row=row_offset + 6, column=3, padx=(0, 10), pady=10)

boton_afip = Button(root, text="Ingreso a AFIP", command=abrir_afip, bg="red", fg="white", font=('Arial', 14, 'bold'))
boton_afip.grid(row=row_offset, column=3, rowspan=5, padx=(0, 10), pady=(0, 10), sticky="W")

boton_maximizar_minimizar = Button(root, text="Max/Min", command=maximizar_minimizar_ventana, bg="black", fg="white", font=('Arial', 10, 'bold'))
boton_maximizar_minimizar.grid(row=row_offset + 6, column=4, padx=(0, 10), pady=10)


# Actualizar el Treeview con datos existentes
actualizar_treeview(tree)

root.mainloop()
