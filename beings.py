"""This file contains the Beings class."""

# pylint: disable=too-few-public-methods
class Beings:
    """
    This class represents a being. It is the parent class of Character and Player.

    Attributes:
        name (str): Name of the being.
        current_room (Room): The current room.

    Methods:
        __init__(self, name) : The constructor.
    """

    def  __init__(self, name):
        """The constructor."""
        self.name = name
        self.current_room = None
