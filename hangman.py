from tkinter import *
from tkinter import messagebox
from random import choice,shuffle
from string import ascii_uppercase

#Funcion para cambiar la imagen de un label
def changeimage(label,path):
    image=PhotoImage(file=path)
    label.configure(image=image)
    label.image=image

#Ventana principal
class Container(Tk):
    def __init__(self,**kwargs):
        super(Container,self).__init__(**kwargs)
        self.geometry("600x600+%i+%i"%((self.winfo_screenwidth()-600)/2,(self.winfo_screenheight()-600)/2)) #Tamaño y posición incial
        self.title("Ahorcado") #Título de la ventana
        Menu().pack(expand=True,fill=BOTH) #Menu incial

    #Destruye un fame y crea otro
    def change(self,destroy,create):
        destroy.destroy()
        create().pack(expand=True,fill=BOTH)

class Menu(Frame):
    def __init__(self,**kwargs):
        super(Menu,self).__init__(**kwargs)
        Label(self,text="AHORCADO",font=("IMPACT",80)).pack(pady=20)
        Button(self,text="JUGAR",font=("IMPACT",20),width=20,command=lambda:self.master.change(self,Game)).pack(pady=40)
        Button(self,text="SALIR",font=("IMPACT",20),width=20,command=quit).pack(pady=40)

class Game(Frame):
    def __init__(self,**kwargs):
        super(Game,self).__init__(**kwargs)
        self.deadimg=["img/1_rope.png","img/2_head.png","img/3_bodysup.png","img/4_bodyinf.png","img/5_extremities.png","img/6_feets.png","img/7_dead.png"]

        #Cantidad de columnas y filas con letras
        columns=10
        rows=2

        #Se obtiene la lista de palabras
        with open("words.txt",'r') as text:
            words=[word.strip() for word in text]
            text.close()

        self.state=0 #Estado del hombre
        self.dead=Label(self) #Contenedor para la imagen del hombre
        self.dead.pack()
        changeimage(self.dead,self.deadimg[self.state]) #Se coloca la primer imagen

        self.word=list(choice(words).upper()) #Se elige una palabra, y se la convierte a mayúsculas y una lista
        #Se utiliza la función copy para no manejar el mismo espacio de memoria
        self.compare=self.word.copy() #Lo uso para comparar con lo adivinado y decidir la victoria, ver funcion check
        filler=self.word.copy() #Variable para rellenar los botones
        while len(filler)<(columns*rows): #Mientras la cantidad de letras para rellenar sea menor a la cantidad de letras a rellenar se añade una letra aleatoria
            filler+=choice(ascii_uppercase) #Selecciona una letra aleatoria de los carácteres ascii básicos en mayusculas
        shuffle(filler) #Se mezcla la palabra con las demás letras

        self.lettersbox=Frame(self) #Contenedor para los botones para poder alinear por columnas y filas dentro de el
        for column in range(columns):
            for row in range(rows):
                button=Button(self.lettersbox,text=filler.pop(),width=3,font=("IMPACT",15))
                button.configure(command=lambda this=button:self.check(this)) #this guarda una referencia al boton
                button.grid(column=column,row=row,padx=5,pady=5)
        self.lettersbox.pack(side=BOTTOM,pady=40)

        self.prediction_var=StringVar() #Variable de tkinter para que el label con los guiones y las letras se actualice solo cuando tenga un cambio
        self.prediction=["_" for letter in self.word] #Genera una lista con guiones igual al tamaño de la palabra y se usa para llevar las letras acertadas
        self.prediction_var.set(self.prediction)
        Label(self,textvar=self.prediction_var,font=("IMPACT",30)).pack(side=BOTTOM)

    #Funcion para verificar
    def check(self,button):
        try: #Si la letra del boton se encuentra en la palabra obtenemos el lugar de la primer incidencia
            place=self.word.index(button["text"])
        except: #Sino eleva un error
            place=-1

        #Si la letra se encuentra en la palabra
        if place != -1:
            button.configure(bg="green",state=DISABLED,disabledforeground="black") #Deshabilitamos el boton y lo ponemos de verde
            self.word[place]="" #La letra en la palabra se vuelve un espacio en blanco para que no genere proximas incidencias al comparar
            self.prediction[place]=button["text"] #Se modifica el guion por la letra del boton en donde ocurrio la incidencia
            self.prediction_var.set(self.prediction) #Se actualiza la variable del label que muestra los guiones y letras
            if self.compare==self.prediction: #Si la variable donde llevamos las letras acertadas es igual a la variable donde respaldamos nuestra palabra incial entonces
                for child in self.lettersbox.winfo_children(): #Deshabilitamos todos los botones
                    child.configure(state=DISABLED,disabledforeground="black")
                self.EndGame(1)
        #Si la letra no se encuentra en la palabra
        else:
            button.configure(bg="red",state=DISABLED,disabledforeground="black") ##Deshabilitamos el boton y lo ponemos de rojo
            self.state+=1 #Aumentamos en 1 el estado del hombre
            changeimage(self.dead,self.deadimg[self.state]) #Actualizamos la imagen del hombre
            if self.state==6: #Si está en su ultimo estado
                self.prediction_var.set(self.compare) #Mostramos la palabra
                for child in self.lettersbox.winfo_children(): #Deshabilitamos todos los botones
                    child.configure(state=DISABLED,disabledforeground="black")
                self.EndGame(0)

    #Genera una ventana para volver a jugar o volver al menu
    def EndGame(self,state):
        if state==1: #Si gana
            message=messagebox.askretrycancel("REINTENAR","¡HAZ GANADO!\n¿QUIERES VOLVER A JUGAR?")
        else: #Si pierde
            message=messagebox.askretrycancel("REINTENAR","¡HAZ PERDIDO!\n¿QUIERES VOLVER A JUGAR?")
        if message: #Devuelve true si se aprieta en reintentar
            self.master.change(self,Game) #Destruye el juego anterior y crea otro
        else:
            self.master.change(self,Menu) #Destruye el juego y crea el menu

game=Container()
mainloop()
