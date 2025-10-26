class Player:
    def __init__(self):
        self.inventory = {}
        
    def add_token(self,key,value):
        """
        args: key: token name (keypad, dns....)
        value: token's value
        """
        self.inventory[key] = value
        
    def show_inventory(self):
        """
        return a string listing all tokens in the inventory
        """
        if not self.inventory:
            return "Nothing in"
        tokens = ', '.join(f"{k}: {v}" for k, v in self.inventory.items())
        return f"You have :\n - {tokens} \n"
        