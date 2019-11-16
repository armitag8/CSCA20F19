import os
from game_data import World, Item, Location
from player import Player

if __name__ == "__main__":
    WORLD = World()
    PLAYER = Player(0, 0)  

    menu = ["look", "inventory", "score", "quit"]
    quit = False
    
    while not PLAYER.victory and PLAYER.moves_remaining > 0 and quit == False:
        location = WORLD.get_location(PLAYER.x, PLAYER.y)

        if location.is_new():
            print(location.get_full_description())
            PLAYER.score += location.points
        else:
            print(location.get_brief_description())
        location.visit()

        print('You have ' + str(PLAYER.moves_remaining) + ' moves remaining.')
        print("What shall you do? \n")
        print("Menu")
        for action in WORLD.get_available_actions(location, 
                                                  PLAYER.get_inventory()):
            print(action)
        choice = ''

        while (choice not in WORLD.get_available_actions(location, 
                                                        PLAYER.get_inventory())
                and quit == False):
            choice = input("\nChoose action: ").title()
            if choice == '[menu]' or  choice == 'Menu':
                print("Menu Options: \n")
                for option in menu:
                    print(option)
            
            elif choice == 'Look':
                print(location.get_full_description())

            elif choice == 'Inventory':
                print('Your inventory:\n')
                for item_name in PLAYER.get_inventory():
                    print(item_name)

            elif choice == 'Score':
                print('\nYour currrent score is: ' + str(PLAYER.score))

            elif choice == 'Quit':
                WORLD.save_items()
                PLAYER.save()
                quit = True
            
            elif choice not in WORLD.get_available_actions(location, 
                                                        PLAYER.get_inventory()):
                print('''Sorry, but you can't do that here. Type menu for free actions, or choose from list above.''')

        if choice == 'Go South':
            PLAYER.move_south()
        elif choice == 'Go North':
            PLAYER.move_north()
        elif choice == 'Go East':
            PLAYER.move_east()
        elif choice == 'Go West':
            PLAYER.move_west()

        elif choice[:4] == 'Take':
            item = location.get_items()[choice[5:].title()]
            PLAYER.add_item(item)
            location.remove_item(item)
            if item.get_target_location() == location.location_num:
                PLAYER.score -= item.get_target_points()            
        elif choice[:4] == 'Drop':
            item = PLAYER.get_inventory()[choice[5:].title()]
            location.add_item(item)
            PLAYER.remove_item(item)
            if item.get_target_location() == location.location_num:
                PLAYER.score += item.get_target_points()
                
        elif choice == 'Cut Lock':
            WORLD.locked = False
            PLAYER.move(1, 5)
        elif choice == 'Close Locker':
            bolt_cutters = PLAYER.get_inventory()['Bolt Cutter']
            location.add_item(bolt_cutters)
            PLAYER.remove_item(bolt_cutters)
            if bolt_cutters.get_target_location() == location.location_num:
                PLAYER.score += bolt_cutters.get_target_points()
            PLAYER.move(-1, -5)
                
        if PLAYER.score >= 50 and quit:
            PLAYER.victory = True

    if PLAYER.victory:
        print('Congratulations! You passed the exam!')
        os.remove('pers_items.txt')
        os.remove('save_game.txt')
    elif not quit:
        print('Game over. Better luck next time')
        os.remove('pers_items.txt')
        os.remove('save_game.txt')        
    if PLAYER.score > 100:
        PLAYER.score = 100
        
    print("You finished with a 'mark' of " + str(PLAYER.score) + '%')
