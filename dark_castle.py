"""Castle Adventure 1.572

This is a simple Zork-like text adventure game.
I am creating it in order to learn how to program in Python.

Written and programmed by Tom Snellgrove

Last update = Mar 17, 2020
"""

# *** Imports ***
import random
import math


# *********************
# --- Situational Logic
# *********************


def switch_value(switch_key, switch_dict):
    # *** Upon pressing the big_red_button returns binary lever value ***

    if switch_key == 'push-big_red_button':
        temp_value = 0
        if switch_dict['left_lever']['state'] == 'up':
            temp_value += 4
        if switch_dict['middle_lever']['state'] == 'up':
            temp_value += 2
        if switch_dict['right_lever']['state'] == 'up':
            temp_value += 1
    return(temp_value)


def trigger(room, trigger_key, room_dict, word2, timer_dict, description_dict,
            state_dict, titles_dict, door_dict, score_dict, creature_dict):
    # *** Situational triggers and switch results ***

    if trigger_key == 'take-shiny_sword':
        if room == 'main_hall' and 'hedgehog' in room_dict[room]['features'] \
                and 'stale_biscuits' not in room_dict[room]['view_only'] \
                and 'shiny_sword' in room_dict[room]['items']:
            print(description_dict[trigger_key])
            return(True)

    elif (trigger_key == 'east-blank') or (trigger_key == 'west-blank'):
        if room == 'entrance' and ('grimy_axe' in state_dict['hand']
                    or 'shiny_sword' in state_dict['hand']):
            if score_dict['gator-crown'][0] == 0:
                print(description_dict['east-blank-crown'])
                state_dict['backpack'].append('royal_crown')
                score('gator-crown', score_dict, state_dict)
                return(True)
            else:
                print(description_dict['east-blank-no_crown'])
                return(True)

    elif trigger_key == 'drop-stale_biscuits':
        if room == 'main_hall' and 'hedgehog' in room_dict[room]['features']:
            room_dict[room]['items'].remove(word2)
            room_dict[room]['view_only'].append(word2)
            state_dict['active_timer'] = 'drop-stale_biscuits'
            timer_dict['drop-stale_biscuits']['timer'] = 5
            creature_dict['hedgehog']['state'] = 'hedgehog_eating'
            description_update(
                'hedgehog', 'hedgehog_eating', description_dict)
            return
    
    elif trigger_key == 'drop-shiny_sword':
        if room == 'main_hall' and 'hedgehog' in room_dict[room]['features'] \
                and state_dict['active_timer'] != 'drop-stale_biscuits':
            creature_dict['hedgehog']['state'] = 'hedgehog_fed_sword_returned'
            description_update(
                'hedgehog', 'hedgehog_fed_sword_returned', description_dict)
            print(description_dict[trigger_key])
            room_dict[room]['items'].append('silver_key')
            return
    
    elif trigger_key == 'attack-goblin':
        if room == 'antechamber' \
                and 'dead_goblin' in room_dict[room]['features']:
            room_dict[room]['view_only'].extend(
                ['left_lever', 'middle_lever', 'right_lever', 'big_red_button']
                )
            return

    elif trigger_key == 'pull-throne':
        if not state_dict['hedgehog_broach_found']:
            print(description_dict[trigger_key])
            room_dict[room]['items'].append('hedgehog_broach')
            state_dict['hedgehog_broach_found'] = True
        return

    elif trigger_key == 'push-throne':
        if not state_dict['hedgehog_broach_found']:
            print(description_dict[trigger_key])
        return

    elif trigger_key == 'read-illuminated_letters':
        if room != 'throne_room':
            print(description_dict['read-illuminated_letters-wrong_room'])
        elif 'hedgehog' not in room_dict['main_hall']['features']:
            print(description_dict['read-illuminated_letters-no_hedgehog'])
        elif 'royal_crown' not in state_dict['worn']:
            print(description_dict['read-illuminated_letters-no_crown'])
        else:
            print(description_dict['read-illuminated_letters-win'])
            score(trigger_key, score_dict, state_dict)
            state_dict['game_ending'] = 'won'
            end(state_dict, titles_dict)
            credits()
            exit()

    elif trigger_key in [
            'examine-control_panel', 'open-iron_portcullis',
            'examine-iron_portcullis', 'examine-grimy_axe', 'north-blank']:
        if room == 'antechamber' and 'goblin' in room_dict[room]['features'] \
                and 'shiny_sword' in state_dict['hand']:
            print(description_dict['goblin_attacks-parry'])
            return(True)
        elif room == 'antechamber' and 'goblin' in room_dict[room]['features']\
                and 'shiny_sword' 'shiny_sword' not in state_dict['hand']:
            print(description_dict['goblin_attacks-death'])
            end(state_dict, titles_dict)
            exit()
        else:
            return(False)

    elif trigger_key == 'push-big_red_button-success':
        if door_dict['iron_portcullis']['door_state'] == 'closed':
            door_dict['iron_portcullis']['door_state'] = 'open'
            print(description_dict['push-big_red_button-open'])
            description_dict['iron_portcullis'] = \
                description_dict['iron_portcullis-base'] + "open.\n"
        else:
            door_dict['iron_portcullis']['door_state'] = 'closed'
            print(description_dict['push-big_red_button-close'])
            description_dict['iron_portcullis'] = \
                description_dict['iron_portcullis-base'] + "closed.\n"

    return


def timer(room, room_dict, timer_dict, state_dict, description_dict):
    # *** Timer conditionals ***

    timer_key = state_dict['active_timer']

    if timer_key == 'drop-stale_biscuits':

        # *** If the hedgehog no longer exists (i.e. attacked by player), ***
        # *** reset timer_value to 0 and set active_timer to none ***
        # *** and remove 'stale_biscuits' from 'view_only' ***
        if 'hedgehog' not in room_dict['main_hall']['features']:
            timer_dict['drop-stale_biscuits']['timer'] = 0
            state_dict['active_timer'] = 'none'
            room_dict['main_hall']['view_only'].remove('stale_biscuits')
            return

        # *** If hedgehog exist and room == main_hall print description ***
        if room == 'main_hall':
            print(timer_dict['drop-stale_biscuits']['timer_txt_'
                + str(timer_dict['drop-stale_biscuits']['timer'])])

        # *** decrement timer ***
        timer_dict['drop-stale_biscuits']['timer'] -= 1

        # *** if timer == 0 reset 'active_timer' & remove 'stale_biscuits' ***
        if timer_dict['drop-stale_biscuits']['timer'] == 0:
            state_dict['active_timer'] = 'none'
            room_dict['main_hall']['view_only'].remove('stale_biscuits')

            # *** update hedgehog state & description based on shiny_sword ***
            if 'shiny_sword' in room_dict['main_hall']['items']:
                creature_dict['hedgehog']['state'] = 'fed_sword_returned'
                description_update(
                    'hedgehog', 'hedgehog_fed_sword_not_taken',
                    description_dict)
            else:
                creature_dict['hedgehog']['state'] = 'fed_sword_taken'
                description_update(
                    'hedgehog', 'hedgehog_fed_sword_taken',
                    description_dict)

        return

# *******************
# --- Helper Routines
# *******************


def unknown_word():
    response = random.randint(0, 4)
    print(unknown_word_lst[response])
    state_dict['move_counter'] -= 1


def help():
    print(
        "One word commands: 'help', 'inventory', 'look', 'north', 'south', "
        "'east', 'west', 'score'\n")
    print(
        "Verb-noun commands: 'take' <item>, 'drop' <item>, "
        "'attack' <creature>, \n'open' <door or container>, "
        "'unlock' <door or container>, 'examine' <room, feature, or item>,\n"
        "read <writing>, eat <food>, pull <lever>, push <button>, "
        "wear <garment>.\n")
    print(
        "Items not in your hand are stored in your backpack. You can view "
        "them using 'inventory'. You can 'take' one object into your hand at "
        "a time. \nYour other hand is holding your lantern\n")
    print("'quit' to quit\n")


