#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mon interface
from tkinter import *
fenetre = Tk()      

# Titre de la fenêtre
fenetre.title("Dictionnaire bilingue des verbes <<Le Wiktionnaire>> FRANCAIS - ANGLAIS")

# Me connecter à la BDD
import sqlite3
conn = sqlite3.connect('dictionnaire2.db')
c = conn.cursor()

# Titre dico
l = LabelFrame(fenetre, text="Le Wiktionnaire FRANCAIS - ANGLAIS ", padx=20, pady=20)
l.pack(fill="both", expand="yes") 
Label(l, text="").pack()


## Icône du Wiktionary
can= Canvas(fenetre,bg='light gray',height=100,width=100)
can.pack(side=RIGHT, padx=50, pady=50)
fichier_img=PhotoImage(file='C:/Users/user/Desktop/Big Data M1 et M2/M1 Big Data/M1 Big DATA S1 et S2/S2/MEMOIRE M1/données/wik.png') 
img=can.create_image(50,50,image=fichier_img) 						

# Icône fenêtre
fenetre.iconbitmap('C:/Users/user/Desktop/Big Data M1 et M2/M1 Big Data/M1 Big DATA S1 et S2/S2/MEMOIRE M1/données/wik.ico')


## ALERTE
from tkinter.messagebox import *


# Traduire	
def act(): 
    mot_a_traduire = svalue.get()
    print ('%s' % mot_a_traduire)
    c.execute("SELECT title2,title3 FROM dictionnaire2 WHERE title1 =\'%s\'" % mot_a_traduire )
    print("Je cherche dans la base le mot %s :" % mot_a_traduire)
    resultat  = c.fetchall()
	
    if resultat != []:
         if resultat[0][0] == 'None':
             resultat = resultat[0][1]
         else:
             resultat = resultat[0][0]  ## else : si iwlinks existe et langliks n'existe pas ET si iwlinks existe et langlinks existe aussi 
             
      
         canvas.delete("all")
         txt = canvas.create_text(250, 40 ,text= resultat, font='Arial 13 italic', fill = 'blue', width=300)

    elif mot_a_traduire == '':
          print(" Veuillez saisir un mot !")
          showinfo("Vide!", " Aucune saisie !")
          
    else:
        print("Le mot n'existe pas dans le Wiktionnaire !")
        showinfo("Introuvable!", " Ce mot est mal orthographié ou n'a pas de traduction disponible dans le Wiktionnaire !")


### entrée
svalue = StringVar()
entree = Entry(fenetre, textvariable=svalue, width=30).pack()
canvas = Canvas(fenetre,  width=500, height=100, bg='ivory')   # Fenêtre du canevas
canvas.pack()


Button(fenetre, text ='Traduire', command=act).pack(side=TOP, padx=5, pady=5)
fenetre.mainloop()
