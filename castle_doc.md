+++ Documentation +++

Version 1.0 Known Limitations
	- Only 2 word sentences... adjectives are connected to nouns using "_"
	- No prepositions
	- Only one timer active at a time (is this still true??)
	- If you attack the hedgehog while it's eating the stale_biscuts simply vanish

# 	Future Notes Topics:
#		Linguistics (such as they are)
#		Mechanics
#		Program layout and approach [list driven]
#		Story
#		Puzzles

+++ Steps for Story Expansion +++

New room creation
	- Outline contents and actions in the room
	- Create room_dict entry: description, features, items
	- Updated allowed_lang_lst as needed
	- Create path_dict entires for viable paths
	- Write description.txt entries for new items, features, view_only, and read entities
	- Update static_dict written_on_dict if needed
	- Create interactions for any doors, creatures, timers, switches, or containers

New verb creation:
	- Add the word to the help() text
	- Add word to allowed_lang_dict 'allowed_verbs' (e.g. [.., 'eat'])
	- If needed, add a verb-specific list to allowed_lang_dict (e.g.: allowed_lang_dict = {'can_be_eaten_lst': ['stale_biscuts']} )
	- If the verb impacts new nouns in a complex way create a new noun dictionary for it (e.g. static_dict food_dict['stale_biscuts'] => eat_results )
		- If you create an entirely new noun dictionary be sure to add it to the passed variables for interpreter_txt()
		- Create verb elif in interpreter_text to call dictionary entries and update lists (e.g. inventory) as needed
		- It can help to start by copying the elif for an existing verb that has similar usage constraints (e.g. 'drop' for 'eat')
	- Test your new verb!

New trigger creation:
	- Determine whether trigger is pre or post action
	- Add trigger text to the correct trigger list (pre_action_trigger_lst and post_action_trigger_lst) (currently skippable for 'push')
	- If trigger is post_action ensure that trigger() is called in the verb elif in text_interpreter() 
	- Add trigger logic to trigger()

New item creation:
	- Determine where the item will 'live' (which room or container it will be found in)
	- Add the item to room_dict or container_dict
	- Add the item's description to description.txt

Version 2.0 Goals
	- articles, adjectives, and prepositions
	- Save Game capability
	- Object oriented code
	- Base on examples of efficient code.. focus on pythonic implementation
	- Classes
	- switcher

# +++ Notes +++ 

#	Misc:
#	   Rooms contain items, doors, containers, switches, and creatures
#   	Inventory = backpack + hand + worn
#   	Examine scope = inventory + room_items + room_features + room_name + "burt" + "fist" + view_only + worn
