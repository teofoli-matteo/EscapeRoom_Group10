class BaseRoom:
    def __init__(self, name, description, items=None):
        self.name = name
        self.description = description
        self.items = [] if items is None else items

    def enter(self):
        items = ", ".join(self.items) if self.items else "None"
        return f"Room: {self.name}\nDescription: {self.description}\nItems: {items}"

    def look(self):
        return f"Room: {self.name}\nDescription: {self.description}"

    def inspect(self, item, player, logger):
        return f"Nothing special about {item}."

    def use(self, item, player, logger):
        return f"You can't use {item} here."