def look(
    room, room_dict, room_items, score_dict, state_dict, description_dict
):

    score_key = room
    print(description_dict[room])
    if len(room_dict[room]['features']) > 0:
        for feature in room_dict[room]['features']:
            print("There is a " + feature + " here.\n")
    if len(room_items) > 0:
        print("The following items are here: " + ", ".join(room_items) + "\n")
        if score_key in score_dict:
            score(score_key, score_dict, state_dict)


def intro():
    print("\nWelcome brave adventurer!\n")
    print(
        "You are Burt-the-Boneheaded, the only adventurer brave - or "
        "foolish - enough to enter the Dark Castle in search of treasure\n")


def str_to_lst(user_input):
    lst = []
    lst.append(user_input)
    return(lst[0].split())


def description_update(description_key, update_key, description_dict):
    description_dict[description_key] = description_dict[update_key]
    return


def end(state_dict, titles_dict):
    if state_dict['game_ending'] == 'death':
        print("You have died.\n")
    elif state_dict['game_ending'] == 'quit':
        print("You have quit.\n")
    elif state_dict['game_ending'] == 'won':
        print("You have won!\n")
    print(
        "Your adventure ended after " + str(state_dict['move_counter'])
        + " moves.\n")
    print(
        "Your score is " + str(state_dict['current_score']) + " out of "
        + str(state_dict['max_score']) + "\n")
    
    score = state_dict['current_score']
    if score < 0:
        title_score = -10
    elif score == 0:
        title_score = 0
    else:
        title_score = math.ceil(score / 10) * 10

    print("Your title is: " + titles_dict[title_score] + "\n")
    return


def credits():
    print(
        "Written and programmed by Tom. Thanks to Toby, Joshua, JoyEllen, "
        "Milo, Gideon, and Franco for advice and playtesting!!")
    return


def room_action(
        action, word1, room, state_dict, path_dict, room_dict,
        score_key, score_dict, description_dict):

    if action == "death":
        state_dict['game_ending'] = 'death'
        end(state_dict, titles_dict)
        exit()

    elif action == "door":
        door_name = path_dict[room + "-" + word1]['door']
        next_room = path_dict[room + "-" + word1]['next_room']
        if door_dict[door_name]['door_state'] == 'open':
            room = next_room
            look(
                room, room_dict, room_dict[room]['items'], score_dict,
                state_dict, description_dict)
            state_dict['room'] = next_room
        else:
            print("The " + door_name + " is closed.\n")

    elif action == "passage":
        door_name = path_dict[room + "-" + word1]['door']
        next_room = path_dict[room + "-" + word1]['next_room']
        room = next_room
        look(
            room, room_dict, room_dict[room]['items'], score_dict,
            state_dict, description_dict)
        state_dict['room'] = next_room

    return


# *** Score is called from look(), 'take', 'attack', and a few other spots ***
def score(score_key, score_dict, state_dict):
    if score_dict[score_key][0] == 0:
        state_dict['current_score'] += score_dict[score_key][1]
        print("Your score is now " + str(state_dict['current_score'])
            + " out of " + str(state_dict['max_score']) + "\n")
    score_dict[score_key][0] += 1
    return

# ********************
# --- Text Interpreter
# ********************


def interpreter_text(
        user_input, description_dict, path_dict, room_dict,
        door_dict, unknown_word_lst, state_dict, allowed_lang_dict,
        written_on_dict, creature_dict, food_dict, score_dict,
        pre_action_trigger_lst, post_action_trigger_lst, timer_dict,
        switch_dict):

    # *** local variables ***
    allowed_verbs = allowed_lang_dict['allowed_verbs']
    allowed_movement = allowed_lang_dict['allowed_movement']
    room = state_dict['room']
    room_items = room_dict[room]['items']
    room_features = room_dict[room]['features']
    hand = state_dict['hand']
    backpack = state_dict['backpack']
    worn = state_dict['worn']

# *** Convert User Input to single word strings ***

    user_input_lst = str_to_lst(user_input)

    word1 = user_input_lst[0]
    if len(user_input_lst) > 1:
        word2 = user_input_lst[1]
    else:
        word2 = "blank"

    if (word1 in allowed_verbs) and (len(user_input_lst) == 1):
        print(word1 + " what Burt?")
        return

    score_key = word1 + "-" + word2
    trigger_key = score_key
    switch_key = score_key

    if trigger_key in pre_action_trigger_lst:
        if trigger(
                room, trigger_key, room_dict, word2, timer_dict,
                description_dict, state_dict, titles_dict, door_dict,
                score_dict, creature_dict):
            return


# --- Handle One Word Commands

    if word1 == "help":
        help()
        
    elif word1 == "look":
        look(
            room, room_dict, room_items, score_dict, state_dict,
            description_dict)

    elif word1 == "score":
        print("Your score is now " + str(state_dict['current_score'])
            + " out of " + str(state_dict['max_score']) + "\n")

    elif word1 == "inventory":
        print("In your hand you have: " + hand[0] + "\n")
        backpack_inv = ', '.join(backpack)
        print("In your backpack you have: " + backpack_inv + "\n")
        worn_inv = ', '.join(worn)
        print("You are wearing: " + worn_inv + "\n")
        
    elif word1 in allowed_movement:
        print(description_dict[room + "-" + word1])
        action = path_dict[room + "-" + word1]['action']
        room_action(
            action, word1, room, state_dict, path_dict, room_dict,
            score_key, score_dict, description_dict)

# *** Handle Two Word Commands ***

# --- Examine verb

    elif word1 == "examine":

        visible_items = (hand + backpack + room_items + room_features
            + room_dict[room]['view_only'] + worn)
        visible_items.append(room)
        visible_items.append("fist")
        visible_items.append("burt")

        if word2 in visible_items:
            print(description_dict[word2])
            if word2 in allowed_lang_dict['is_container']:
                if door_dict[word2]['door_state'] == 'open':
                    contain_inv = ', '.join(door_dict[word2]['contains'])
                    print("The " + word2 + " contains a "
                        + contain_inv + ".\n")

            if trigger_key in post_action_trigger_lst:
                trigger(
                    room, trigger_key, room_dict, word2, timer_dict,
                    description_dict, state_dict, titles_dict, door_dict,
                    score_dict, creature_dict)

            if score_key in score_dict:
                score(score_key, score_dict, state_dict)

        else:
            print("Burt you can't " + word1 + " that!\n")

# --- Take verb

    elif word1 == "take":

        takeable_items = backpack + room_items + worn

        # *** if item is takable && not "nothing" (inventory placeholder) ***
        if word2 in takeable_items and word2 != "nothing":

            # *** swap variable ***
            temp_swap = hand[0]
            del hand[0]

            # *** add the taken item to player's hand' ***
            hand.append(word2)
            state_dict['hand'] = hand

            # *** put contents of hand in backpack unless hand == "nothing" ***
            if temp_swap != "nothing":
                backpack.append(temp_swap)

            # *** remove taken item from its source list (backpack or room) ***
            if word2 in backpack:
                backpack.remove(word2)
            elif word2 in worn:
                worn.remove(word2)
            else:
                room_items.remove(word2)
                room_dict[room]['room_items'] = room_items

                # *** Deal with Container Cases ***
                if word2 in state_dict['item_containers']:
                    container = state_dict['item_containers'][word2]
                    door_dict[container]['contains'].remove(word2)
                    if len(door_dict[container]['contains']) == 0:
                        door_dict[container]['contains'].append('nothing')
                    del state_dict['item_containers'][word2]

            # *** confirm to the player that the item has been taken ***
            print("Taken\n")

