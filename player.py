import items
import world


class Player:
    def __init__(self):
        self.inventory = [items.Rock(),
                          items.Dagger(),
                          items.IDCard(),
                          #items.Tie(),
                          items.CrustyBread()]
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.hp = 24
        self.gold = 5
        self.score = 0
        self.victory = False

    def is_alive(self):
        return self.hp > 0
    
    def is_hungry(self):
        if self.hp > 0 and self.hp < 20 :
            return True
        else:
            return False
        
    
    def print_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print('* ' + str(item))
        print("Gold: {}".format(self.gold))

    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]
        if not consumables:
            print("You don't have any items to heal you!")
            return

        for i, item in enumerate(consumables, 1):
            print("Choose an item to use to heal: ")
            print("{}. {}".format(i, item))

        valid = False
        while not valid:
            choice = input("")
            try:
                to_eat = consumables[int(choice) - 1]
                self.hp = min(100, self.hp + to_eat.healing_value)
                self.inventory.remove(to_eat)
                print("Current HP: {}".format(self.hp))
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            except AttributeError:
                pass

        return best_weapon

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # reduce the players health every time they move
        self.hp = self.hp - 5

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)
        
    def drop(self, name_of_item):
        count = 0
        for x in range(0,len(self.inventory)):       
            name = self.inventory[count].name
            #print(name)
            if name == name_of_item:
                the_dropped_item = self.inventory[count]
                del self.inventory[count]
                print("Dropped : ", name )
                room = world.tile_at(self.x, self.y)
                room.add_item(the_dropped_item)
                return
            count = count + 1

    def take(self, name_of_item):
        count = 0
        room = world.tile_at(self.x, self.y)
        for x in range(0,len(room.inventory)):       
            name = room.inventory[count].name
            if name == name_of_item:
                the_taken_item = room.inventory[count]
                del room.inventory[count]
                #room.remove_item(
                print("Taken : ", name )
                #room = world.tile_at(self.x, self.y)
                #room.add_item(the_dropped_item)
                self.inventory.append(the_taken_item)
                return
            count = count + 1        

    def display_stats(self):
        print("\nYou health is : ", self.hp )
        print("\nYou score is : ", self.score )


              
        

        
