""" This file contains the Character class. """

import random
import copy
from beings import Beings #The parent class of Character

# pylint: disable = too-many-arguments
# pylint: disable = too-many-positional-arguments
class Character(Beings):
    """
    This class represents a character.

    Attributes:
        name (str): Name of the pnj.
        description (str): The description of the pnj.
        current_room (Room): The current room.
        msgs (list): The list of the messages to print when interracting with the pnj.
        area (list): The list of the rooms that are accessible to the pnj.

    Methods:
        __init__(self, name, description, action, current_room, msgs) : The constructor.
        __str__(self) : The string representation of the command.
        move(self) : Moves the pnj or not.
        get_msg(self) : Print what the pnj has to say.

    """

    def  __init__(self, name, description, current_room, msgs, area):
        Beings.__init__(self, name)
        self.current_room = current_room
        self.description = description
        self.msgs = msgs
        self.area = area
        self.answers = []

    def __str__(self):
        return f"{self.name} : {self.description}"

    def move(self):
        """
        Define the move method.
        Characters have one chance out of tree to go to an adjacent room or not. 
        """
        #The list of the rooms the pnj can go in
        rooms = copy.copy(self.area)
        rooms.remove(self.current_room)

        #The pnj has a 1/3 probability of going in one of those rooms
        if random.randint(0,2) == 1 and rooms != [] and rooms is not None:
            room = random.choice(rooms)
            del self.current_room.characters[self.name]
            self.current_room = room
            self.current_room.characters[self.name] = self
            return True
        return False

    def get_msg(self, game):
        """
        Get the message of a png
        """
        #if some conditions are met, a message is unlocked

        #if the player has the item "page" in its inventory, the monkey helps him
        if self.name == "barba-singe" :
            if "page" in game.player.inventory :
                self.msgs.insert(0,"\nTu as juste a récupérer les bons ingrédiens pour t'en sortir")
        #if the player has the item "cameleon" in its inventory, the vilain does not kill him
        if self.name == "vilain" :
            if "cameleon" not in game.player.inventory :
                game.text = "Il vous a vu et vous êtes mort."
                game.text += f"Merci {game.player.name} d'avoir joué. Au revoir.\n"
                q = "quit"
                game.commands[q].action(game.command[q], [q], game.command[q].number_of_parameters)
        #print the messages in a rotating manner
        msg = self.msgs.pop(0)
        player = game.player
        game.text = "\n" + msg + "\n"
        game.text += player.current_room.get_long_description() + player.get_history()
        self.msgs.append(msg)