# *** Clean up source containers ***

            # *** if the backpack is now empty add placeholder "nothing" ***
            if len(backpack) == 0:
                backpack.append("nothing")

            # *** ensure we don't get multiple "nothing" in backpack ***
            if len(backpack) > 1 and "nothing" in backpack:
                backpack.remove("nothing")

            # *** if worn is now empty add the placeholder "nothing" to it ***
            if len(worn) == 0:
                worn.append("nothing")
                print(description_dict[score_key + '-worn']) # worn removal txt

            # *** ensure we don't get multiple "nothing" in backpack ***
            if len(worn) > 1 and "nothing" in backpack:
                worn.remove("nothing")
            
            state_dict['backpack'] = backpack
            state_dict['worn'] = worn
            
            if score_key in score_dict:
                score(score_key, score_dict, state_dict)

        else:
            print("Burt you can't " + word1 + " that!\n")

# --- Drop verb

    elif word1 == "drop":

        droppable_items = hand
        
        if word2 in droppable_items and word2 != "nothing":
            temp_swap = hand[0]
            del hand[0]
            hand.append("nothing")
            state_dict['hand'] = hand
            room_items.append(temp_swap)
            room_dict[room]['room_items'] = room_items
            print("Dropped\n")
            
            if trigger_key in post_action_trigger_lst:
                trigger(
                    room, trigger_key, room_dict, word2, timer_dict,
                    description_dict, state_dict, titles_dict, door_dict,
                    score_dict, creature_dict)
                           
        else:
            print("Burt you can't " + word1 + " that!\n")

# --- Open verb

    elif word1 == "open":
    
        if word2 in allowed_lang_dict['can_be_opened']:
            if word2 not in room_dict[room]['features']:
                print("Burt, you can't see a " + word2 + " here!\n")
            elif door_dict[word2]['door_state'] == 'open':
                print("Burt, the " + word2 + " is already open!\n")
            elif door_dict[word2]['lock_state'] == 'locked':
                print("The " + word2 + " is locked.\n")
            else:
                print("Opened\n")
                door_dict[word2]['door_state'] = 'open'
                description_dict[word2] = description_dict[word2 + '-base'] \
                    + door_dict[word2]['door_state'] + ".\n"
                if door_dict[word2]['is_container']:
                    contain_inv = ', '.join(door_dict[word2]['contains'])
                    print("The " + word2 + " contains a "
                        + contain_inv + ".\n")
                    room_dict[room]['items'].extend(
                        door_dict[word2]['contains'])
        else:
            print("Burt you can't " + word1 + " that!\n")

# --- Unlock verb

    elif word1 == "unlock":
    
        if word2 in allowed_lang_dict['can_be_opened']:
            if word2 not in room_dict[room]['features']:
                print("Burt, you can't see a " + word2 + " here!\n")
            elif door_dict[word2]['door_state'] == 'open':
                print("Burt, the " + word2 + " is already open!\n")
            elif door_dict[word2]['lock_state'] == 'unlocked':
                print("The " + word2 + " is already unlocked.\n")
            else:
                if hand[0] == door_dict[word2]['key']:
                    print("Unlocked\n")
                    door_dict[word2]['lock_state'] = 'unlocked'
                else:
                    print("Burt, you don't have the key in your hand!\n")
        else:
            print("Burt you can't " + word1 + " that!")

# --- read verb

    elif word1 == "read":
    
        visible_items = (hand + backpack + room_items + room_features
            + room_dict[room]['view_only'])
        visible_items.append(room)
        visible_items.append("fist")
        visible_items.append("burt")

        if word2 in allowed_lang_dict['can_be_read']:
            if written_on_dict[word2] in visible_items:
                print(description_dict[word2 + "-read"])
                if trigger_key in post_action_trigger_lst:
                    trigger(
                        room, trigger_key, room_dict, word2, timer_dict,
                        description_dict, state_dict, titles_dict, door_dict,
                        score_dict, creature_dict)
            else:
                print("Burt, you can't read what you can't see!\n")

        else:
            print("Burt you can't " + word1 + " that!\n")

# --- attack verb

    elif word1 == "attack":
    
        if word2 in allowed_lang_dict['can_be_attacked'] \
                and word2 in room_dict[room]['features']:

            if hand[0] not in allowed_lang_dict['weapons']:
                weapon = 'fist'
            else:
                weapon = hand[0]

            attack_weapon = word1 + "-" + weapon
            attack_result = attack_weapon + "-" + 'result'
            attack_description = word2 + "-" + attack_weapon
            print(description_dict[attack_description])

            if creature_dict[word2][attack_result] == 'creature_death':
                room_dict[room]['features'].remove(word2)
                room_dict[room]['features'].append('dead_' + word2)
                print("the " + word2 + " has died.\n")
                if score_key in score_dict:
                    score(score_key, score_dict, state_dict)
                room_dict[room]['items'].extend(creature_dict[word2]['drops'])

            elif creature_dict[word2][attack_result] == 'creature_runs':
                room_dict[room]['features'].remove(word2)
                print("the " + word2 + " has run away.\n")
                if score_key in score_dict:
                    score(score_key, score_dict, state_dict)

            elif creature_dict[word2][attack_result] == 'player_death':
                state_dict['game_ending'] = 'death'
                end(state_dict, titles_dict)
                exit()

            if trigger_key in post_action_trigger_lst:
                trigger(
                    room, trigger_key, room_dict, word2, timer_dict,
                    description_dict, state_dict, titles_dict, door_dict,
                    score_dict, creature_dict)

        else:
            print("Burt you can't " + word1 + " that!\n")

# --- eat verb

    elif word1 == "eat":
        if word2 in allowed_lang_dict['can_be_eaten_lst'] and word2 in hand:
            print(description_dict[word2 + "-eat"])
        else:
            print("Burt you can't " + word1 + " that!\n")

# --- Pull verb

    elif word1 == 'pull':

        if word2 in allowed_lang_dict['can_be_pulled_lst'] \
                and (word2 in room_dict[room]['view_only']
                or word2 in room_dict[room]['features']):
            print("Pulled.\n")

            if word2 in switch_dict:
                if switch_dict[word2]['state'] == 'down':
                    switch_dict[word2]['state'] = 'up'
                    description_dict[word2] = "The " + word2 + " is " \
                        + switch_dict[word2]['state'] + ".\n"
                elif switch_dict[word2]['state'] == 'up':
                    switch_dict[word2]['state'] = 'down'
                    description_dict[word2] = "The " + word2 + " is " \
                        + switch_dict[word2]['state'] + ".\n"

            if trigger_key in post_action_trigger_lst:
                trigger(
                    room, trigger_key, room_dict, word2, timer_dict,
                    description_dict, state_dict, titles_dict, door_dict,
                    score_dict, creature_dict)

        else:
            print("Burt you can't " + word1 + " that!\n")

# --- Push verb

    elif word1 == 'push':

        if word2 in allowed_lang_dict['can_be_pushed_lst'] \
                and (word2 in room_dict[room]['view_only']
                or word2 in room_dict[room]['features']):
            print("Pushed.\n")

            if word2 in switch_dict:
                switch_dict[word2]['press_count'] += 1

                if switch_dict[word2]['success_value'] \
                        == switch_value(switch_key, switch_dict):
                        trigger_key = trigger_key + '-success'
                else:
                    print(description_dict[word1 + "-" + word2 + '-fail'])

            trigger(
                room, trigger_key, room_dict, word2, timer_dict,
                description_dict, state_dict, titles_dict, door_dict,
                score_dict, creature_dict)
            if score_key in score_dict:
                score(score_key, score_dict, state_dict)

        else:
            print("Burt you can't " + word1 + " that!\n")

# --- Wear verb

    elif word1 == "wear":

        if word2 != "nothing" and word2 in allowed_lang_dict['can_be_worn']:

            if word2 not in hand:
                print("Burt, you're not holding the " + word2 + "!\n")
                return

