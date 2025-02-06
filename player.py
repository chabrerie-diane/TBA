"""  This file contains the Player class. """

from beings import Beings #The parent class of Player

class Player(Beings):
    """
    This class represents a player.

    Attributes:
        name (str): Name of the player.
        current_room (Room): The current room.
        history (list) : The rooms where the player has already been.
        inventory(dict) : The inventory of the player.

    Methods:
        __init__(self, name) : The constructor.
        move(self, direction) : Moves the player in the given direction, if possible.
        get_history(self) : Return the history of where the player has been.

    """

    def __init__(self, name):
        """
        Define the constructor.
        """
        Beings.__init__(self, name)
        self.history = []
        self.inventory = {}
        self.inventory_weight_max = 200
        self.current_room = None

    def move(self, direction, game):
        """
        Define the move method.
        """
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            return False

        #add current_room to the hitory before moving to another room
        self.history.append(self.current_room)

        # Set the current room to the next room.
        self.current_room = next_room

        # Display the description of the room and the history
        game.text = self.current_room.get_long_description() + self.get_history()
        return True

    def get_history(self):
        """
        Define the method to get the history of the rooms visited by the player.
        """
        l_room =''
        for r in self.history :
            description_split =r.description.split('.')
            l_room = l_room + '- ' + description_split[0] + '\n'
        return f"Vous avez déjà visité les pièces suivantes:\n{l_room}"
