from tkinter import *
from random import choice,shuffle
from string import ascii_uppercase
from PIL import Image,ImageTk

def change(create):
    for object in Container.app.winfo_children():
        object.destroy()
    create(Container.app)

def labelimage(path,frame,side=TOP):
    imgPath = path
    img = ImageTk.PhotoImage(Image.open(imgPath))
    label = Label(frame)
    label.image = img
    label.configure(image=img)
    label.pack(side=side)
    return label

class Container():
    app=Tk()
    app.geometry("600x600")
    app.resizable(False,False)
    app.title("Ahorcado")

    def __init__(self):
        Menu(Container.app)

class Menu():
    def __init__(self,app):
        self.frame=Frame(app)
        self.frame.pack(fill=BOTH,expand=1)

        Label(self.frame,text="AHORCADO",font=("IMPACT",80)).pack(pady=20)
        Button(self.frame,text="JUGAR",font=("IMPACT",20),width=20,command=lambda:change(Game)).pack(pady=40)
        Button(self.frame,text="SALIR",font=("IMPACT",20),width=20,command=quit).pack(pady=40)

class Game():
    columns=10
    rows=2
    deadimg=["img/1_rope.png","img/2_head.png","img/3_bodysup.png","img/4_bodyinf.png","img/5_extremities.png","img/6_feets.png","img/7_dead.png"]

    with open("words.txt",'r') as list:
        words=[word.strip() for word in list]
        list.close()

    def __init__(self,app):
        self.frame=Frame(app)
        self.frame.pack(fill=BOTH,expand=1)

        self.state=0
        self.dead=labelimage(Game.deadimg[self.state],self.frame)

        self.word=choice(Game.words).upper()
        GameButton.word=list(self.word)
        filler=self.word
        while len(filler)<(Game.columns*Game.rows):
            filler+=choice(ascii_uppercase)
        filler=list(filler)
        shuffle(filler)

        index=0
        self.lettersbox=Frame(self.frame)
        for column in range(Game.columns):
            for row in range(Game.rows):
                new=GameButton(self.lettersbox,filler[index],self)
                new.button.grid(column=column,row=row,padx=5,pady=5)
                index+=1

        self.lettersbox.pack(side=BOTTOM,pady=40)

        GameButton.prediction=["_" for letter in self.word]
        GameButton.var.set(GameButton.prediction)

        predictionlabel=Label(self.frame,textvar=GameButton.var,font=("IMPACT",30)).pack(side=BOTTOM)

class GameButton():
    word=[]
    var=StringVar()
    prediction=[]
    def __init__(self,frame,text,game):
        self.button=Button(frame,text=text,width=3,font=("IMPACT",15))
        self.button.configure(command=lambda:self.check(GameButton.word,self.button))
        self.game=game

    def check(self,word,button):
        try:
            place=GameButton.word.index(button["text"])
        except:
            place=-1

        if place != -1:
            button.configure(bg="green",state=DISABLED,disabledforeground="black")
            word[place]=""
            GameButton.prediction[place]=button["text"]
            GameButton.var.set(GameButton.prediction)
            if list(self.game.word)==GameButton.prediction:
                for button in self.game.lettersbox.winfo_children():
                    button.configure(state=DISABLED,disabledforeground="black")
                EndGame(1)
        else:
            button.configure(bg="red",state=DISABLED,disabledforeground="black")
            self.game.state+=1
            self.game.dead.destroy()
            self.game.dead=labelimage(Game.deadimg[self.game.state],self.game.frame)
            if self.game.state==6:
                GameButton.var.set(self.game.word)
                for button in self.game.lettersbox.winfo_children():
                    button.configure(state=DISABLED,disabledforeground="black")
                EndGame(0)

class EndGame():
    def __init__(self,state):
        frame=Frame(Container.app,bd=2,relief=GROOVE)
        frame.place(x=300,y=275,anchor=CENTER)
        if state==1:
            Label(frame,text="HAS GANADO",font=("IMPACT",40),width=15).pack(pady=10)
        else:
            Label(frame,text="HAS PERDIDO",font=("IMPACT",40),width=15).pack(pady=10)
        Button(frame,text="VOLVER A JUGAR",command=lambda:change(Game),width=15).pack(side=LEFT,padx=30,pady=10)
        Button(frame,text="VOLVER AL MENU",command=lambda:change(Menu),width=15).pack(side=RIGHT,padx=30,pady=10)

game=Container()
mainloop()
