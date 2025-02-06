""" Define the Room class. """

class Room:
    """
    This class represents a room. A room is composed of a name, a description, a direction.

    Attributes:
        name (str): The name of the room.
        description (str): The description of the room.
        direction (function): The direction the player wants to go to.

    Methods:
        __init__(self, name, description) : The constructor.
        get_exit(self, direction) : The string representation of the command.
        get_exit_string(self) :
        get_long_description(self) :

    Examples:

    >>> from actions import go
    >>> command = Command("go", "Permet de se déplacer dans une direction.", go, 1)
    >>> command.command_word
    'go'
    >>> command.help_string
    'Permet de se déplacer dans une direction.'
    >>> type(command.action)
    <class 'function'>
    >>> command.number_of_parameters
    1

    """
    # Define the constructor.
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}

    # Define the get_exit method.
    def get_exit(self, direction):
        """
        Return the room in the given direction if it exists.
        """
        if direction in self.exits.values():
            return self.exits[direction]
        return None

    def get_exit_string(self):
        """
        Return a string describing the room's exits.
        """
        exit_string = "Sorties: "
        for direction, room in self.exits.items():
            if room is not None:
                exit_string += direction + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    def get_long_description(self):
        """
        Return a long description of this room including exits.
        """
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
