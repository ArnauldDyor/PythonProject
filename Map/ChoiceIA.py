from tkinter import *

class ChoiceIA:
    
    def __init__(self):

        self.IA = -1

        self.fenetre = Tk()
        self.fenetre.title("IA Choice")
        self.fenetre.minsize(500, 250)
        self.fenetre.config(bg='#00997b')

        self.champ_label = Label(self.fenetre, text="Choisit ton IA", font='Arial 15 bold', height=2, bg='#00997b')
        self.champ_label.pack(side = BOTTOM)

        self.canevas = Canvas(self.fenetre, width=300, height=200, bg='#00997b')
        self.canevas.pack()

        self.listbox = Listbox(self.canevas, selectmode='single')
        self.listbox.insert(1, "IA VICTOR")
        self.listbox.insert(1, "IA ARNAULD")
        self.listbox.insert(3, "IA ILES")
        self.listbox.pack()

        self.button = Button(self.canevas, text='       Sélectionner       ', command=self.ia_choice_button_click)
        self.button.pack(side=TOP)

        self.fenetre.mainloop()

    def ia_choice_button_click(self):
        if len(self.listbox.curselection()) < 1:
            return
        self.IA = self.listbox.curselection()[0]
        self.fenetre.quit()
        self.fenetre.destroy()

    def getIA(self):
        return self.IA