"""Description: The actions module."""

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.

from inventory import Inventory

# The error message is stored in the MSG0 and MSG1 variables
#and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.                     "
# The MSG1 variable is used when the command takes number_of_parameters parameter.
MSG1 = (
    "\nLa commande '{command_word}' prend "
    "{number_of_parameters} paramètre exactement. "
)
# The MSG2 variable is used when the command go is used with an invalid direction.
MSG2 = "\nLa direction '{direction}' non reconnue.                      "
# The MSG3 variable is used when the command back is used with an empty history.
MSG3 = "\nL'historique est vide.               "
# The MSG4 variable is used when the command take is used with a wrong object.
MSG4 = "\nLe '{item}' n'est pas dans {inventaire_ou_piece}.                "
# The MSG5 variable is used when the command take is used with an object that is too heavy.
MSG5 = "\nLe '{item}' est trop lourd pour rentrer dans votre inventaire.                      "


class Actions:
    """
    This class represents an action.

    Fonctions:
        go(game, list_of_words, number_of_parameters)
        quit(game, list_of_words, number_of_parameters)
        help(game, list_of_words, number_of_parameters)
        back(game, list_of_words, number_of_parameters)
        look(game, list_of_words, number_of_parameters)
        take(game, list_of_words, number_of_parameters)
        drop(game, list_of_words, number_of_parameters)
        check(game, list_of_words, number_of_parameters)
        talk (game, list_of_words, number_of_parameters)
        clear(game, list_of_words, number_of_parameters)
        answer (game, list_of_words, number_of_parameters)

    """
    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """

        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            np = number_of_parameters
            cw = command_word
            game.warning=MSG1.format(command_word=cw,number_of_parameters=np)
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]

        #Replace the different possible expressions of the same command
        if direction in ("n", "Nord", "nord", "NORD") :
            direction = "N"
        elif direction in ("s", "Sud", "sud", "SUD") :
            direction = "S"
        elif direction in ("e", "Est", "est", "EST") :
            direction = "E"
        elif direction in ("o", "Ouest", "ouest", "OUEST") :
            direction = "O"
        elif direction in ("u", "Up", "up", "UP") :
            direction = "U"
        elif direction in ("d", "Down", "down", "DOWN") :
            direction = "D"

        #if the direction is valid
        if direction in game.possible_direction :
            # Move the player in the direction specified by the parameter.
            if not player.move(direction, game):
                game.warning = (
                    "\nAucune porte dans cette direction !                      ")
                return False
        else :
            command_word = list_of_words[0]
            game.warning = MSG2.format(direction=direction)
            game.text = player.current_room.get_long_description()
            return False

        #Moves the pnjs
        for knownroom in game.rooms :
            characters_before = list(knownroom.characters.values())
            for character in characters_before :
                character.move()
                #if DEBUG == True:
                #A ENLEVER game.text = game.text + "\nEst présent " + character.__str__()


        return True

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game (the player asked to quit).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            game.warning = MSG0.format(command_word=command_word)
            return False

        # Set the finished attribute of the game object to True.
        game.warning = "PERDU"
        game.finished = True
        return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            game.warning = MSG0.format(command_word=command_word)
            return False

        # Print the list of available commands.
        game.text = "Voici les commandes disponibles:"
        for command in game.commands.values():
            game.text = game.text + "\n\t- " + str(command)
        game.text = game.text + "\n"
        game.text += game.player.current_room.get_long_description()
        game.text += game.player.get_history()
        return True

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """
        If possible, the player goes back to the previous room.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        player = game.player
        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            game.warning = MSG0.format(command_word=command_word)
            return False

        if len(game.player.history) > 0:

            #Moves the pnjs
            for knownroom in game.rooms:
                characters_before = list(knownroom.characters.values())
                for character in characters_before:
                    character.move()

            #Goes back
            game.player.current_room= game.player.history.pop()
            if len(player.history) > 0:
                game.text = player.current_room.get_long_description() + player.get_history()
            else :
                game.text = player.current_room.get_long_description()
            return True
        game.warning = MSG3
        return False

    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        """
        Print the list of the items and pnj in the room.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        player = game.player
        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            game.warning = MSG0.format(command_word=command_word)
            return False

        Inventory.get_inventory(game, player.current_room)
        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        """
        Take an item present in the room and put it in the player's inventory.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        player = game.player
        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            cw = command_word
            np = number_of_parameters
            game.warning = MSG1.format(command_word=cw, number_of_parameters=np)
            return False

        # Get the object from the list of words.
        item_object = list_of_words[1]

        #If the object is not in the room, print an error message and return False..
        if item_object not in game.player.current_room.inventory :
            game.warning = MSG4.format(item=item_object, inventaire_ou_piece='la pièce')
            return False

        #If the maximum weight is reached, print an error message and return False.

        #Calculates the weight of is currently in inventory
        total_weight = 0
        for i in game.player.inventory.values():
            if i is not None :
                total_weight = total_weight + i.weight
        wanted_weight = total_weight + game.player.current_room.inventory.get(item_object).weight
        if  wanted_weight > game.player.inventory_weight_max :
            game.warning = MSG5.format(item=item_object)
            game.warning += f"\nLe poids total de ce que vous portez est de {total_weight} g."
            max_weight = game.player.inventory_weight_max
            game.warning += f"Le maximum de ce que vous pouvez porter est de {max_weight} g."
            object_weight = game.player.current_room.inventory.get(item_object).weight
            to_drop = object_weight -(game.player.inventory_weight_max - total_weight)
            game.warning += "Si vous voulez prendre cet item il faut que vous"
            game.warning += f"vous deparassiez de {to_drop} g au moins."
            return False

        #Put the object in the inventory.
        game.player.inventory[item_object] = game.player.current_room.inventory.get(item_object)
        del game.player.current_room.inventory[item_object]
        game.text = f"\nVous avez pris l'object {item_object}.\n"
        game.text += player.current_room.get_long_description()
        game.text += player.get_history()
        return True

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        """
        Drop an item present in the player's inventory and put it in the current room.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        player = game.player
        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            cw =command_word
            np = number_of_parameters
            game.warning = MSG1.format(command_word=cw, number_of_parameters=np)
            return False

        # Get the object from the list of words.
        item_object = list_of_words[1]

        #If the object is not in the player's inventory, print an error message and return False.
        if item_object not in game.player.inventory :
            game.warning = MSG4.format(item=item_object, inventaire_ou_piece="l'inventaire")
            return False

        #Droop the object in the room.
        game.player.current_room.inventory[item_object] = game.player.inventory.get(item_object)
        del game.player.inventory[item_object]
        game.text = f"\nVous avez déposé l'object {item_object}.\n"
        game.text +=player.current_room.get_long_description()
        game.text += player.get_history()
        return True

    @staticmethod
    def check(game, list_of_words, number_of_parameters):
        """
        See what is in the player's inventory.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        player = game.player
        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            game.warning = MSG0.format(command_word=command_word)
            return False

        Inventory.get_inventory(game, player)
        return True

    @staticmethod
    def talk (game, list_of_words, number_of_parameters):
        """Call the get_msg method (if possible) to print what the pnj has to say."""
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            cw = command_word
            np = number_of_parameters
            game.warning = MSG1.format(command_word=cw, number_of_parameters=np)
            return False

        # Get the pnj from the list of words.
        pnj = list_of_words[1]

        #If the pnj is not in the current room, print an error message and return False.
        if pnj not in  game.player.current_room.characters  :
            command_word = list_of_words[0]
            game.warning = MSG4.format(item=pnj, inventaire_ou_piece="la pièce")
            game.warning += ' ' + player.current_room.get_long_description()
            return False

        #Print a message of the character.
        player.current_room.characters[pnj].get_msg(game)
        return True

    @staticmethod
    def clear(game, list_of_words, number_of_parameters):
        """Reset the player history."""
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            game.warning = MSG0.format(command_word=command_word)
            return False

        # Set the finished attribute of the game object to True.
        player = game.player
        player.history = []
        game.text = player.current_room.get_long_description()
        return True

    @staticmethod
    def answer (game, list_of_words, number_of_parameters):
        """Answer a question. 
        In the list_of_word, there needs to be :
        -the pnj to answer to
        -the numero of the question
        -the letter of the answer.
        """
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            cw =command_word
            np = number_of_parameters
            game.warning = MSG1.format(command_word=cw, number_of_parameters=np)
            return False

        # Get the pnj from the list of words.
        pnj = list_of_words[1]
        number = int(list_of_words[2]) -1
        qcm = list_of_words[3]

        #If the pnj is not in the current room, print an error message and return False.
        if pnj not in game.player.current_room.characters :
            command_word = list_of_words[0]
            game.warning = MSG4.format(item=pnj, inventaire_ou_piece="la pièce")
            game.warning += player.current_room.get_long_description()
            return False

        #If the answer is wrong, kill the player
        if qcm != player.current_room.characters[pnj].answers[number]:
            game.text = f"Mauvaise réponse, vous êtes mort.\nMerci {game.player.name}"
            game.text += " d'avoir joué. Au revoir.\n"
            game.commands["quit"].action(game, ["quit"], game.commands["quit"].number_of_parameters)

        #Print a message of the character.
        else :
            if player.current_room.characters[pnj] == "barbaaigri":
                speach = (
                    "\nMouais, c'est ça. Bon bah là va down mais"
                    " prend garde au cyclope une fois dans le terrier, j'ai connu il"
                    " fut un temps un bon monsieur qui s'appellait Ulysse, pense a prende"
                    " ton mouton en sortant toi aussi.")
                game.player.current_room.characters[pnj].msgs.insert(0, speach)
            else :
                game.player.current_room.characters[pnj].msgs.insert(0, "\n Tout à fait. Bravo !")
            game.player.current_room.characters[pnj].get_msg(game)
        return True