# *** wear the taken item ***
            worn.append(word2)
            state_dict['worn'] = worn

# *** remove the taken item from its source list (hand) ***
            if word2 in hand:
                hand.remove(word2)

# *** if the hand is now empty add the placeholder "nothing" to it ***
            if len(hand) == 0:
                hand.append("nothing")

# *** remove 'nothing' once something is worn ***
            if len(worn) > 1 and "nothing" in worn:
                worn.remove("nothing")
                state_dict['worn'] = worn

# *** confirm to the player that the item has been worn ***
            print("Worn\n")

# *** print worn update text ***
            print(description_dict[score_key])

# *** update global 'hand' and score ***
            state_dict['hand'] = hand
            if score_key in score_dict:
                score(score_key, score_dict, state_dict)

        else:
            print("Burt you can't " + word1 + " that!\n")

    else:
        unknown_word()

# ************************
# --- Dictionaries & Lists
# ************************

# --- Door Dictionary [Variable]
door_dict = {
    'front_gate': {
        'door_state': 'closed',
        'lock_state': 'locked',
        'key': 'rusty_key',
        'is_container': False
    },
    'iron_portcullis': {
        'door_state': 'closed',
        'lock_state': 'locked',
        'key': 'none',
        'is_container': False
    },
    'crystal_box': {
        'door_state': 'closed',
        'lock_state': 'locked',
        'key': 'silver_key',
        'is_container': True,
        'contains': ['scroll_of_the_king']
    }
}

# --- Switch Dictionary [Variable]
switch_dict = {

    # *** Control Panel ***

    'left_lever': {
        'state': 'down'
    },
    'middle_lever': {
        'state': 'down'
    },
    'right_lever': {
        'state': 'down'
    },
    'big_red_button': {
        'success_value': 0,
        'current_value': 0,
        'press_count': 0,
    }
}

