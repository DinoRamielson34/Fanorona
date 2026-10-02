from tkinter import *
from fanorina.Fanorina import Fanorina

class Plateau:
    def __init__(self):
        self.root = Tk()
        self.root.title("Fanorina")
        self.root.geometry("600x600")

        self.canvas = Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack()

        self.fanorina = Fanorina(self.canvas)
        self.canvas.bind("<Button-1>", self.fanorina.clic)

        # Créer le label explicatif des modes de jeu
        self.create_instructions_label()

        self.root.mainloop()
        
    def create_instructions_label(self):
        """Crée une étiquette avec les instructions du jeu"""
        instructions = """Modes de jeu:
- Humain vs IA: Jouez contre l'IA
- Humain vs Humain: Jouez à deux
- IA vs IA: Regardez deux IAs s'affronter (utilisez 'Tour suivant IA')

En début de partie, le pion noir peut être placé pour bloquer une case."""
        
        instructions_label = Label(self.root, text=instructions, justify=LEFT, 
                                  anchor='w', bg="lightgray", padx=10, pady=10)
        instructions_label.place(x=50, y=10, width=500)