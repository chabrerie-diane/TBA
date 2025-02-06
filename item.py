
"""This file contains the Item class."""

# pylint: disable=too-few-public-methods
class Item:
    """
    This class represents an item. An item is composed of a name, a description and its weight.

    Attributes:
        name (str): The name of the item/object.
        description (str): The description of the item.
        weight (int): The weight of the item.

    Methods:
        __init__(self, name, description, weight) : The constructor.
        __str__(self) : The string representation of the command.

    """

    def __init__(self, name, description, weight):
        """The constructor."""
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        """The string representation of the item."""
        return f"{self.name} : {self.description} ({self.weight} g)"