# --- Description Dictionary [Programmatically Updated]
description_dict = {

    # --- Doors ---

    'front_gate': "The front_gate is just north of the Dark Castle's "
                  "drawbridge. It is 10 feet tall and reenforced with steel "
                  "bands. Imposing indeed! There is rusty_lettering across "
                  "the top of the gate and a rusty keyhole next to a handle. "
                  "The front_gate is closed.\n",
    
    'iron_portcullis': "Beyond the iron_portcullis you can dimly make out the "
                       "next room. The iron_portcullis is closed.\n",

    # --- Non-Door Features ---

    'control_panel': "The control_panel contains three levers: a left_lever, a"
                     " middle_lever, and a right_lever. The control_panel "
                     "also contains a big_red_button. There are no directions "
                     "posted as to what the controls are for or how to use "
                     "them (a clear ISO lapse is ever you've seen one "
                     "Burt).\n",
    
    'left_lever': "The left_lever is "
                  + switch_dict['left_lever']['state'] + ".\n",
    
    'middle_lever': "The middle_lever is "
                    + switch_dict['middle_lever']['state'] + ".\n",
    
    'right_lever': "The right_lever is "
                   + switch_dict['right_lever']['state'] + ".\n",
    
    'big_red_button': "The big_red_button is to the right of the three "
                      "levers. You have no idea what it does but you have an "
                      "almost irrestiable urge to push it.\n",
    
    'throne': "High-backed and intricately carved, the throne is secured to "
              "the floor and wedged against the castle wall behind it. It "
              "does not look entirely comfortable but it must have once been "
              "very grand indeed. Alas, like the rest of Dark Castle, it is "
              "now dingy and ominous with only faint hints of its past glory. "
              "It must have heard many secrets in its time... perhaps it "
              "still holds some?\n",
    
    'stone_coffer': "This is the sort of coffer that, in better days, was no "
                    "doubt filled to the brim will brightly shining gold "
                    "pieces. Unfortunately, as you'd begun to fear, those "
                    "days are long past and now the coffer is filled only "
                    "with a deep layer of dust.\n",
    
    'crystal_box': "Atop an ornate pillar to the left of the throne sits an "
                   "intricate crystal_box. Through the glass you can make out "
                   "and aged but intact scroll that fits perfectly within the "
                   "container. There is a silver keyhole on the front of the "
                   "crystal_box that glitters brilliantly - much like the "
                   "shiny_sword in fact - in the otherwise dark and brooding "
                   "room. The top of the crystal_box is engraved with "
                   "calligraphy. The crystal_box is closed.\n",

    # --- Items ---

    "rusty_key": "An old Rusty Key... the one they gave you at the pub when "
                 "you swore to pillage the Dark Castle. What could you "
                 "possibly do with it?\n",
    
    "stale_biscuits": "The stale_biscuits are rather unappetizing. There is a "
                      "trademark baked into the biscuits.\n",
        
    'shiny_sword': "The sword glitters even in the dim light. Despite its "
                   "age, the edge is keen and looks ready for action. There "
                   "are dwarven_runes engraved upon the blade.\n",

    'grimy_axe': "A nasty looking weapon - and poorly maintained too. If you "
                 "ever get out of this castle you should set aside some time "
                 "to polish it.\n",
    
    'torn_note': "This must have dropped from the goblin's hand when you "
                 "slew it. The note is ragged and torn. On it there is some "
                 "messy_handwriting.\n",
    
    'silver_key': "The small silver_key glitters in the dim light. It "
                  "certainly stands out in the otherwise dreary Dark Castle. "
                  "If you find a glittering silver keyhole somewhere this is "
                  "definitely the key for it!\n",
    
    'scroll_of_the_king': "Wow this thing is fancy! Huge letters with little "
                          "pictures inside them and all sorts of curvy "
                          "flourish at the end of each and every letter. "
                          "Burt, your humble biscuit-baking, pub-crawling "
                          "brain doesn't even know what to call this thing "
                          "but if it did you would call it an illuminated "
                          "manuscript composed (of course) of "
                          "illuminated_letters. Thanks to the hard and "
                          "thankless work of your first grade teacher, Ms. "
                          "Lusk, you could probably just manage to read the "
                          "illuminated_letters.\n",

    'royal_crown': "Giant rubies: check. Dozens of glittering jewels: check. "
                   "Gleaming gold and precious metals: check. Yep, this is a "
                   "*seriously royal* crown you've got here Burt!\n",

    'hedgehog_broach': "The silver hedgehog_broach is about an inch in "
            "diameter and is carved with the crest of a hedgehog bearing a "
            "sword and a key. It's strangely familiar... you've seen one "
            "just like it... long ago... examining the hedgehog_broach up "
            "close triggers a long forgotten memory... \n\n"

            "you were only five or six years old... you and all your family "
            "were at the bedside of your great grandmother, Nana Baker. She "
            "was old - very, very old -  so old no even was sure how old - "
            "not even Nana. She'd been unable to eat or get out of bed for "
            "the past week and the village healer had given his solemn "
            "verdict that at long last her time had come. The whole village "
            "had come round to pay their last respects but now it was just "
            "family left. She looked very tired and her eyes were closed. \n\n"
            
            "'Thomas', said Nana, meaning your father, "
            "'I'm weary... be a good lad and go "
            "heat me some tea.. Nice and hot please.'. Next she sent your "
            "mother off for a special pillow she'd loaned to a friend. Soon "
            "every member of the family was off on an errand and it was just "
            "you and Nana. \n\n"
            
            "Quite suddenly, Nana's eyes opened, bright blue "
            "and wide awake. 'Well, Burty, finally we can have a little chat. "
            "I wish you were a bit older but now will have to do. Tell me "
            "Burty, how do ya feel about baking biscuits?' \n\n"
            
            "'It's na so bad' you'd stammered back. \n\n"
            
            "Nana laughed and gave you a warm smile. "
            "Don't feel bad Burty, I wasn't much of a Baker myself - had a "
            "bit of a wild romantic streak in me - just like you. You remind "
            "me so much of my Willy.. and that's not entirely an accident "
            "mind you. Thought I might see a resemblance in your grandfather "
            "or father but they were mindful lads and happy enough to be "
            "Bakers. I guess it's waited for you to show itself. Probably "
            "just as well. \n\n"
            
            "Ah Willy... now don't get me wrong, Papa Baker "
            "was a good man - hard working and with a kind heart - took me "
            "hand when many others wouldn't have and always treated me good. "
            "But you're from different stock Burty, very different. And that "
            "comes with some responsibilities.. you've got a destiny 'afore "
            "you and that can be hard on young man with no expecting of it. "
            "That's why I'm telling you this now. \n\n"
            
            "Your real great grandpa was Willy... William Herbert... "
            "last of the line of Flatheads.. "
            "or so everyone's been told. He was a handsome man.. like you "
            "Burty.. and unlike the rest of his family - full of romance and "
            "laughter and travel and adventure. Could be a bit reckless at "
            "times but he had a good heart. He proposed to me right proper "
            "he did... didn't really have to... he was so high up in "
            "society... and so much older too... but the moment I told him he "
            "dropped right to one knee and popped the question. Didn't care "
            "the least what people said. Swore’d we'd elope if the high "
            "priest wouldn't marry us... and he would have too! \n\n"
            
            "Alas, that crazy "
            "man... four months before the big day he was wandering about the "
            "castle entrance, wearing his bathrobe and crown, smoking his "
            "pipe and reading a book as he walked.. as usual.. and boom, he "
            "trips on the drawbridge and falls right into the moat... eaten "
            "right up in one bite by one of those mean old crocodiles that "
            "have swum in it forever. Oh the day I heard the news...' And "
            "with these words she touched the hedgehog_broach she always wore "
            "over her heart. It was a dark day Burty, a dark day for me an' "
            "for the castle and all the lands around. \n\n"
            
            "Someday Burty William Baker, "
            "someday you'll be King. And when you is, you be a "
            "good King... a kind and courageous and bold king.. and when you "
            "is King don't ya going walking off the edge of the drawbridge "
            "with no weapon in your hands and breaking young girl's hearts.. "
            "you hear me? \n\n"
            
            "Stunned by this strange tale... you began to "
            "stammer an answer but just then your Father returned with the "
            "hot tea. With a wink just for you, Nana's eyes closed again and "
            "she sank back into the bed. Minutes later she was gone. \n\n"
            
            "For years and years you wondered what she was talking about.. "
            "and eventually you began to doubt the conversation had ever even "
            "happened... over time it had faded completely... but here in "
            "Dark Castle, with the hedgehog_broach before you, the memory "
            "is clear and real.. Nana was buried with her beloved broach.. "
            "she had insisted on it... this must have been a matching mate.. "
            "presumably worn by Willy himself.\n",

    # --- Special ---

    "fist": "Yep, that's your fist. Still bruised from the last time you "
            "swung and missed and hit a wall...\n",
    
    "burt": "That's you. A fine specimen of a man. If not for the drooling "
            "and the farting I don't know how you'd fend off the ladies\n",
    
    "nothing": "Burt, nothing is nothing. Nada. Zilch. Empty. Like that "
               "noggin of yours..\n",

    'tapestries': "The main_hall tapestries are vast and elaborate, covering "
                  "both the east and the west walls. They appear to depict an "
                  "unkempt figure breaking into a solitary white house and "
                  "from there pillaging a Great Underground Empire. "
                  "Strangely, there is a looming figure near the top of the "
                  "west tapestry who appears to be tapping with his fingers "
                  "on a many-buttoned plank and staring intently into a "
                  "window filled with text. For some reason the figure "
                  "disconcerts you.. his presence in the tapestry fills you "
                  "with existential dread and forces you to question your "
                  "agency and the very nature of your being... BURT!! Get "
                  "hold of yourself man! You're a mangey, pub-crawling "
                  "adventure who lives in his mom's basement. You don't even "
                  "know what half those words mean. Stop staring at "
                  "tapestries and get out there and find the treasure you "
                  "fool!!\n",
    
    'alcove': "A small indentation in the west wall near the portcullis. "
              "It is just deep enough to hold one control_panel and one "
              "goblin.\n",
    
    'family_tree': "It appears to show the family tree of the Flathead "
                   "dynasty. Though generally agreed to have peaked "
                   "(nadired?) during the reign of Dimwit Flathead and "
                   "petered out shortly there-after during the inglorious "
                   "rulership of Wurb Flathead, this family_tree tells a "
                   "different story. It claims that a remote uncle of Wurb "
                   "continued the line for seven more generations and "
                   "eventually ended with William 'The Wanderer' Flathead "
                   "only a little over 100 years ago. The area below William "
                   "is indistinct and feels incomplete.. as if there are "
                   "details still waiting to be filled in.\n\n"

                   "At the very top of the family_tree you see a royal "
                   "crest. Oddly enough, it appears to be a hedgehog bearing "
                   "a sword and a key\n",

    # --- Creatures ---

    'hedgehog': "This poor little hedgehog has seen better days. It looks "
                "gaunt and like it skipped breakfast - and maybe lunch and "
                "dinner too. But despite looking in need of a good meal the "
                "hedgehog's eyes have a bright, territorial gleam in them "
                "and it appears to have quite a preference for shiny things. "
                "You don't know why but you feel an innate fondness for this "
                "small but valiant creature.\n",
    
    'dead_hedgehog': "Tragically, some mean and nasty adventurer has slain "
                     "this innocent woodland creature. In death it looks "
                     "piteous and in need of a hug.\n",
    
    'goblin': "The goblin stands in the alcove guarding the control_panel "
              "and is armed and dangerous. It wields a grimy_axe and looks at "
              "you with watchful malice. This goblin clearly takes its guard "
              "duties very seriously. It would not be wise to approach the "
              "iron_portcullis or the control_panel (or the goblin) "
              "un-armed.\n",

    'dead_goblin': "Even in death the goblin looks fierce and resolute. "
                   "Whoever dispatched this enemy must be an adventurer of "
                   "some renown!\n",

    # --- Rooms ---

    'entrance': "\n*** Entrance ***\n\nYou are standing atop a drawbridge at "
                "the entrance to the Dark Castle. To the north is the "
                "front_gate. To the south the way back home. \nTo the east "
                "and west and below you are the moat.\n",

    'main_hall': "\n*** Main Hall ***\n\nYou are standing in what was once "
                 "the sumptuous main hall of the castle. Faded tapestries "
                 "hang on the east and west walls. The front_gate is to the "
                 "south. And a foreboding archway leads to the north.\n",

    'antechamber': "\n*** Antechamber ***\n\nYou are standing in a what feels "
                   "more like a wide, tall-ceilinged corridor than a room. "
                   "Apparently this is the room-before-the-room, the pre-room "
                   "before the really, really grand room that comes after it. "
                   "If so, the next room must be quite something because back "
                   "in it's day this spot was clearly impressive. Alas, like "
                   "all of the castle it has fallen on dark times and now "
                   "feels more sinister than grand. The east and west walls "
                   "are bare stone. To the south is an open passageway "
                   "leading to the main_hall and to the north there is an "
                   "iron portcullis that guards the path to the grand chamber "
                   "beyond. Near the portcullis on the west wall there is a "
                   "small alcove. It appears to have a control_panel with "
                   "some levers and a big red button on it but you can't see "
                   "it very well due to the dim light. The whole north end of "
                   "the room is cloaked in shadows that make you uneasy.\n",

    'throne_room': "\n*** Throne Room ***\n\nThe room you're currently in is "
                   "vast - almost cavernous. At the far end sits what must "
                   "have once been a grand and glorious throne. To the right "
                   "of the throne is a giant stone_coffer and to the left an "
                   "elegant pedestal that holds what appears to be a delicate "
                   "crystal_box. On either wall there are tall windows - now "
                   "shattered and ruined but you've heard stories of the "
                   "glowing stained glass that once filled them. And above "
                   "the room's entrance hangs a vast (though quite grimy) "
                   "family_tree.\n",

    # --- Trigger Descriptions ---

    'take-shiny_sword': "The moment you approach the sword the territorial "
                        "hedgehog springs forward, blocks your path, and "
                        "bares it's teeth.\n",

    'east-blank-crown': "With courage and boldness to spare you leap from the "
                        "drawbridge into the murky waters of the moat. A less "
                        "resolute adventurer might have turned tail at the "
                        "sight of the oncoming giant crocodile but not you "
                        "Burt. Treading water with your feet you take a "
                        "two-handed grip on your weapon and get ready to face "
                        "your destiny. Just before reaching you the primitive "
                        "reptile realizes that you are armed and ready to "
                        "fight (crocs are famously near-sighted). In surprise "
                        "and fear it belches up the contents of it's stomach "
                        "- including the royal_crown - and flees in fear. "
                        "With a deft athleticism unlike anything you've ever "
                        "displayed before today you snag the crown with your "
                        "off hand, toss it into your backpack, and in one "
                        "smooth motion adroitly hoist yourself back onto the "
                        "drawbridge one handed. The lads at the pub would "
                        "fall over at the sight this your skill and courage! "
                        "(though mind you, they fall over on a regular basis "
                        "as it is)\n",

    'east-blank-no_crown': "With courage and boldness to spare you leap from "
                           "the drawbridge into the murky waters of the moat. "
                           "Apparently the last time you did this you "
                           "terrified the local wildlife so much they are "
                           "still in hiding. After treading water for a few "
                           "minutes you clamber back onto the drawbridge.\n",

    'drop-shiny_sword': "The hedgehog beams at you with gratitude for "
                        "returning the shiny_sword. From a hidden fold of its "
                        "fur it takes out a silver_key and places it at your "
                        "feet with a bow.\n",

    'push-throne': "You push hard on the throne. Nothing happens but one "
                   "side of the throne feels a bit askew - as if something "
                   "was wedged behind it. Strange...\n",

    'pull-throne': "Hoping hoping to find some sort of secret compartment "
                   "filled with gold - or at least a good souvenir to show to "
                   "the lads back at the pub - you pull and prod the throne. "
                   "As you are pulling the throne forward you hear a "
                   "metallic 'clank' and something rolls out from beneath the "
                   "throne.. it appears to be a hedgehog_broach. It must have "
                   "been wedged between the throne and the castle wall all "
                   "these years... since the days of the last King!\n",

    'read-illuminated_letters-wrong_room': "Upon reading the scroll aloud you "
                                           "hear a distant rumble as if great "
                                           "powers are at work... but then it "
                                           "fades... perhaps you need to "
                                           "read it somewhere else to "
                                           "complete the recipe?\n",

    'read-illuminated_letters-no_hedgehog': "Upon reading the scroll aloud "
                                            "there is a rumble and a bright "
                                            "flash of light in the sky.. but "
                                            "then it dims and the sound "
                                            "fades... Alas, some vital "
                                            "ingredient has gone missing in "
                                            "the castle... this is grim "
                                            "Burt... you may need to start "
                                            "your adventures over from the "
                                            "start and play through with a "
                                            "more benevolent spirit.\n",

    'read-illuminated_letters-no_crown': "Upon reading the scroll aloud "
                                         "the clouds outside part, the "
                                         "sun shines, there is a booming "
                                         "sound... but then it fades "
                                         "away abruptly... there's one "
                                         "missing ingredient that's "
                                         "keeping the scroll_of_the_king from "
                                         "performing its magic... if only "
                                         "there was some token of royal "
                                         "lineage... perhaps some form of "
                                         "headpiece you could wear.. that you "
                                         "would proclaim your birthright...\n",

    'read-illuminated_letters-win': "Upon reading the scroll aloud "
                                    "the clouds outside part, the "
                                    "sun shines, there is a booming sound "
                                    "like a great and thunderous gong that "
                                    "echoes and rebounds across the land! By "
                                    "the scroll's power the castle is "
                                    "scourgafied and all that was once dark "
                                    "is now glimmering with color and ligtht. "
                                    "Where Dark Castle once lurked, now "
                                    "gleams Bright Castle! The coffer "
                                    "magically fills with gold (and also a "
                                    "conveniently provided and legally "
                                    "complete deed to Bright Castle). And "
                                    "suddenly Burt, you find your own "
                                    "somewhat threadbare Baker's clothing "
                                    "replaced by garments of rich velvet and "
                                    "silk. Well done Burt! To the amazement "
                                    "of your family and friends - and the "
                                    "eternal pride of your great grandmother "
                                    "- you are now the King of Bright "
                                    "Castle!!\n",

    'goblin_attacks-parry': "The goblin does not take kindly to your "
                            "presence in the north side of the room. It "
                            "attacks with lightening-fast swing of the "
                            "grimy_axe and you only barely manage to parry "
                            "with your own weapon.\n",

    'goblin_attacks-death': "The goblin does not take kindly "
                            "to your presence in the north side of the room. "
                            "It attacks with lightening-fast swing of the "
                            "grimy_axe and you are helpless against the "
                            "onslaught. You will need a better weapon than "
                            "your fists if you are to survive this foe.\n",

    'push-big_red_button-open': "You hear a loud clank, a whirring "
                                "of gears, and the iron_portcullis suddenly "
                                "opens.\n",

    'push-big_red_button-close': "You hear a loud clank, a whirring "
                                 "of gears, and the iron_portcullis suddenly "
                                 "closes.\n",

    'push-big_red_button-fail': "You press the button and hear a whirring of "
                                "gears but nothing happens.\n",

    # --- Worn Descriptions ---

    'wear-royal_crown': "You now feel more regal.\n",

    'take-royal_crown-worn': "You suddenly feel a bit less kingly.\n",

    # --- Path Descriptions ---

    'entrance-north': "You approach the daunting front gate.\n",

    'entrance-south': "Don't be ridiculous Burt. You just swore to the whole "
                      "pub that you'd march into the Dark Castle and grab "
                      "the gold and buy everyone drinks with it. \nThat is "
                      "why they gave you the rusty_key. You can't turn back "
                      "now!\n",

    'entrance-east': "With confidence and vigor you pitch off the side of "
                     "the drawbridge and into the moat. Who knew it would "
                     "be full of crocodiles?\n",

    'entrance-west': "With confidence and vigor you pitch off the side of "
                     "the drawbridge and into the moat. Who knew it would "
                     "be full of crocodiles?\n",

    'main_hall-north': "You pass through the foreboding archway.\n",

    'main_hall-south': "You exit through the front_gate.\n",

    'main_hall-east': "Ouch! You have walked into a wall.\n",

    'main_hall-west': "Ouch! You have walked into a wall.\n",

    'antechamber-north': "You approach the iron_portcullis.\n",

    'antechamber-south': "You exit through the southern passage.\n",

    'antechamber-east': "Ouch! Burt, stop walking into walls!\n",

    'antechamber-west': "Ouch! Burt, stop walking into walls!\n",

    'throne_room-north': "Ouch! Burt, stop walking into walls!\n",

    'throne_room-south': "You approach the iron_portcullis.\n",

    'throne_room-east': "Ouch! Burt, stop walking into walls!\n",

    'throne_room-west': "Ouch! Burt, stop walking into walls!\n",

    # --- Read Text ---

    'rusty_lettering-read': "'ABANDON HOPE ALL YE WHO EVEN THINK ABOUT IT'\n",

    'trademark-read': "'McVities'\n",

    'dwarven_runes-read': "'Goblin Walloper'\n",

    'messy_handwriting-read': "",  # random number assigned in main routine

    'calligraphy-read': "'The Scroll of the King'\n",

    'illuminated_letters-read': "First with great effort and then, "
                                "surprisingly, with surety and confidence, "
                                "you read out loud the text on the scroll. "
                                "Your voice booms forth of its own accord - "
                                "as if some part of your brain has been "
                                "getting ready to say these words all your "
                                "life. The rest of brain is struggling just "
                                "to make sense of what you're saying with "
                                "such confidence... it seems to be something "
                                "along the lines of a recipe with ingredients"
                                "... so if the 'heir to the true king' "
                                "(whoever that might be)... reads 'this "
                                "precious parchment'(you're pretty sure that "
                                "means the scroll you're holding)... in the "
                                "throne_room (you've been there!)... while "
                                "'adorned with the gleaming headpiece of "
                                "state' (whatever that means)... and also "
                                "requiring that 'so long as the castle "
                                "remains invested with a representative of "
                                "our most noble heraldic charge seen ever "
                                "upon our crest, seal, and glorious coat of "
                                "arms' (even Ms. Lusk would have no clue what "
                                "this means but she would notice that an "
                                "awful lot of the illuminated_letters in this "
                                "sentence include a hedgehog with a sword and "
                                "a key)... and then it finishes on a rather "
                                "dramatic high note with the words 'upon the "
                                "hour these conditions be met, a new King of "
                                "Bright Castle shall shine forth and be "
                                "proclaimed!'\n",

    # --- Attack Results ---

    'hedgehog-attack-fist': "You take a wild swipe at the hedgehog with your "
                            "fist but it nimbly leaps aside. BURT! What has "
                            "gotten into you?? We have an evil castle to "
                            "conquer. Stop trying to slay defenseless "
                            "woodland creatures!\n",

    'hedgehog-attack-shiny_sword': "You strike at the hedgehog with the "
                                    "shiny_sword and it flees, terrified, "
                                    "from your unprovoked attack. You know in "
                                    "your heart that you will come to regret "
                                    "this unkingly deed.\n",

    'hedgehog-attack-grimy_axe': "You strike at the hedgehog with the "
                                 "grimy_axe and it flees, terrified, "
                                 "from your unprovoked attack. You know in "
                                 "your heart that you will come to regret "
                                 "this unkingly deed.\n",

    'goblin-attack-fist': "With an echoing war cry you charge the goblin, "
                          "flailing your fists wildly in all directions as "
                          "you come. This technique has served you well "
                          "during drunken altercations at the pub but it "
                          "proves less effective against a trained goblin "
                          "guard. The last thing you ever see is the goblin's "
                          "grimy_axe swinging towards your head.\n",

    'goblin-attack-shiny_sword': "The shiny_sword surges with power and "
                                 "lethal heft in your hand. A preternatural "
                                 "calm comes over you. You were born for this "
                                 "moment. Your raucous pub crawling days "
                                 "were a mere temporary distraction.. you "
                                 "know in your bones that this primal "
                                 "showdown was meant to be and that, with the "
                                 "shiny_sword at your command, you were meant "
                                 "to win it. Resolute, and with a confidence "
                                 "you have never even imagined having up "
                                 "until this very moment, you stride to meet "
                                 "your foe in battle and dispatch him with "
                                 "one blazing fast strike of your sword.\n",

# --- Stateful Description Updates ---

    'hedgehog_hungry_has_sword': "This poor little hedgehog has seen better "
                                 "days. It looks gaunt and like it skipped "
                                 "breakfast - and maybe lunch and dinner too. "
                                 "But despite looking in need of a good meal "
                                 "the hedgehog's eyes have a bright, "
                                 "territorial gleam in them and it appears to "
                                 "have quite a preference for shiny things. "
                                 "You don't know why but you feel an innate "
                                 "fondness for this small but valiant "
                                 "creature.\n",
    
    'hedgehog_eating': "The hedgehog is eating ravenously.\n",
    
    'hedgehog_fed_sword_not_taken': "The hedgehog is looking svelte and "
                                    "chipper. It has the swagger of a "
                                    "hedgehog that has scored a meal of "
                                    "stale_biscuits and still has it's "
                                    "favorite shiny possession.\n",
    
    'hedgehog_fed_sword_taken': "The hedgehog is looking svelte and chipper "
                                "but not entirely content. It's clearly "
                                "grateful for its recent meal but keeps "
                                "looking at you hopefully.",
    
    'hedgehog_fed_sword_returned': "This hedgehog is on top of the world! It "
                                   "has recently devoured a meal of "
                                   "stale_biscuits (a rare delicacy among "
                                   "hedgehogs) and now has it's favorite "
                                   "shiny object back. It looks upon you with "
                                   "gratitude and devotion. It sees within "
                                   "you a nobility, compassion, and destiny "
                                   "beyond anything you've hitherto imagined "
                                   "possessing.\n",

    'front_gate-base': "The front_gate is just north of the Dark Castle's "
                       "drawbridge. It is 10 feet tall and reenforced with "
                       "steel bands. Imposing indeed! There is "
                       "rusty_lettering across the top of the gate and a "
                       "rusty keyhole next to a handle. The front_gate is ",
    
    'iron_portcullis-base': "Beyond the iron_portcullis you can dimly make "
                            "out the next room. The iron_portcullis is ",
    
    'crystal_box-base': "Atop an ornate pillar to the left of the throne sits "
                        "an intricate crystal_box. Through the glass you can "
                        "make out and aged but intact scroll that fits "
                        "perfectly within the container. There is a silver "
                        "keyhole on the front of the crystal_box that "
                        "glitters brilliantly - much like the shiny_sword in "
                        "fact - in the otherwise dark and brooding room. The "
                        "top of the crystal_box is engraved with calligraphy. "
                        "The crystal_box is ",

# --- Eat Results ---

    'stale_biscuits-eat': "You'd really rather not. You've been rooming in "
                          "your Mom's basement and living off the "
                          "stale_biscuits in her pantry ever since you "
                          "finished school - mostly so that you could spend "
                          "whatever money you had at the pub. You don't mind "
                          "sleeping in the basement but the stale_biscuits "
                          "are really getting to you.. you'll need to be a "
                          "lot hungrier than you are now before you'll be "
                          "able to keep another of those down!\n"

}

