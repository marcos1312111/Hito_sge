import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import mysql.connector
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para conectar a la base de datos usando mysql-connector-python
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="campusfp",
            database="ENCUESTAS"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Error de Conexión", str(e))
        return None

# Clase principal de la aplicación
class EncuestaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.create_widgets()

    def create_widgets(self):
        # Frame para tabla de datos
        self.tree = ttk.Treeview(self, columns=("id", "edad", "sexo", "bebidas", "cervezas", "bebidas_fin_semana", "destiladas_semana", "vinos", "perdidas_control", "diversion_dependencia", "digestivos", "tensionAlta", "dolorCabeza"),
                                 show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("edad", text="Edad")
        self.tree.heading("sexo", text="Sexo")
        self.tree.heading("bebidas", text="Bebidas/Semana")
        self.tree.heading("cervezas", text="Cervezas/Semana")
        self.tree.heading("bebidas_fin_semana", text="Bebidas Fin/Semana")
        self.tree.heading("destiladas_semana", text="Destiladas/Semana")
        self.tree.heading("vinos", text="Vinos/Semana")
        self.tree.heading("perdidas_control", text="Pérdidas de Control")
        self.tree.heading("diversion_dependencia", text="Diversión/Dependencia")
        self.tree.heading("digestivos", text="Problemas Digestivos")
        self.tree.heading("tensionAlta", text="Tensión Alta")
        self.tree.heading("dolorCabeza", text="Dolor de Cabeza")

        # Ajustar el ancho de las columnas para que todas sean visibles
        self.tree.column("id", width=50)
        self.tree.column("edad", width=50)
        self.tree.column("sexo", width=70)
        self.tree.column("bebidas", width=100)
        self.tree.column("cervezas", width=100)
        self.tree.column("bebidas_fin_semana", width=140)
        self.tree.column("destiladas_semana", width=140)
        self.tree.column("vinos", width=100)
        self.tree.column("perdidas_control", width=140)
        self.tree.column("diversion_dependencia", width=170)
        self.tree.column("digestivos", width=140)
        self.tree.column("tensionAlta", width=140)
        self.tree.column("dolorCabeza", width=140)

        # Estilo para hacer las filas más pequeñas
        style = ttk.Style()
        style.configure("Treeview", rowheight=20)

        self.tree.pack(fill="both", expand=True)

        # Crear botones de operaciones
        self.create_operation_buttons()

        # Botón para cargar encuestas al iniciar
        self.view_encuestas()

    def create_operation_buttons(self):
        # Frame para los botones
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Crear botones para operaciones
        tk.Button(button_frame, text="Agregar Encuesta", command=self.add_encuesta).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Actualizar Encuesta", command=self.update_encuesta).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Eliminar Encuesta", command=self.delete_encuesta).grid(row=0, column=2, padx=10, pady=5)

        # Crear botones para filtros
        tk.Button(button_frame, text="Filtrar por Edad", command=self.filter_by_age).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Filtrar por ID", command=self.filter_by_id).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Filtrar por Sexo", command=self.filter_by_gender).grid(row=1, column=2, padx=10, pady=5)

        # Botón para mostrar todos los datos
        tk.Button(button_frame, text="Mostrar Todo", command=self.show_all).grid(row=2, column=0, padx=10, pady=5)

        # Crear botones para extras
        tk.Button(button_frame, text="Exportar a Excel", command=self.export_to_excel).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Mostrar Gráficos", command=self.show_graph).grid(row=2, column=2, padx=10, pady=5)

    def view_encuestas(self, query="SELECT idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza FROM ENCUESTA"):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                self.tree.insert("", tk.END, values=row)
            conn.close()

    def add_encuesta(self):
        self.input_window("Agregar Encuesta", self.insert_data)

    def insert_data(self, edad, sexo, bebidas, cervezas, bebidas_fin_semana, destiladas_semana, vinos, perdidas_control, diversion_dependencia, digestivos, tensionAlta, dolorCabeza):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                query = """INSERT INTO ENCUESTA (edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (edad, sexo, bebidas, cervezas, bebidas_fin_semana, destiladas_semana, vinos, perdidas_control, diversion_dependencia, digestivos, tensionAlta, dolorCabeza))
                conn.commit()
                messagebox.showinfo("Éxito", "Encuesta agregada correctamente.")
                self.view_encuestas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_encuesta(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            encuesta_id = item["values"][0]
            self.input_window("Actualizar Encuesta", lambda *args: self.update_data(encuesta_id, *args), item["values"])

    def update_data(self, encuesta_id, edad, sexo, bebidas, cervezas, bebidas_fin_semana, destiladas_semana, vinos, perdidas_control, diversion_dependencia, digestivos, tensionAlta, dolorCabeza):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                query = """UPDATE ENCUESTA SET edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s, BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, DiversionDependenciaAlcohol=%s, ProblemasDigestivos=%s, TensionAlta=%s, DolorCabeza=%s WHERE idEncuesta=%s"""
                cursor.execute(query, (edad, sexo, bebidas, cervezas, bebidas_fin_semana, destiladas_semana, vinos, perdidas_control, diversion_dependencia, digestivos, tensionAlta, dolorCabeza, encuesta_id))
                conn.commit()
                messagebox.showinfo("Éxito", "Encuesta actualizada correctamente.")
                self.view_encuestas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_encuesta(self):
        selected_item = self.tree.selection()
        if selected_item:
            try:
                item = self.tree.item(selected_item)
                encuesta_id = item["values"][0]
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM ENCUESTA WHERE idEncuesta=%s", (encuesta_id,))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Encuesta eliminada correctamente.")
                    self.view_encuestas()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def input_window(self, title, callback, default_values=None):
        input_win = tk.Toplevel(self)
        input_win.title(title)
        labels = ["Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana", "Bebidas Fin/Semana", "Destiladas/Semana", "Vinos/Semana", "Pérdidas de Control", "Diversión/Dependencia", "Problemas Digestivos", "Tensión Alta", "Dolor de Cabeza"]
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(input_win, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(input_win)
            entry.grid(row=i, column=1, padx=5, pady=5)
            if default_values:
                entry.insert(0, default_values[i + 1])  # Usar los valores por defecto si existen
            entries[label] = entry
        tk.Button(input_win, text="Guardar", command=lambda: self.submit_data(entries, callback, input_win)).grid(row=len(labels), columnspan=2)

    def submit_data(self, entries, callback, input_win):
        values = [entries[label].get() for label in entries]
        input_win.destroy()
        callback(*values)  # Llamar al callback con los valores ingresados

    def filter_by_age(self):
        age = simpledialog.askstring("Filtrar por Edad", "Introduce la edad a filtrar:")
        if age:
            query = f"SELECT * FROM ENCUESTA WHERE edad={age}"
            self.view_encuestas(query)

    def filter_by_id(self):
        encuesta_id = simpledialog.askinteger("Filtrar por ID", "Introduce el ID de la encuesta:")
        if encuesta_id:
            query = f"SELECT * FROM ENCUESTA WHERE idEncuesta={encuesta_id}"
            self.view_encuestas(query)

    def filter_by_gender(self):
        gender = simpledialog.askstring("Filtrar por Sexo", "Introduce el sexo (Hombre/Mujer):")
        if gender:
            query = f"SELECT * FROM ENCUESTA WHERE Sexo='{gender}'"
            self.view_encuestas(query)

    def show_all(self):
        self.view_encuestas()

    def export_to_excel(self):
        try:
            conn = connect_db()
            if conn:
                query = "SELECT * FROM ENCUESTA"
                df = pd.read_sql(query, conn)
                df.to_excel("encuestas.xlsx", index=False)
                messagebox.showinfo("Exportación", "Datos exportados correctamente a 'encuestas.xlsx'.")
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_graph(self):
        try:
            conn = connect_db()
            if conn:
                query = "SELECT edad, COUNT(*) FROM ENCUESTA GROUP BY edad"
                df = pd.read_sql(query, conn)
                conn.close()
                
                df.plot(kind="bar", x="edad", y="COUNT(*)")
                plt.title("Encuestas por Edad")
                plt.ylabel("Número de Encuestas")
                plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Iniciar la aplicación
if __name__ == "__main__":
    app = EncuestaApp()
    app.mainloop()
