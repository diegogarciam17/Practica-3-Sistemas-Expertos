import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk

# Cargar la base de datos de youtubers
def cargar_youtubers():
    try:
        with open('youtubers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Guardar la base de datos de youtubers
def guardar_youtubers(youtubers):
    with open('youtubers.json', 'w') as f:
        json.dump(youtubers, f, indent=4)

# Clase para la interfaz del juego
class Nodo:
    def __init__(self, pregunta=None, si=None, no=None, youtuber=None):
        self.pregunta = pregunta
        self.si = si
        self.no = no
        self.youtuber = youtuber

class AdivinaQuienApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivina Quién - Youtubers")

        # Cargar la imagen de fondo
        try:
            self.background_image = Image.open("background.jpg")
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.root.geometry(f"{self.background_image.width}x{self.background_image.height}")
            self.background_label = tk.Label(root, image=self.background_photo)
            self.background_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Error: No se encontró el archivo 'background.jpg'. Asegúrate de que el archivo esté en el mismo directorio.")

        self.iniciar_juego()

    def iniciar_juego(self):
        self.youtubers = cargar_youtubers()
        self.posibles_youtubers = self.youtubers.copy()
        self.preguntas = [
            {"atributo": "hombre", "pregunta": "¿Es hombre?"},
            {"atributo": "gamer", "pregunta": "¿Es un gamer?"},
            {"atributo": "vlogs", "pregunta": "¿Hace vlogs?"},
            {"atributo": "comedia", "pregunta": "¿Hace contenido de comedia?"},
            {"atributo": "coches", "pregunta": "¿Hace contenido de coches?"},
            {"atributo": "cantante", "pregunta": "¿Es cantante?"},
            {"atributo": "suscriptores_mas_10_millones", "pregunta": "¿Tiene más de 10 millones de suscriptores?"}
        ]
        self.pregunta_indice = 0

        # Mensaje de bienvenida
        messagebox.showinfo("Bienvenida", "¡Bienvenido a Adivina Quién - Youtubers! Responde las preguntas para adivinar al youtuber.")

        self.label_pregunta = tk.Label(self.root, text=self.preguntas[self.pregunta_indice]["pregunta"], font=("Arial", 14), bg="white")
        self.label_pregunta.pack(pady=20)

        self.btn_si = tk.Button(self.root, text="Sí", command=lambda: self.responder(True), width=10)
        self.btn_si.pack(side=tk.LEFT, padx=20, pady=10)

        self.btn_no = tk.Button(self.root, text="No", command=lambda: self.responder(False), width=10)
        self.btn_no.pack(side=tk.RIGHT, padx=20, pady=10)

    def responder(self, respuesta):
        atributo = self.preguntas[self.pregunta_indice]["atributo"]

        # Filtrar los posibles youtubers según la respuesta
        self.posibles_youtubers = [y for y in self.posibles_youtubers if y.get(atributo) == respuesta]

        # Avanzar a la siguiente pregunta
        self.pregunta_indice += 1

        if len(self.posibles_youtubers) == 1:
            respuesta = messagebox.askyesno("Resultado", f"¡He adivinado! Es {self.posibles_youtubers[0]['nombre']}. ¿Es correcto?")
            if respuesta:
                self.reiniciar_juego()
            else:
                self.agregar_nuevo_youtuber()
        elif len(self.posibles_youtubers) == 0 or self.pregunta_indice >= len(self.preguntas):
            self.no_pude_adivinar()
        else:
            self.label_pregunta.config(text=self.preguntas[self.pregunta_indice]["pregunta"])

    def no_pude_adivinar(self):
        respuesta = messagebox.askyesno("No pude adivinar", "No pude adivinar el youtuber. ¿Quieres ayudarme a aprender?")
        if respuesta:
            self.agregar_nuevo_youtuber()
        else:
            self.reiniciar_juego()

    def agregar_nuevo_youtuber(self):
        nuevo_nombre = simpledialog.askstring("Nuevo Youtuber", "¿Cuál es el nombre del youtuber?")
        if nuevo_nombre:
            nuevo_youtuber = {"nombre": nuevo_nombre}
            for pregunta in self.preguntas:
                respuesta = messagebox.askyesno("Características", pregunta["pregunta"])
                nuevo_youtuber[pregunta["atributo"]] = respuesta

            self.youtubers.append(nuevo_youtuber)
            guardar_youtubers(self.youtubers)
            messagebox.showinfo("Gracias", "¡Gracias! He aprendido un nuevo youtuber.")
        self.reiniciar_juego()

    def reiniciar_juego(self):
        respuesta = messagebox.askyesno("Nuevo Juego", "¿Quieres jugar de nuevo?")
        if respuesta:
            # Reiniciar el juego
            self.label_pregunta.pack_forget()
            self.btn_si.pack_forget()
            self.btn_no.pack_forget()
            self.iniciar_juego()
        else:
            self.root.quit()

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AdivinaQuienApp(root)
    root.mainloop()