# --- Path Description Dictionary [STATIC]
path_dict = {
    'entrance-north': {
        'action': 'door',
        'door': 'front_gate',
        'next_room': 'main_hall'
    },
    'entrance-south': {
        'action': 'none',
        'door': 'none',
        'next_room': 'none'
    },
    'entrance-east': {
        'action': 'death',
        'door': 'none',
        'next_room': 'none'
    },
    'entrance-west': {
        'action': 'death',
        'door': 'none',
        'next_room': 'none'
    },
    'main_hall-north': {
        'action': 'passage',
        'door': 'none',
        'next_room': 'antechamber'
    },
    'main_hall-south': {
        'action': 'door',
        'door': 'front_gate',
        'next_room': 'entrance'
    },
    'main_hall-east': {
        'action': 'none',
        'door': 'none',
        'next_room': 'none'
    },
    'main_hall-west': {
        'action': 'none',
        'door': 'none',
        'next_room': 'none'
    },
    'antechamber-north': {
        'action': 'door',
        'door': 'iron_portcullis',
        'next_room': 'throne_room'
    },
    'antechamber-south': {
        'action': 'passage',
        'door': 'none',
        'next_room': 'main_hall'
    },
    'antechamber-east': {
        'action': 'none',
        'door': 'none',
        'next_room': 'none'
    },
    'antechamber-west': {
        'action': 'none',
        'door': 'none',
        'next_room': 'none'
    },
    'throne_room-north': {
        'action': 'none',
        'door': 'none',
        'next_room': 'none'
    },
    'throne_room-south': {
        'action': 'door',
        'door': 'iron_portcullis',
        'next_room': 'antechamber'
    },
    'throne_room-east': {
        'action': 'none',
        'door': 'none',
        'next_room': 'none'
    },
    'throne_room-west': {
        'action': 'none',
        'door': 'none',
        'next_room': 'none'
    }
}

