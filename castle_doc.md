+++ Documentation +++

Steps for new room creation
	Outline contents and actions in the room
	Create room_dict entry: description, features, items
	Updated allowed_lang_lst as needed
	Create path_dict entires: north, south, east, west
	Write description_dict entries for items, features, and view_only entities
	Write entries for read_dict
	Create interactions for any doors, creatures, timers, switches, or containers

Steps for new verb creation:
	Add the word to the help() text
	
	Add word to allowed_lang_dict['allowed_verbs'] (e.g. [.., 'eat'])

	If needed, add a verb-specific list to allowed_lang_dict (e.g.: allowed_lang_dict = {'can_be_eaten_lst': ['stale_biscuts']} )

	If the verb impacts new nouns create a new noun dictionary for it (e.g. food_dict['stale_biscuts'] => eat_txt and eat_action )		If you create a new nound dictionary be sure to add it to the passed variables for interpreter_txt()

	Create verb elif in interpreter_text to call dictionary entries and update lists (e.g. inventory) as needed

		It can help to start by copying the elif for an existing verb that has similar usage constraints (e.g. 'drop' for 'eat')

	Test your new verb!


#	Steps for new trigger creation:
#		Determine whether trigger is pre or post action
#		Add trigger text to the correct trigger list (pre_action_trigger_lst and post_action_trigger_lst) (currently skippable for 'push')
#		If trigger is post_action ensure that trigger() is called in the verb elif in text_interpreter() 
#		Add trigger logic to trigger()

# 	Steps for new item creation:
#		Determine where the item will 'live' (which room or container it will be found in)
#		Add the item to room_dict or container_dict
#		Add the item's description to description_dict

#	Version 1.0 Known Limitations
#		Only 2 word sentences... adjectives are connected to nouns using "_"
#		No prepositions
#		Only one timer active at a time
#		If you attack the hedgehog while it's eating the stale_biscuts simply vanish

#	Version 2.0 Goals
#		articles, adjectives, and prepositions
#		Save Game capability
#		Base on examples of efficient code.. focus on pythonic implementation
#		Classes
#		switcher

# +++ Notes +++ 

#	Misc:
#	   Rooms contain items, doors, containers, switches, and creatures
#   	Inventory = backpack + hand + worn
#   	Examine scope = inventory + room_items + room_features + room_name + "burt" + "fist" + view_only + worn

# 	Future Notes Topics:
#		Linguistics (such as they are)
#		Mechanics
#		Program layout
#		Story
#		Puzzles
