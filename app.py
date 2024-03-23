import tkinter as tk
import psycopg2
import random
from PIL import Image, ImageTk
from tkinter import ttk
from psycopg2 import OperationalError

class AdivinadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivinador de Jugadores Campeones del Mundo")
        self.condiciones = []  # Lista para almacenar las condiciones de filtrado
        self.cargar_jugadores()  # Inicializa la carga de jugadores
        self.pregunta_actual = ""
        self.atributos = ["PAIS", "POSICION", "AÑO", "YEAR", "MES", "DIA"]
        self.atributo = ""
        self.valor = ""
        self.conozcoPais = False
        self.conozcoPosicion = False
        self.conozcoAño = False
        self.conozcoAñoNacimiento = False
        self.conozcoMesNacimiento = False
        self.conozcoDiaNacimiento = False
        self.progreso_acierto = 0
        self.jugadores_descartados = 0
        self.total_jugadores = 493

        # Configuración de la interfaz gráfica
        root.geometry("800x400")
        
        self.label_pregunta = tk.Label(root, text="", wraplength=300, font=("Arial", 18))
        self.label_pregunta.pack(pady=20)
        
        self.imagen1 = Image.open("imagen1.png").resize((200,200))
        self.imagen_tk1 = ImageTk.PhotoImage(self.imagen1)

        self.label_imagen = tk.Label(root, image=self.imagen_tk1)
        self.label_imagen.pack(pady=20)

        self.marco_si = tk.Frame(root, width=100, height=50)
        self.marco_si.pack_propagate(0)  # Evita que el marco se ajuste al tamaño del botón
        self.marco_si.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.boton_si = tk.Button(self.marco_si, text="Sí", command=lambda: self.responder("sí"), font=("Arial", 17))
        self.boton_si.pack(expand=True)

        self.marco_no = tk.Frame(root, width=100, height=50)
        self.marco_no.pack_propagate(0)  # Evita que el marco se ajuste al tamaño del botón
        self.marco_no.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.boton_no = tk.Button(self.marco_no, text="No", command=lambda: self.responder("no"), font=("Arial", 17))
        self.boton_no.pack(expand=True)
        
        self.barra_progreso = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.barra_progreso.pack(pady=20)
        self.barra_progreso['value'] = self.progreso_acierto

        self.generar_pregunta()

    def conectar_db(self):
        try:
            self.conexion = psycopg2.connect(
                dbname='campeones',
                user='postgres',
                password='abc',
                host='localhost'
            )
            print("Conexión exitosa a la base de datos")
        except OperationalError as e:
            print(f"Ocurrió un error al conectar con la base de datos: {e}")
            self.conexion = None
        

    def cargar_jugadores(self):
        # Establecer la conexión con la base de datos
        self.conectar_db()
        conexion = self.conexion
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                # Construir la consulta SQL basada en las condiciones actuales
                sql_query = "SELECT * FROM public.jugadores"
                if self.condiciones:
                    sql_query += " WHERE " + " AND ".join(self.condiciones)
                cursor.execute(sql_query)
                self.jugadores = cursor.fetchall()  # Actualizar la lista de jugadores
                cursor.close()
                self.actualizar_progreso()
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Error al cargar jugadores: {error}")
            finally:
                conexion.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            self.jugadores = []

    def actualizar_progreso(self):
        
        self.jugadores_descartados = self.total_jugadores - len(self.jugadores)
        self.progreso_acierto = int(self.jugadores_descartados/493 * 100)
        self.barra_progreso['value'] = self.progreso_acierto
        

    def generar_pregunta(self):
        
        self.actualizar_imagen()
        
        if not self.jugadores:
            self.label_pregunta.configure(text="No se encontraron jugadores con esas características.")
            return

        self.atributo = random.choice(self.atributos)  # Elegir un atributo al azar
        if self.atributo == "PAIS":
            if self.conozcoPais:
                #remover PAIS de los atributos
                self.atributos.remove("PAIS")
                self.atributo = random.choice(self.atributos)
        elif self.atributo == "POSICION":
            if self.conozcoPosicion:
                #remover POSICION de los atributos
                self.atributos.remove("POSICION")
                self.atributo = random.choice(self.atributos)
        elif self.atributo == "AÑO":
            if self.conozcoAño:
                #remover AÑO de los atributos
                self.atributos.remove("AÑO")
                self.atributo = random.choice(self.atributos)  
        elif self.atributo == "YEAR":
            if self.conozcoAñoNacimiento:
                #remover YEAR de los atributos
                self.atributos.remove("YEAR")
                self.atributo = random.choice(self.atributos)
        elif self.atributo == "MES":
            if self.conozcoMesNacimiento:
                #remover MES de los atributos
                self.atributos.remove("MES")
                self.atributo = random.choice(self.atributos)
        elif self.atributo == "DIA":
            if self.conozcoDiaNacimiento:
                #remover DIA de los atributos
                self.atributos.remove("DIA")
                self.atributo = random.choice(self.atributos)
        
        self.valor = self.obtener_atributo_para_pregunta()
        if self.atributo == "PAIS":
            self.pregunta_actual = f"¿Tu jugador es de {self.valor}?"
        elif self.atributo == "POSICION":
            posiciones = {"por": "portero", "def": "defensa", "med": "centrocampista", "del": "delantero"}
            self.pregunta_actual = f"¿Tu jugador juega en la posición de {posiciones[self.valor]}?"
        elif self.atributo == "AÑO":
            self.pregunta_actual = f"¿Tu jugador fue campeón en el año {self.valor}?"
        elif self.atributo == "YEAR":
            self.pregunta_actual = f"¿Tu jugador nació en el año {self.valor}?"
        elif self.atributo == "MES":
            meses = {1: "enero",2: "febrero",3: "marzo",4: "abril",
            5: "mayo",6: "junio",7: "julio",8: "agosto",9:"septiembre",
            10: "octubre",11: "noviembre",12: "diciembre"
            }
            self.pregunta_actual = f"¿Tu jugador nació en el mes {meses[self.valor]}?"
        elif self.atributo == "DIA":
            self.pregunta_actual = f"¿Tu jugador nació en el día {self.valor}?"
        else:
            
            pass

        self.label_pregunta.configure(text=self.pregunta_actual)

    def actualizar_imagen(self):
        # Lista de imágenes precargadas
        imagenes = [
            "imagen1.png",
            "imagen2.png",
            "imagen3.png",
            "imagen4.png",
            "imagen5.png",
            "imagen6.png"
        ]

        # Elegir una imagen al azar
        imagen_aleatoria = random.choice(imagenes)

        # Cargar la imagen y ajustar su tamaño
        imagen = Image.open(imagen_aleatoria).resize((200, 200))

        # Convertir la imagen a un objeto ImageTk
        imagen_tk = ImageTk.PhotoImage(imagen)

        # Actualizar la imagen mostrada en la interfaz gráfica
        self.label_imagen.configure(image=imagen_tk)
        self.label_imagen.image = imagen_tk  # Actualizar la referencia a la imagen para evitar que sea eliminada por el recolector de basura

    def obtener_atributo_para_pregunta(self):
        atributos_a_indices = {"NOMBRE": 0, "POSICION": 1,"PAIS": 2, "AÑO": 3, "YEAR": 4, "MES": 5, "DIA": 6}
        
        indicejugador = random.randint(0, len(self.jugadores) - 1)
        
        indice = atributos_a_indices[self.atributo]
        if indice > 3:
            valor = self.jugadores[indicejugador][4].year if indice == 4 else self.jugadores[indicejugador][4].month if indice == 5 else self.jugadores[indicejugador][4].day
        else:
            valor = self.jugadores[indicejugador][indice]
        if valor:
            return  valor
        else:
            # Si no hay jugadores o no se pudo determinar, devolver un valor por defecto
            return "Valor por defecto"  # Ejemplo default, debes ajustarlo

    def responder(self, respuesta):
        # Generar la condición SQL adecuada basada en la pregunta actual y la respuesta
        condicion = self.generar_condicion_sql(respuesta)
        if condicion:  # Asegurarse de que la condición no esté vacía
            self.condiciones.append(condicion)
        
        self.cargar_jugadores()  # Recargar jugadores con las nuevas condiciones
        
        # Verificar si queda un único jugador después de aplicar el filtro
        if len(self.jugadores) == 1:
            # Mostrar el jugador restante como la respuesta
            self.label_pregunta.configure(text=f"El jugador en el que estás pensando es: {self.jugadores[0][0]}")
        elif len(self.jugadores) > 1:
            # Si hay más de un jugador, generar una nueva pregunta
            self.generar_pregunta()
        else:
            # Si no quedan jugadores, es posible que haya un error lógico en las condiciones
            self.label_pregunta.configure(text="No se encontró ningún jugador con esas características. Intentemos de nuevo.")



    def generar_condicion_sql(self, respuesta):
        if self.atributo and self.valor:
            if self.atributo == "PAIS":
                if respuesta == "sí":
                    self.conozcoPais = True
                    return f"\"PAIS\" LIKE '{self.valor}'"
                else:
                    return f"\"PAIS\" NOT LIKE '{self.valor}'"
            if self.atributo == "POSICION":
                if respuesta == "sí":
                    self.conozcoPosicion = True
                    return f"\"POSICION\" LIKE '{self.valor}'"
                else:
                    return f"\"POSICION\" NOT LIKE '{self.valor}'"
            if self.atributo == "AÑO":
                if respuesta == "sí":
                    self.conozcoAño = True
                    return f"\"AÑO\" = {self.valor}"
                else:
                    return f"\"AÑO\" != {self.valor}"
            if self.atributo == "YEAR":
                if respuesta == "sí":
                    self.conozcoAñoNacimiento = True
                    return f"EXTRACT(YEAR FROM \"NACIMIENTO\") = {self.valor}"
                else:
                    return f"EXTRACT(YEAR FROM \"NACIMIENTO\") != {self.valor}"
            if self.atributo == "MES":
                if respuesta == "sí":
                    self.conozcoMesNacimiento = True
                    return f"EXTRACT(MONTH FROM \"NACIMIENTO\") = {self.valor}"
                else:
                    return f"EXTRACT(MONTH FROM \"NACIMIENTO\") != {self.valor}"
            if self.atributo == "DIA":
                if respuesta == "sí":
                    self.conozcoDiaNacimiento = True
                    return f"EXTRACT(DAY FROM \"NACIMIENTO\") = {self.valor}"
                else:
                    return f"EXTRACT(DAY FROM \"NACIMIENTO\") != {self.valor}"
        return ""

if __name__ == "__main__":
    root = tk.Tk()
    app = AdivinadorApp(root)
    root.mainloop()
    
    