# --- Room Dictionary [VARIABLE]
room_dict = {
    'entrance': {
        'features': ["front_gate"],
        'items': [],
        'view_only': [],
    },
    'main_hall': {
        'features': ['hedgehog', 'front_gate'],
        'items': ['shiny_sword'],
        'view_only': ['tapestries']
    },
    'antechamber': {
        'features': ['iron_portcullis', 'goblin', 'control_panel'],
        'items': [],
        'view_only': ['alcove', 'grimy_axe']
    },
    'throne_room': {
        'features': ['iron_portcullis', 'throne', 'crystal_box'],
        'items': [],
        'view_only': ['family_tree', 'stone_coffer']
    }
}

# --- Creature Dictionary [VARIABLE]
creature_dict = {
    'hedgehog': {
        'drops': [],
        'state': 'hungry_has_sword',
        'attack-fist-result': 'none',
        'attack-shiny_sword-result': 'creature_runs',
        'attack-grimy_axe-result': 'creature_runs'
    },
    'goblin': {
        'drops': ['grimy_axe', 'torn_note'],
        'state': 'guarding',
        'attack-fist-result': 'player_death',
        'attack-shiny_sword-result': 'creature_death'
    }
}

# --- List of Pre-Action Triggers [STATIC]
pre_action_trigger_lst = [
    'take-shiny_sword',
    'examine-control_panel',
    'open-iron_portcullis',
    'examine-iron_portcullis',
    'examine-grimy_axe',
    'north-blank',
    'east-blank',
    'west-blank'
]

