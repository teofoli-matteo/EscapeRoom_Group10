"""
base_room.py:
Common base class that defines shared room behavior and default interactions.
"""
class BaseRoom:
    def __init__(self, name, description, items=None):
        """
        args: name: Name of the room.
              description: Description of the room.
              items: List of items in the room. (optional)
        """
        self.name = name
        self.description = description
        self.items = [] if items is None else items

    def enter(self):
        """
        return a string with the room's name, description and items
        """
        items = ", ".join(self.items) if self.items else "None"
        return f"Room: {self.name}\nDescription: {self.description}\nItems: {items}"

    def look(self):
        """
        inspect an item in the room
        return: a string with the room's name and description
        """
        return f"Room: {self.name}\nDescription: {self.description}"

    def inspect(self, item, player, logger):
        """
        inspect an item in the room
        args: item: the item name
        player: player object (inventory, tokens....)
        logger: logger for recording game actions
        return a default string indicating nothing special
        """
        return f"Nothing special about {item}."

    def use(self, item, player, logger):
        """
        args: item: the item name
        player: player object 
        logger: logger for recording game actions
        return a default string indicating the item cannot be used here
        """
        return f"You can't use {item} here."
