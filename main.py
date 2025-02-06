"""Description: Game class and Graphic class"""

# Import modules

import tkinter as tk
from tkinter import messagebox, PhotoImage

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character

DEBUG = True


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-instance-attributes
# Game class as written in class
class Game():
    """Game class"""

    def __init__(self):
        """ The constructor"""
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.possible_direction = set()

        self.text = "" #the text to display on the graphical interface
        self.warning = ""
        self.nb = 0 #nb of interactions with the player
        self.images = dict([('begining', 'begining.png')])

    def setup(self):
        """Setup the game"""

        # Setup commands
        help_ = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help_
        quit_ = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit_
        go_help_string = (
            " <direction> : se déplacer dans une direction cardinale (N, E, S, O),"
            " ou une direction verticale (U, D)"
        )
        go = Command("go", go_help_string, Actions.go, 1)
        self.commands["go"] = go
        back = Command("back", " : revenir en arrière", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look", " : regarder les items présents dans la pièce", Actions.look, 0)
        self.commands["look"] = look
        take_help_string = (
            " <item> : prendre un des items présents dans la pièce"
        )
        take = Command("take", take_help_string, Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " : <item> enlever un des items que l'on possède", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : regarder les items que l'on possède", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <someone> : parler à un pnj", Actions.talk, 1)
        self.commands["talk"] = talk
        clear = Command("clear", " : effacer l'historique", Actions.clear, 0)
        self.commands["clear"] = clear
        answer_help_string = (
            " <someone> <number> <letter> : "
            "repondre <letter> à la <number> question du pnj <someone>"
        )
        answer = Command("answer", answer_help_string, Actions.answer, 3)
        self.commands["answer"] = answer

        # Setup rooms

        erlenmeyer_description =(
            "une salle barba-intrigante et terrifiante."
            " Vous êtes plus pécisément sur une table parsemée d'erlenmeyers qui vous semble géants"
            " et de poils de barbi-dur."
        )
        erlenmeyer = Room("Erlenmeyer", erlenmeyer_description)
        self.rooms.append(erlenmeyer)
        self.images['Erlenmeyer'] = 'Erlenmeyer.png'
        realisation_description = (
            "une salle très haute de plafond. Un escalier en colimaçon aux marches"
            " de géant et parcemé de moutons de poussière de la taille de votre barba-bras"
            " se dessine devant vous. Vous avez l'impression d'être au sommet d'une tour géante"
        )
        realisation = Room("Realisation", realisation_description)
        self.rooms.append(realisation)
        self.images['Realisation'] = 'Realisation.png'
        wardrob_o_description = "une salle avec une armoire au nord qui cache une porte dérobée."
        wardrob_o=Room("WardrobeO",wardrob_o_description)
        self.rooms.append(wardrob_o)
        self.images['WardrobeO'] = 'WardrobeO.png'
        wardrob_e_description = (
            "la partie de droite d'une grande salle lugubre sans fenêtre de la tour."
        )
        wardrob_e = Room("WardrobeE", wardrob_e_description)
        self.rooms.append(wardrob_e)
        self.images['WardrobeE'] = 'WardrobeE.png'
        enigma_description = (
            "une salle modeste. Devant vous se tient un petit barba-monsieur à l'air malicieux."
        )
        enigma = Room("Enigma", enigma_description)
        self.rooms.append(enigma)
        self.images['Enigma'] = 'Enigma.png'
        nothing = Room("Nothing", "une salle barba-vide.")
        self.rooms.append(nothing)
        self.images['Nothing'] = 'Nothing.png'
        cyclop = Room("Cyclop", "un terrier sombre.")
        self.rooms.append(cyclop)
        self.images['Cyclop'] = 'Cyclop.png'
        farm_description = (
            "une partie du terrier où s'entassent des caméléons. Il semblerait "
            "que ce soit un élevage fait par, barba-barbarre, la marmotte borgne, "
            "elle les sort 2 fois par jour."
        )
        farm = Room("Farm", farm_description)
        self.rooms.append(farm)
        self.images['Farm'] = 'Farm.png'

        brokenglass_description = (
            "une salle dont le sol est couvert par une écatombe de fioles brisées. Le reflet du"
            " soleil sur ces fragments de verre brisé donne des couleurs irisées aux murs "
            "telle une mosaique des temps antiques."
        )
        brokenglass = Room("Brokenglass", brokenglass_description)
        self.rooms.append(brokenglass)
        self.images['Brokenglass'] = 'Brokenglass.png'
        glitter_description = (
            "une salle où se dresse au milieu une statue à paillettes rose. "
            "Cette statue représente un homme, environ la quarantaine et demi, barbu"
            " de 12 jours, petites lunettes losange sur un nez imposant, une interminablement"
            " longue blouse de scientifique sur le dos, et deux yeux roses."
        )
        glitter = Room("Glitter", glitter_description)
        self.rooms.append(glitter)
        self.images['Glitter'] = 'Glitter.png'
        evil_description =(
            "un bureau sombre. Un vilain monsieur (un humain) est concentré. "
            "Des schémas de l'intestin grèle des barba-collègues sont dessinés"
            " sur les feuilles de son bureau."
        )
        evil = Room("Evil", evil_description)
        self.rooms.append(evil)
        self.images['Evil'] = 'Evil.png'
        potionbook_description = (
            "une bibliothèque barba-lugubre. Des grimoires"
            " s'entassent un peu partout, c'est le barba-foutoir."
        )
        potionbook = Room("Potionbook", potionbook_description)
        self.rooms.append(potionbook)
        self.images['Potionbook'] = 'Potionbook.png'
        musty_description = (
            "une petit pièce humide et sombre. Les murs sont"
            " tapis d'une couche barba-épaisse de moisissure."
        )
        musty = Room("Musty", musty_description)
        self.rooms.append(musty)
        self.images['Musty'] = 'Musty.png'
        out_description =(
            "une large pièce acceuillante vu sur un jardin. Il y fait "
            "un peu frais, le vent s'engouffre par le pas d'une petite porte dissimulée."
        )
        out = Room("Out", out_description)
        self.rooms.append(out)
        self.images['Out'] = 'Out.png'
        tree_description = (
            "une parcelle de terre sur laquelle s'élève un acacia centenaire. "
            "Gloire de la nature et de Gaïa, son tronc est épais comme une maison, "
            "ses branches ont la circonférence d'une centrale nucléaire et ses "
            "feuilles sont petites comme des petites libellules.  Malheureusement pour"
            " les dryades, cet arbre garde la trace de son exploitation : "
            "des balafres multiples décorent son tronc."
        )
        tree = Room("Tree", tree_description)
        self.rooms.append(tree)
        self.images['Tree'] = 'Tree.png'
        monkey_description =(
            "l'arbre, devant vous il y a une cabane. Derrière celle-ci"
            " est caché un barba-singe qui semble s'être échappé de la"
            " salle des essais cliniques."
        )
        monkey = Room("Monkey", monkey_description)
        self.rooms.append(monkey)
        self.images['Monkey'] = 'Monkey.png'
        bread_description =(
            "une étendue d'herbe. Chaque brin d'herbe vous arrive à l'épaule."
            " Une miette de pain est juste devant vous."
        )
        bread = Room("Bread", bread_description)
        self.rooms.append(bread)
        self.images['Bread'] = 'Bread.png'
        storage = Room("Storage", "une grange.")
        self.rooms.append(storage)
        self.images['Storage'] = 'Storage.png'
        lake = Room("Lake", "un petit lac.")
        self.rooms.append(lake)
        self.images['Lake'] = 'Lake.png'

        # Create exits for rooms

        erlenmeyer.exits = {"N":None, "E":None, "S":None, "O":realisation, "U":None, "D":wardrob_e}
        realisation.exits = {"N":None, "E":erlenmeyer, "S":None , "O":None, "U":None, "D":None}
        evil.exits = {"N":None, "E":potionbook, "S":None, "O":None, "U":None, "D":glitter}
        potionbook.exits = {"N":None, "E":None, "S":None, "O":evil, "U":None, "D":None}

        wardrob_o.exits = {"N":glitter, "E":wardrob_e, "S":None, "O":None, "U":None, "D":None}
        wardrob_e.exits = {"N":None, "E":None, "S":None, "O":None, "U":None, "D":enigma}
        brokenglass.exits = {"N":None, "E":None, "S":None, "O":glitter, "U":None, "D":None}
        glitter.exits = {"N":None, "E":brokenglass, "S":wardrob_o, "O":None, "U":evil, "D":out}
        monkey.exits = {"N":None, "E":None, "S":None, "O":None, "U":None, "D":tree}

        enigma.exits = {"N":None, "E":None, "S":None, "O":None, "U":None, "D":cyclop}
        nothing.exits = {"N":None, "E":None, "S":None, "O":None, "U":wardrob_o, "D":None}
        cyclop.exits = {"N":None, "E":farm, "S":None, "O":None, "U":None, "D":None}
        farm.exits = {"N":None, "E":None, "S":None, "O":None, "U":nothing, "D":None}


        musty.exits = {"N":None, "E":None, "S":None, "O":out, "U":brokenglass, "D":None}
        out.exits = {"N":None, "E":musty, "S":None, "O":tree, "U":glitter, "D":None}
        tree.exits = {"N":None, "E":out, "S":bread, "O":None, "U":monkey, "D":None}
        bread.exits = {"N":tree, "E":None, "S":None, "O":storage, "U":None, "D":None}
        storage.exits = {"N":lake, "E":bread, "S":None, "O":None, "U":None, "D":None}
        lake.exits = {"N":None, "E":tree, "S":storage, "O":None, "U":None, "D":None}

        #Setup items of the rooms

        armoire = Item("armoire", "l'armoire entrouverte", 10000)
        wardrob_o.inventory["armoire"] = armoire
        cameleon = Item("cameleon", "un bébé caméléon", 145)
        farm.inventory["cameleon"] = cameleon

        verre_description = "une poignée de mini bouts de verres aussi jolis que des diamants"
        verre = Item("verre", verre_description, 10)
        brokenglass.inventory["verre"] = verre
        page_description = (
            "un bout de page déchiré avec griffonné dessus une recette"
            " de barba-pancake !grandissant! :\nfarine, eau, levure, banane, seve"
        )
        page = Item("page", page_description, 0.1)
        potionbook.inventory["page"] = page

        seve = Item("seve", "une goutte de sève (issue du tronc)", 10)
        tree.inventory["seve"] = seve
        banane = Item("banane", "une barba-banane naine", 50)
        monkey.inventory["banane"] = banane
        farine = Item("farine", "un petit reste de farine", 50)
        storage.inventory["farine"] = farine
        levure = Item("levure", "un petit reste de moisissure (de la levure ?))", 10)
        musty.inventory["levure"] = levure
        sucre = Item("sucre", "une bonne poignée de grains de sucres", 14)
        storage.inventory["sucre"] = sucre
        pomme = Item("pomme", "une pomme entière", 300)
        storage.inventory["pomme"] = pomme
        pain = Item("pain", "un grosse miette de pain sec", 40)
        bread.inventory["pain"] = pain
        eau = Item("eau", "une demi goutte d'eau", 20)
        lake.inventory["eau"] = eau


        #Setup characters of the rooms

        ptitb_q1 = (
            "1ere question : Qui es-tu ?\na : "
            "Je suis comme toi, je suis un barbapapa qui a rétréci.\n"
            "b : Je suis barba-perdu."
        )
        ptitb_d = "un barbapapa qui n'arrête pas de changer de forme"
        petitbarba = Character("petitbarba",ptitb_d,realisation,["Bonjour", ptitb_q1],[realisation])
        realisation.characters["petitbarba"] = petitbarba
        petitbarba.answers = ["a"]
        mote_q1 =(
            "1ere question:\na : Tu veux te battre avec moi ?\n"
            "b : Ou coopère et enfonce toi encore plus dans le terrier"
        )
        mote_q2 = (
            "2eme question : Bon tu viens?\na : Oui\nb : Non"
        )
        marmotte =Character("marmotte","une marmotte balèze",cyclop,[mote_q1,mote_q2],[cyclop,farm])
        cyclop.characters["marmotte"] = marmotte
        marmotte.answers = ["b", "a"]
        vil_p2 = (
            "Qui va là ? *il vous regarde droit dans "
            "les yeux mais ne vous voit pas grâce au caméléon"
            " qui vous rend invisible* Bon je ne vois personne."
        )
        vilain = Character("vilain", "un monsieur à l'air vilain", evil, ["Hum", vil_p2], [evil])
        evil.characters["vilain"] = vilain

        aigri_q1 = (
            "Vous m'avez réveillé barba-filou;\nVotre survie dépend"
            " maintenant de la réponse à cette 1ere question : Qu'est-ce qui "
            "est petit et qui barba-attend ? \na : Barbotine\nb : "
            "Barba-jonathan\nc : Vous\nd : Jonathan"
        )
        aigri_d ="le barba-monsieur à l'air malicieux"
        barbaaigri = Character("barbaaigri", aigri_d, enigma, [aigri_q1], [enigma])
        enigma.characters["barbaaigri"] = barbaaigri
        barbaaigri.answers = ["c"]

        singe_d ="un barba-singe qui s'est échappé des laboratoires"
        singe = Character("barba-singe", singe_d, monkey, ["Prend cette banane"], [monkey, tree])
        monkey.characters["barba-singe"] = singe

        #Set of all the possible directions
        self.possible_direction = {k for r in self.rooms for k in r.exits.keys() }

        # Setup starting room
        self.player.current_room = erlenmeyer

        #A ENLEVER POUR TESTER
        #Setup the text to display
        self.text = self.player.current_room.get_long_description()

    def get_current_text(self):
        """Returns the current question"""
        if self.nb == 0:  #if it is the first interaction of the game
            self.text = "\nEntrez votre nom: "
        elif self.nb == 1: #if it is the second interaction of the game
            self.text = f"\nBienvenue {self.player.name} dans ce jeu d'aventure !\n"
            self.text += "Entrez 'help' si vous avez besoin d'aide.\n"
        return self.text

    def execute_command(self, command, list_of_words):
        """If the command is recognized (verified in treat_command), 
        execute it (used in the methode treat_command of the Class Graphic)"""
        command.action(self, list_of_words, command.number_of_parameters)



class Graphic(tk.Tk, Game):
    """Class of the graphical interface with tkinter"""

    def __init__(self):
        """The constructor."""
        tk.Tk.__init__(self)
        Game.__init__(self)
        self.title("Jeu d'Aventure")
        self.geometry("800x900")
        self.background = PhotoImage(file = self.images["begining"])
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets of the interface"""
        # Background
        self.image_label = tk.Label(self, image = self.background)
        self.image_label.place(x=0, y=0, relwidth = 1, relheight = 1)
        # Text box to display text
        self.text_label=tk.Label(self,text=self.get_current_text(),font=("Arial",14),wraplength=700)
        self.text_label.pack(pady=20)
        #Text area to enter the response
        self.answer_entry = tk.Entry(self, font=("Arial", 14), width=30)
        self.answer_entry.pack(pady=10)
        # Button to submit the answer. This button is what calls the fonction treat_command.
        self.submit_button = tk.Button(self,text="Soumettre", font=("Arial", 14), command=self.treat_command) # pylint: disable=line-too-long
        self.submit_button.pack(pady=10)

    def treat_command(self):
        """Process the answer and move to the next question"""
        command_string = self.answer_entry.get()

        if self.nb == 1:
            self.setup()

        elif self.nb == 0:
            self.player = Player(command_string)

        elif  len(command_string) != 0 :
            # Split the command string into a list of words
            list_of_words = command_string.split(" ")

            command_word = list_of_words[0]

            # If the command is not recognized, display an error message
            if command_word not in self.commands:
                warn = f"\nCommande '{command_word}' non reconnue. "
                warn += "Entrez 'help' pour voir la liste des commandes disponibles.\n"
                messagebox.showwarning(warn)
            # If the command is recognized, execute it
            else:
                command = self.commands[command_word]
                self.execute_command(command, list_of_words)

        #If the game is not ended, update the graphical interface
        #(does not get the command from the player,
        #it is the push of the submit_button that calls the treat_command)
        if not self.finished:
            if ("farine" in self.player.inventory
                and "levure" in self.player.inventory
                and "eau" in self.player.inventory
                and "banane" in self.player.inventory
                and "seve" in self.player.inventory):
                self.text = "Vous avez réussi à retrouver votre barba-taille d'origine, bravo."
                score = self.nb
                self.text+= f"\nVous avez eu besoin de {score} commandes!"
                self.warning = f"FELICITATION {self.player.name}"
                self.background = PhotoImage(file = self.images["begining"])
                self.finished = True
            else:
                self.update_widgets()
        if self.finished:
            self.end_game()

    def update_widgets(self):
        """Updates the displayed question"""
        #increases the numbers of interactions
        self.nb = self.nb + 1
        # Clear the response entry (clear what was written by the player)
        self.answer_entry.delete(0, tk.END)
        #Shows the new text / question
        self.text_label.config(text=self.get_current_text())
        #New image of the current room in the background
        if self.nb > 1 :
            self.background = PhotoImage(file = self.images[self.player.current_room.name])
            self.image_label.config(image = self.background)
        #Popup (messagebox) if there is a warning
        if self.warning != "" :
            messagebox.showwarning(self.warning)
        self.warning = ""

    def end_game(self):
        """End of game"""
        self.image_label.config(image = self.background)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.config(state='disabled')
        self.text_label.config(text=self.text)
        messagebox.showinfo(self.warning)
        self.quit_game()

    def quit_game(self):
        """Quit the game permanently"""
        self.destroy()

def main():
    """Start the game"""
    # Create a game objet and play the game
    jeu = Graphic()
    #displays the main window on the screen and then waits for the user to take an action.
    jeu.mainloop()

if __name__ == "__main__":
    main()
