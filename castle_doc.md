+++ Documentation +++

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

Noun types:
- Items: Nouns that can be taken
- Features: Nouns that can be interacted with but not taken. Includes doors, containers, creatures, and switches.
- Vew_only: Nounds that can be examined but not taken or interacted with.
- Doors: May be locked or unlocked (with the right key). If unlocked a door can be opened. Finding a way to open a door is one of the most basic puzzle elements in the game.
- Containers: Like doors, containers can be locked or unlocked and open or closed. Also, they can contain things. Once a container i open it's contents are added to the room 'items' and may be taken. Due to linguistic limitations (i.e. only noun verb pairs) items cannot be put back into a container. No concept of container capaicty has been coded yet.
	- Note on Doors and Containers: At present only 'unlock' and 'open' are implemented. I plan to implement 'close' and 'lock' when I write a puzzle that utilizes these. It does irk me that Burt wanders through the Dark Castle like a random murder hobo leaving a swath of unclosed doors behind him. I picture his Nana yelling "Burty Baker, for goodness sake, close the door behind you!". I'm also considering implementing 'put' <item> to place something in a container... this would limit the game to one container per room - but that seems like a reasonable tradeoff.
- Switches: Set values and trigger effects. At present 'levers' are implemented to set values and 'buttons' trigger effects but the reverse is also possible. Also other switch types are possible - e.g. dials, knobs, switches, etc.
- Creatures: Living entities that Burt can interact with. These may be helpul (like the 'hedgehog' when treated well) or hazardous (like the 'goblin' and 'crocodile'). Finding the right gift or weapon needed to interact with a creature is a common puzzle element in the game.

Inventory types:
- Hand: Can hold exactly one item. Anything taken goes into your hand. Anything dropped is dropped from your hand. Something must be in your hand in order to wear or eat it.
- Backpack: Items can be taken from your backpack. There is no mechanic to intentionally place something in your backpak but any overflow from your hand (i.e. if you are holding the 'rusty_key' and take the 'shiny_sword', the 'rusty_key' is automatically placed in your backpack). There is no capacity limit to your backpack.
- Worn: In theory, multiple items can be worn but at paresent only the 'royal_crown' is wearable. Wearing an item may have an effect (e.g. the 'royal_crown' enables the magic of the 'scroll_of_the_king').

Noun scopes:
- Room scope = items + features + view_only + the contents of open containers
- Inventory scope = hand + backpack + worn

Verb overview:
- Before the verb ifel statements, check for a pre-action tirgger; Escape if one exists
- At the start of each verb ifel, check for scope to ensure that the command is possible (i.e. the item is 'takeable' or 'wearable' or such).
- At the end of each verb ifel statement check for post-action triggers
- At the end of each verb ifel statment check score_key for score changes.

Verbs-Noun Interactions:
- examine: Scope = room scope + inventory scope + view_special. Probably the most frequently used verb in the game. Check's specially for open containers and lists their contents.
- take: Scope = room items + backpack + worn. Possibly the most complicated verb. Upon confirming scope, adds the taken item to 'hand'. Adds the current contents of 'hand' to 'backpack'. Updates the 'backpack' or 'worn' lists or the room or container dictionaries to remove the taken item from its source.  Adds a 'nothing' placeholder to 'backpack' or 'worn' if 'take' leaves them empty.
- drop: Scope = 'hand'. Dropped items are added to the room dictionary. If 'hand' contains 'nothing' then don't allow 'drop'.
- open:
- unlock:
- read:
- attack:
- eat:
- pull:
- push:
- wear:
- close: [future]
- lock: [future]
- put: [future]
- give: [future]
- stow: [future]

Mechanics

Dictionaries and Lists

Puzzles

Story

+++ Steps for Game Expansion +++

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

+++ Limitations & Goals +++

Version 1.0 Major Limitations
- Only 2 word sentences... adjectives are connected to nouns using "_"
- No prepositions
- Only one timer active at a time (is this still true??)
- If you attack the hedgehog while it's eating the stale_biscuts simply vanish

Version 2.0 Features
- articles, adjectives, and prepositions
- Save Game capability
- Object oriented code
- Base on examples of efficient code.. focus on pythonic implementation
- Classes
- switcher

