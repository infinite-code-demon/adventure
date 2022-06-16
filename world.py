import enemies
import items
import npc
import random
from items import IDCard
from items import Key
from items import Tie

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.locked = False
        self.inventory = []
        self.locked_directions_dict = {"N":False,"E":False,"S":False,"W":False}
        self.locked_directions_text_dict = {"N":"","E":"","S":"","W":""}
        self.locked_directions_keyname_dict = {"N":"","E":"","S":"","W":""}
        self.locked_directions_name_dict = {"N":"","E":"","S":"","W":""}
        
        
    
    # if you want to make a map tile locked then set this True
    #def set_lock(self, state):
    #    self.locked = state
    
    # return the state of the room - its unlocked if the player has the item required.
    def get_lock(self, player):
        if self.locked == False :
            return False
        count = 0
        for x in range(0,len(player.inventory)):       
            name = player.inventory[count].name
            if name == "IDCard":
                #the_key_item = player.inventory[count]
                #del self.inventory[count]
                #print("key item = : ", name )
                self.locked = False
                #print("you unlockled it")
                print(self.unlocked_text())
                return self.locked
            count = count + 1
        return self.locked

    # a list of directions that are locked - eg. "n" "s" etc
    def add_locked_direction(self,direction):
        self.locked_directions.append(direction)

    def set_locked_direction(self,direction,desc,name,keyname):
        # direction N,S,E or W
        self.locked_directions_dict[direction] = True
        # desc is the text that describes the locked door 
        self.locked_directions_text_dict[direction] = desc
        # keyname is the name of the object that unlocks that direction
        self.locked_directions_keyname_dict[direction] = keyname
        # name is the item name of the locked - eg door or window
        self.locked_directions_name_dict[direction] = name
        #print(self.locked_directions_dict)
        #print(self.locked_directions_text_dict)
        
    def get_locked_direction(self,direction):
        # to make things easier, check if the player is carrying the item that can unlock
        # the direction they want to go in, if they have it then unlock automatically
        # call the "get_lock" function to go thru the players inventory and see if it 
        # matches the locked direction, if it does then unlock
        if self.locked_directions_dict[direction] == True:
            return True
        else:
            return False

    def get_locked_direction_desc(self,direction):
        if self.locked_directions_dict[direction] == True:
            return self.locked_directions_text_dict[direction]
        else:
            return None


    # once a direction has been unlocked it doesnt have to be opened again
    def remove_locked_direction(self,direction):
        self.locked_directions_dict[direction] = False
        self.locked_directions_text_dict[direction] = None
        self.locked_directions_name_dict[direction] = None
        self.locked_directions_keyname_dict[direction] = None   
        
        
    def unlock_direction(self,direction,key,name):
        # first see if the player is using the correct key
        if key == self.locked_directions_keyname_dict[direction]:
            if name == self.locked_directions_name_dict[direction]:
                # unlocked ok
                remove_locked_direction(direction)
                print(name, " unlocked OK")
                return True
            else:
                print(name, " cannot be unlocked")
                return False
        else:
            print(key," is not the right key to unlock ",name)
            return False
        
    def unlock(self, item_to_use):
        return
        
    def add_item(self,an_item):
        self.inventory.append(an_item)
    
    def remove_item(self,an_item):
        self.inventory.remove(an_item)

    def get_items(self):
        return self.inventory

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    # print a message that relates to something being locked
    def locked_text(self):
        raise NotImplementedError("Create a subclass instead!")

    # print a message that relates to user unlocking something
    def unlocked_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass
    
    def display_room_items(self):
        if len(self.inventory) == 0:
            return
        else:
            print("You can see : ")
            for item in self.inventory:
                print('* ' + str(item))


class StartTile(MapTile):
    def intro_text(self):
        return """
        You stand near to the school entrance.
        To enter the school go north.
        """


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant spider jumps down from " \
                              "its web in front of you!"
            self.dead_text = "The corpse of a dead spider " \
                             "rots on the ground."
        elif r < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "An ogre is blocking your path!"
            self.dead_text = "A dead ogre reminds you of your triumph."
        elif r < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squeaking noise growing louder" \
                              "...suddenly you are lost in s swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground."
        else:
            self.enemy = enemies.RockMonster()
            self.alive_text = "You've disturbed a rock monster " \
                              "from his slumber!"
            self.dead_text = "Defeated, the monster has reverted " \
                             "into an ordinary rock."

        super().__init__(x, y)


    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".
                  format(self.enemy.damage, player.hp))


class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True

    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!
        """


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print("+{} gold added.".format(self.gold))

    def intro_text(self):
        if self.gold_claimed:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        else:
            return """
            Someone dropped some gold. You pick it up.
            """

class FindKeyTile(MapTile):
    def __init__(self, x, y):
        self.key_claimed = False
        super().__init__(x, y)

    def intro_text(self):
        #if self.key_claimed:
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

class RoomTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().add_item(IDCard())
        super().add_item(Key())

    def intro_text(self):
        return """
        You find yourself in an ordinary office room
        """

class CarParkTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def intro_text(self):
        return """
        You are standing in the car park. There isnt much here.
        """
    
class CarTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().set_lock(True)
        super().add_item(Tie())

    def locked_text(self):
        return """
        There is a car here, looks like there is something on seat. Unfortunately the car is locked
        Maybe you need to find a key and use it to unlock the car.
        """

    def intro_text(self):
        return """
        You are standing in the car park. There isnt much here.
        """

    def unlocked_text(self):
        return """
        You have unlocked the car.
        """

class CarParkTieTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().add_item(Tie())

    def intro_text(self):
        return """
        You are standing in the car park.
        """

class HedgeTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        #super().set_lock(True)

    def intro_text(self):
        return """
        Nothing here apart from a hedge.
        """


class TestTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().set_locked_direction("N","That way is locked, perhaprs an IDCard would unlock the door?","Door","IDCard")
        super().set_locked_direction("E","That was is locked, try bashing it with a Rock","Window","Rock")
        
    def intro_text(self):
        return """
        Test tile to check for lock
        """


    
class SchoolEntranceTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def modify_player(self, player):
        got_tie = False
        for item in player.inventory:
            if item.name == "Tie":
                print("you can enter")
                got_tie = True
        if got_tie == False:
            player.hp = player.hp - 100
            print("No tie, game over" )
                         
    def intro_text(self):
        return """
        Entrance to your school.
        """
    
class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                return
            elif user_input in ['B', 'b']:
                print("Here's whats available to buy: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                print("Here's whats available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Gold".format(i, item.name, item.value))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Invalid choice!")

    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("That's too expensive")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print("Trade complete!")

    def intro_text(self):
        return """
        A frail not-quite-human, not-quite-creature squats in the corner
        clinking his gold coins together. He looks willing to trade.
        """

world_dsl = """
|EN|EN|VT|EN|EN|
|EN|  |  |  |EN|
|EN|FG|KT|  |TT|
|TT|RT|SE|FG|EN|
|CP|CP|ST|CP|CP|
|CP|HG|XX|HG|CP|
|CP|  |CP|TT|CP|
"""


def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True

tile_type_dict = {"VT": VictoryTile,
                  "EN": EnemyTile,
                  "ST": StartTile,
                  "FG": FindGoldTile,
                  "TT": TraderTile,
                  "KT": FindKeyTile,
                  "RT": RoomTile,
                  "CP": CarParkTile,
                  "CT": CarTile,
                  "TT": CarParkTieTile,
                  "XX": TestTile,
                  "HG": HedgeTile,
                  "SE": SchoolEntranceTile,
                  "  ": None}


world_map = []

start_tile_location = None


def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)


def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None
