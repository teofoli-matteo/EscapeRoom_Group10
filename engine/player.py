class Player:
    def __init__(self):
        self.inventory = {}
        
    def add_token(self,key,value):
        self.inventory[key] = value
        
    def show_inventory(self):
        if not self.inventory:
            return "Nothing in"
        tokens = ', '.join(f"{k}: {v}" for k, v in self.inventory.items())
        return f"You have :\n - {tokens} \n"
        