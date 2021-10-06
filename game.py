from collections import OrderedDict
from player import Player
import world


def play():
    print("*** The mystery Of Henry Cort School ***")
    world.parse_world_dsl()
    player = Player()
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print(room.intro_text())
        room.display_room_items()
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            if player.is_hungry():
                print("You are getting hungry, you must eat something soon")
            choose_action(room, player)
        elif not player.is_alive():
            print("Your journey has come to an early end!")


def choose_action(room, player):
    action = None
    while not action:
        action_input = input("\nAction: \n")
        parts = action_input.split(" ")
        number = len(parts)
        # single commands
        if number == 1:
            verb = parts[0]
            if verb == "i" or verb == "inventory":
                player.print_inventory()
            if verb == "description" or verb == "desc":
                print(room.intro_text())
                room.display_room_items()
            if verb == "help" or verb == "h":
                player.display_stats()
        # two word commands        
        if number == 2:
            verb = parts[0]
            noun = parts[1]
            if verb == "go":
                if noun == "n" or noun == "north":
                    if world.tile_at(room.x, room.y - 1):
                        #check to see if this direction is blocked
                        if world.tile_at(room.x, room.y).get_locked_direction("N") == True:
                            print( world.tile_at(room.x, room.y).get_locked_direction_desc("N"))
                            return
                        player.move_north()
                        return
                    else:
                        print("You can't go that way")
                        return
                if noun == "s" or noun == "south":
                    if world.tile_at(room.x, room.y + 1):
                        #check to see if this direction is blocked
                        if world.tile_at(room.x, room.y).get_locked_direction("S") == True:
                            print( world.tile_at(room.x, room.y).get_locked_direction_desc("S"))
                            return
                        player.move_south()
                        return
                    else:
                        print("You can't go that way")
                        return
                if noun == "e" or noun == "east":
                    if world.tile_at(room.x + 1, room.y):
                        #check to see if this direction is blocked
                        if world.tile_at(room.x, room.y).get_locked_direction("E") == True:
                            print( world.tile_at(room.x, room.y).get_locked_direction_desc("E"))
                            return
                        player.move_east()
                        return
                    else:
                        print("You can't go that way")
                        return   
                if noun == "w" or noun == "west":
                    if world.tile_at(room.x - 1, room.y):
                        #check to see if this direction is blocked
                        if world.tile_at(room.x, room.y).get_locked_direction("W") == True:
                            print( world.tile_at(room.x, room.y).get_locked_direction_desc("W"))
                            return
                        player.move_west()
                        return
                    else:
                        print("You can't go that way")
                        return   
            if verb == "drop":
                player.drop(noun)
                return
            if verb == "take":
                player.take(noun)
                return
            if verb == "use":
                player.use(noun)
                return

def search(list, listofitems):
    for i in range(len(list)):
        if list[i] == listofitems:
            return True
    return False


# def get_available_actions(room, player):
#     actions = OrderedDict()
#     print("Choose an action: ")
#     if player.inventory:
#         action_adder(actions, 'i', player.print_inventory, "Print inventory")
#     if player.inventory:
#         action_adder(actions, 'drop', player.drop, "Drop")
#     if player.inventory:
#         action_adder(actions, 'take', player.drop, "Take")
#     if isinstance(room, world.TraderTile):
#         action_adder(actions, 't', player.trade, "Trade")
#     if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
#         action_adder(actions, 'a', player.attack, "Attack")
#     else:
#         if world.tile_at(room.x, room.y - 1):
#             action_adder(actions, 'n', player.move_north, "Go north")
#         if world.tile_at(room.x, room.y + 1):
#             action_adder(actions, 's', player.move_south, "Go south")
#         if world.tile_at(room.x + 1, room.y):
#             action_adder(actions, 'e', player.move_east, "Go east")
#         if world.tile_at(room.x - 1, room.y):
#             action_adder(actions, 'w', player.move_west, "Go west")
#     if player.hp < 100:
#         action_adder(actions, 'h', player.heal, "Heal")
# 
#     return actions
# 
# 
# def action_adder(action_dict, hotkey, action, name):
#     action_dict[hotkey.lower()] = action
#     action_dict[hotkey.upper()] = action
#     #print("{}: {}".format(hotkey, name))


play()