# --- List of Post-Action Triggers [STATIC]
post_action_trigger_lst = [
    'drop-stale_biscuits',
    'attack-goblin',
    'drop-shiny_sword',
    'pull-throne',
    'push-throne',
    'read-illuminated_letters'
]

# --- Written On Dictionary [STATIC]
written_on_dict = {
    'rusty_lettering': 'front_gate',
    'trademark': "stale_biscuits",
    'dwarven_runes': 'shiny_sword',
    'messy_handwriting': 'torn_note',
    'calligraphy': 'crystal_box',
    'illuminated_letters': 'scroll_of_the_king'
}

# --- Food Results Dictionary [STATIC]
food_dict = {
    'stale_biscuits': 'none'
}

# --- Unknown Word List [STATIC]
unknown_word_lst = [
    "Burt, I have no idea what you're talking about!\n",
    "Burt, are you babbling again?\n",
    "Burt, I'm just going to pretend I didn't hear that\n",
    "Burt, you've said some strange things over the years but "
    "that was a doosey!\n",
    "Burt! What would your mother say if she heard you speaking like that!?\n"
]

# --- Game State Dictionary [VARIABLE]
state_dict = {
    'room': 'entrance',
    'hand': ["nothing"],
    'backpack': ['rusty_key', 'stale_biscuits'],
    'move_counter': 0,
    'current_score': 0,
    'max_score': 75,
    'active_timer': 'none',
    'hedgehog_broach_found': False,
    'game_ending': 'unknown',
    'item_containers': {'scroll_of_the_king': 'crystal_box'},
    'worn': ['nothing']
}

# --- Score Dictionary [VARIABLE]
score_dict = {
    'take-rusty_key': [0, 5],
    'main_hall': [0, 5],
    'take-shiny_sword': [0, 10],
    'attack-hedgehog': [0, -20],
    'attack-goblin': [0, 5],
    'push-big_red_button': [0, 10],
    'take-silver_key': [0, 5],
    'take-scroll_of_the_king': [0, 5],
    'examine-hedgehog_broach': [0, 5],
    'gator-crown': [0, 5],
    'wear-royal_crown': [0, 5],
    'read-illuminated_letters': [0, 15]
}

# --- Timer Dcitionary [STATIC]
timer_dict = {
    'drop-stale_biscuits': {
        'timer': 0,
        'timer_txt_5': "With a yelp of grateful delight the starving hedgehog "
                       "leaps upon the stale_biscuits and begins to devour "
                       "them.\n",
        'timer_txt_4': "The hedgehog is ravenously devouring the "
                       "stale_biscuits and is taking no notice of you at "
                       "all.\n",
        'timer_txt_3': "The hedgehog has eaten through half the "
                       "stale_biscuits but is still giving them all of its "
                       "attention.\n",
        'timer_txt_2': "The hedgehog is nearly done eating all of the "
                       "stale_biscuits and is beginning to look around a "
                       "bit.\n",
        'timer_txt_1': "The hedgehog has finished the stale_biscuits and is "
                       "vigilantly looking around.\n"
    }
}

# --- Titles Dictionary [STATIC]
titles_dict = {
    -10: 'Burt the Best Forgotten',
    0: 'Burt the Boneheaded',
    10: 'Burt the Beginner',
    20: 'Burt the Better Than Average',
    30: 'Burt the Brawny',
    40: 'Burt the Brainy',
    50: 'Burt the Benevolent',
    60: 'Burt the Breathtaking',
    70: 'Burt the Bodacious',
    80: 'Burt the Bold, Baron of Bright Castle'
}

# --- Allowed Language Dictionary [STATIC]
allowed_lang_dict = {
    'allowed_movement': ["north", "south", "east", "west"],
    'allowed_verbs': [
        "examine", "take", "attack", "drop", "open", "unlock",
        'read', 'eat', 'pull', 'push', 'wear'],  # 2-word verbs
    'can_be_opened': ['front_gate', 'iron_portcullis', 'crystal_box'],
    'can_be_read': [
        'rusty_lettering', 'trademark', 'dwarven_runes',
        'messy_handwriting', 'calligraphy', 'illuminated_letters'],
    'can_be_attacked': ['hedgehog', 'goblin'],
    'weapons': ['shiny_sword', 'grimy_axe'],
    'can_be_eaten_lst': ['stale_biscuits'],
    'can_be_pulled_lst': [
        'left_lever', 'middle_lever', 'right_lever', 'throne'],
    'can_be_pushed_lst': ['big_red_button', 'throne'],
    'is_container': ['crystal_box'],
    'can_be_worn': ['royal_crown']   # not broach; causes player confusion
}

# ****************
# --- Main Routine
# ****************

# *** Variable Assignment ***
switch_dict['big_red_button']['success_value'] = random.randint(0, 7)
description_dict['messy_handwriting-read'] = "'..ode is " \
    + str(switch_dict['big_red_button']['success_value']) \
    + ". Don't tell anyo..'\n"

# *** Start of Game Welcome Text ***
intro()
help()
look(
    state_dict['room'], room_dict, room_dict[state_dict['room']]['items'],
    score_dict, state_dict, description_dict)

# *** Get User Input ***
while True:
    user_input = input("> ")
    if user_input == "quit":
        print("Goodbye Burt!\n")
        state_dict['game_ending'] = 'quit'
        end(state_dict, titles_dict)
        break
    else:
        state_dict['move_counter'] += 1
        interpreter_text(
            user_input, description_dict, path_dict, room_dict,
            door_dict, unknown_word_lst, state_dict, allowed_lang_dict,
            written_on_dict, creature_dict, food_dict, score_dict,
            pre_action_trigger_lst, post_action_trigger_lst, timer_dict,
            switch_dict)
        if state_dict['active_timer'] != 'none':
            timer(
                state_dict['room'], room_dict, timer_dict, state_dict,
                description_dict)
