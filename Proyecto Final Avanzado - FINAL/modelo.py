#________________________

     #MODULOS IMPORTADOS             ----------   MODELO -----------
#_________________________

from tkinter import *
from tkinter.messagebox import *
from tkinter import messagebox
from peewee import *
import webbrowser
from decoradores import ManejoErrores

#________________________

     #MODELO PROPIO REGISTRO DE CLLIENTES
     #SOLO DE INGRESO A AFIP
#________________________________________
     #BASE DE DATOS
#_________________________

midb = SqliteDatabase("base_clientes.db")

class BaseModel(Model):
    class Meta:
        database = midb


class Clientes(BaseModel):
    nombre = CharField()
    apellido = CharField()
    rubro = CharField()
    cuit = IntegerField()
    clave_fiscal = CharField()

midb.connect()
midb.create_tables([Clientes])


#________________________________________
     #FUNCIONES PARA LA BOTONERA
#_________________________

class FuncionesBotonera(Exception):
    
    @ManejoErrores.manejar_movimiento
    def alta(self, nombre, apellido, rubro, cuit, clave_fiscal, tree):
        if not self.validar_campos(nombre, apellido, rubro, cuit, clave_fiscal):
            return
        if self.validar_cliente_existente(nombre.get(), apellido.get()):
            return

        try:
            noticia = Clientes.create(
                nombre=nombre.get(),
                apellido=apellido.get(),
                rubro=rubro.get(),
                cuit=cuit.get(),
                clave_fiscal=clave_fiscal.get()
            )

            ManejoErrores.registrar_movimiento(f"Haz agregado un nuevo cliente llamado/a {noticia.nombre} {noticia.apellido} con CUIT: {noticia.cuit}.")
            showinfo("Cliente agregado", "El cliente se ha agregado correctamente.")  # Ventana emergente de éxito
            self.actualizar_treeview(tree)
        except Exception as e:
            ManejoErrores.registrar_error(str(e))


    def toggle_password(self, show_password_var, entry, show_char):
        if show_password_var.get():
            entry.config(show="")
        else:
            entry.config(show=show_char)
            
    def abrir_afip(self):
        webbrowser.open("https://www.afip.gob.ar/landing/default.asp")


    def actualizar_treeview(self, mi_tree_view):
        records = mi_tree_view.get_children()
        for element in records:
            mi_tree_view.delete(element)

        for fila in Clientes.select():
            mi_tree_view.insert("", 0, text=fila.id, values=(fila.nombre, fila.apellido, fila.rubro, fila.cuit, fila.clave_fiscal))
    
    @ManejoErrores.manejar_movimiento
    def borrar(self, tree):
        valor = tree.selection()
        if not valor:
            ManejoErrores.registrar_error("Por favor, seleccione un cliente para eliminar.")
            return

        respuesta = askquestion("Confirmar", "¿Estás seguro que deseas eliminar este cliente?")
        if respuesta == 'yes':
            item = tree.item(valor)
            nombre = item['values'][0]
            apellido = item['values'][1]
            cuit = item['values'][3]
            borrado = Clientes.get(Clientes.nombre == nombre, Clientes.apellido == apellido, Clientes.cuit == cuit)
            borrado.delete_instance()
            tree.delete(valor)
            ManejoErrores.registrar_movimiento(f"Cliente {nombre} {apellido} con CUIT {cuit} eliminado correctamente.")

    @ManejoErrores.manejar_movimiento
    def modificar(self, tree, nombre, apellido, rubro, cuit, clave_fiscal):
        if not self.validar_campos(nombre, apellido, rubro, cuit, clave_fiscal):
            return
        if not cuit.get().isdigit() or len(cuit.get()) != 11:
            ManejoErrores.registrar_error("El CUIT debe contener exactamente 11 dígitos.")
            return

        valor = tree.selection()
        if not valor:
            ManejoErrores.registrar_error("Por favor, seleccione un cliente para modificar.")
            return

        item = tree.item(valor)
        nombre_actual = item['values'][0]
        apellido_actual = item['values'][1]
        cuit_actual = item['values'][3]

        respuesta = askquestion("Confirmar", f"¿Estás seguro que deseas modificar al cliente {nombre_actual} {apellido_actual} con CUIT {cuit_actual}.?")
        if respuesta == 'yes':
            # Guardar los datos anteriores
            nombre_antiguo = nombre_actual
            apellido_antiguo = apellido_actual
            cuit_antiguo = cuit_actual

            # Actualizar el cliente
            actualizar = Clientes.update(
                nombre=nombre.get(),
                apellido=apellido.get(),
                rubro=rubro.get(),
                cuit=cuit.get(),
                clave_fiscal=clave_fiscal.get()
            ).where(Clientes.nombre == nombre_actual, Clientes.apellido == apellido_actual, Clientes.cuit == cuit_actual)
            actualizar.execute()

            # Obtener los nuevos datos
            nombre_nuevo = nombre.get()
            apellido_nuevo = apellido.get()
            cuit_nuevo = cuit.get()

            # Registrar el movimiento
            ManejoErrores.registrar_movimiento(f"Cliente {nombre_antiguo} {apellido_antiguo} con CUIT {cuit_antiguo} modificado a {nombre_nuevo} {apellido_nuevo} con CUIT {cuit_nuevo}")
            self.actualizar_treeview(tree)

    @ManejoErrores.manejar_movimiento
    def consultar(self, tree, nombre, apellido, rubro, cuit, clave_fiscal):
        valor = tree.selection()
        if not valor:
            ManejoErrores.registrar_error("Por favor, seleccione un cliente para consultar.")
            return

        item = tree.item(valor)
        nombre_actual = item['values'][0]
        apellido_actual = item['values'][1]
        cuit_actual = item['values'][3]
        consulta = Clientes.get(Clientes.nombre == nombre_actual, Clientes.apellido == apellido_actual, Clientes.cuit == cuit_actual)

        nombre.set(consulta.nombre)
        apellido.set(consulta.apellido)
        rubro.set(consulta.rubro)
        cuit.set(consulta.cuit)
        clave_fiscal.set(consulta.clave_fiscal)
        ManejoErrores.registrar_movimiento(f"Consulta de cliente {nombre_actual} {apellido_actual} con CUIT {cuit_actual}.")


    def mostrar_mensaje(self, titulo, mensaje):
        showinfo(titulo, mensaje)

    def maximizar_minimizar_ventana(self, tree):
        if tree.winfo_ismapped():
            tree.grid_remove()  # Ocultar la Treeview si está visible
        else:
            tree.grid()  # Mostrar la Treeview si está oculta

    def validar_cliente_existente(self, nombre, apellido):
            try:
                cliente_existente = Clientes.get((Clientes.nombre == nombre) & (Clientes.apellido == apellido))
                messagebox.showerror("Error", f"Ya existe un cliente con el nombre {nombre} y apellido {apellido}.")
                ManejoErrores.registrar_error(f"Intento de agregar un cliente ya registrado: {nombre} {apellido}")
                return True
            except Clientes.DoesNotExist:
                return False       
    
    def validar_campos(self, nombre, apellido, rubro, cuit, clave_fiscal):
        campos_faltantes = []
        if not nombre.get():
            campos_faltantes.append("Nombre")
        if not apellido.get():
            campos_faltantes.append("Apellido")
        if not rubro.get():
            campos_faltantes.append("Rubro")
        if not cuit.get():
            campos_faltantes.append("CUIT")
        if not clave_fiscal.get():
            campos_faltantes.append("Clave Fiscal")

        if campos_faltantes:
            messagebox.showerror("Error", f"Los siguientes campos son obligatorios: {', '.join(campos_faltantes)}")
            ManejoErrores.registrar_error(f"Faltan los siguientes campos obligatorios: {', '.join(campos_faltantes)}")
            return False
        elif not cuit.get().isdigit() or len(cuit.get()) != 11:
            messagebox.showerror("Error", "El CUIT debe contener exactamente 11 digitos.")
            ManejoErrores.registrar_error("El CUIT debe contener exactamente 11 digitos.")
            return False
        return True
