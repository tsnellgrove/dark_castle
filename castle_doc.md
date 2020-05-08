+++ Documentation +++

Version 1.0 Known Limitations
- Only 2 word sentences... adjectives are connected to nouns using "_"
- No prepositions
- Only one timer active at a time (is this still true??)
- If you attack the hedgehog while it's eating the stale_biscuts simply vanish

Program approach:
- The coding style (for better or worse) is nearly 'anti-object-oriented'
- Verbs are the central construct of the code
- Everything else is a series of loosely connected (at best) dictionaries and lists
- This is not something I set out to do.. the style arose naturally from beginner programming techniques and a 'figure it out as I go' approach to writing the text adventure
- The result is code that is challenging to maintain and extend because you need to update so many diseparate lists anytime you want to change anything
- Although not ideal from a coding standpoint I don't really have any regrets. This has given me a lot of practice with lists and dictionaries and a deep appreciation for object-oriented coding

Program layout
- A Main Routine that first imports modules and loads description.csv into description_dict
- The Main Routine then takes user input and calls interpeter_text() until user input = 'quit'
- The interpeter_text() function is an if - elif chain of all existing one-word commands and verbs
- Each verb elif performs a standard action on allowed verbs (e.g. 'take' and item into the players 'hand')
- Helper Routines assist with common tasks (e.g. print_score)
- Situational_Logic routines address special puzzle cases where standard actions cause non-standard results (e.g. 'take shiny_sword' in the main_hall is blocked by a hungry hedgehog)
- There are a collection of smaller static and stateful dictionaries and lists that hold game variables (e.g. room_dict)

Linguistics (such as they are):
- The linguistics are extremely primitive
- All sentences are either one word or 2-word noun-verb pairs
- There are no articles, adjectives, adverbs, prepositions, or direct objects
- This means you can 'take' the scroll_of_the_king out of the container but you litterally can't put it back
- ('put' is essentially impossible in a noun-verb pair)
- One of my main user experience goals for version 2.0 is to enrich the interpreter

Noun types
#	   Rooms contain items, doors, containers, switches, and creatures
#   	Inventory = backpack + hand + worn
#   	Examine scope = inventory + room_items + room_features + room_name + "burt" + "fist" + view_only + worn

Mechanics

Dictionaries and Lists

Puzzles

Story

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

+++ Version 2.0 Goals +++

Version 2.0 Features
	- articles, adjectives, and prepositions
	- Save Game capability
	- Object oriented code
	- Base on examples of efficient code.. focus on pythonic implementation
	- Classes
	- switcher

