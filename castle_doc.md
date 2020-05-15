+++ Documentation +++

What is Interactive Fiction?
- IF / Text Adv
- Zork
- TADS
- Frotz on iPad
- Learn more at





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
- For better or worse, verbs are the heart of the program; its primary organizing structure. Nouns come and go from list to list but verbs drive the program and the story forward.
- Each noun-verb pair verb is an ifel in the interpreter_text loop
- Each verb ifel has some common features: 
	- Before the verb ifel statements, check for a pre-action tirgger; Escape if one exists
	- At the start of each verb ifel, check for scope to ensure that the command is possible (i.e. the item is 'takeable' or 'wearable' or such).
	- Asign local variables to make dictionary calls shorter and clearer
	- Upon confirming scope and performing action each verb ifel confirms success to the player (e.g. 'Taken', 'Openned', etc)
	- At the end of each verb ifel statement check for post-action triggers
	- At the end of each verb ifel statment check score_key for score changes.

Verbs-Noun Interactions:

- examine: Many things can be examined. Scope = room scope + inventory scope + view_special + room name. Probably the most frequently used verb in the game. Check's specially for open containers and lists their contents.

- take: Items can be taken. Scope = room items + backpack + worn. Possibly the most complicated verb. Upon confirming scope, adds the taken item to 'hand'. Adds the current contents of 'hand' to 'backpack'. Updates the 'backpack' or 'worn' lists or the room or container dictionaries to remove the taken item from its source.  Adds a 'nothing' placeholder to 'backpack' or 'worn' if 'take' leaves them empty.

- drop: Items in your hand can be dropped. Scope = 'hand'. Dropped items are added to the room dictionary. If 'hand' contains 'nothing' then don't allow 'drop'.

- open: Doors and container features can be opened. Scope = allowed_language['can_be_openned'] and (feature in room) and (not open) and (not locked). There is code to update the door / container description as "open". If the feature is a container and opening reveals contents then the contents are revealed and added to the rooms inventory.

- unlock: Doors and container features can be unlocked. Scope = allowed_language['can_be_openned'] and (feature in room) and (not open) and (is locked). Upon confirming scope, test to ensure that the player has the correct key in 'hand'. If so, set door state to 'unlocked'.

- read: Some items or features have text on them. Text can be read. Scope = allowed_language[can_be_read] and (room scope + inventory scope). Check to ensure that the text referenced is written on an item or feature that is in scope. If so, print the text message.

- attack: Creature features can be attacked. The results of the attack may vary based on whether the player has a weapon (e.g. the shiny_sword or the grimy_axe) or just their fists. Attack results are deterministic based on creature and attack weapon (i.e. there are no die rolls). Ultimately, creatures are more puzzles to solve than they are RPG enemies to defeat. Scope = allowed_language[can_be_attacked] and (creature is in room_features). If attack is in scope, 'hand' is checked to determine attack_weapon (if no weapon in hand, attack_weapon = 'fist'). Based on creature and attack_weapon an attack description is printed. Then, based on attack_weapon, an attack result is looked up in creature_dict. The three possilbe results are 'creature_death', 'creature_runs', and 'player_death'. player_death prints a result description and calls end(). creature_runs prints a result description, removes the creature from room_features, and updates score. creature_death removes creature from room_features and replaces it with dead_creature, prints a result description, updates score, and then adds any 'drops' items (stored in creature_dict) to room_items. Because score is dependent on attack_result, attack is the only verb that does not genericaly check score at the end of the verb ifel.

- eat: Food can be eaten. This is probably my least implemented verb. You can't actually eat anything in the game but I thought it was only fair to let the player attempt to eat the stale_biscuits. Scope = allowed_language[can_be_eaten] and (in 'hand'). If scope is met, print eat description. There is a food_dict sub-dictionary in static_dict meant to track eating results but this is not currently implemented.

- pull: Levers can be pulled to change a state as a standard action. Other features may be pulled via trigger. Scope = allowed_lang_dict[can_be_pulled] and in (room_view_only or room_features). If in scope and word2 is in switch_dict, swap switch_state from up to down or vice versa and update switch description. For cases other than levers controlling state, trigger can be used to initiate an action (e.g. 'pull throne').

- push: Buttons can be pushed to trigger an action as a standard action. Other features may be pushed via trigger. Scope = allowed_lang_dict[can_be_pushed] and in (room_view_only or room_features). If in scope and word2 is in switch_dict check to see is switch success value == current switch value. If it does update trigger_key and score_key (the actual action will be handled via the tirgger routine). If switch success value != current switch value print failure description. I also track button pushes. Non-button push cases (e.g. push throne) can be handeled via trigger.

- wear: Garments can be worn. Scope = allowed_lang_lst['can_be_worn'] and (item in 'hand'). If scope conditions are met, append garment to 'worn' and clean up "nothing" placeholder if needed ('worn' is tracked in state_dict[worn] so that it can be printed during inventory). Remove garment from 'hand' and add "nothing" placeholder if needed. Print confirmation of command to player along with any effects of donning the garment. At present the only wearable item is the royal_crown. It feels like the hedgehog_broach should also be wearable but I feared that this would be a red herring for the scroll_of_the_king puzzle. I'd like to add one more room that provides a puzzle that is solved by wearing the hedgehog_broach.

- close: [future] "For the love of God Burt, close the door!". Would like a puzzle that requires 'cloes'
- lock: [future] Feels like if you can unlock something you should be able to lock it. Again, puzzle needed.
- put: [future] Place contents of 'hand' in container. Syntax = "put <item>". Assumes one container per room.
- give: [future] Give contents of 'hand' to a creature. Syntax = "give <item>". Assumes one creature per room.
- stow: [future] Explicitly put something into your backpack. Syntax = "stow <item>".
- swap: [future] Swap the contents of 'hand' with a takeable item. Syntax = "swap <takeable item>". Puzzle needed.

Mechanics (include scoring & titles)

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

