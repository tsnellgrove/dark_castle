+++ To Dos +++

Updates for v1.6
	Sort out Working Copy
		DONE: Get live connection working (Open from Pythonista file manger - use app chooser)
		DONE: Test an Undo / Revert (pre remote push, left swipe on commit to undo then "revert" at top)
	Centralize lists and dictionaries
		DONE: worn_dict => description_dict
		DONE: room_dict descriptions => description_dict
		DONE: writing_dict text => description_dict [remove commented txt]
		DONE: consolidate writing_dict into single level dictionary
		DONE: creature_dict descriptions => description_dict
		DONE: understand and the update_dict and migrate to description_dict (crystal box testing needed)
		DONE: food_dict txt => description_dict
		DONE: remove creature_dict from timer, trigger, and update routines
		DONE: state_dict['hedgehog_state] => creature_dict
		DONE: Move timer from state_dict to timer_dict
		DONE: Move timer descriptions to description_dict and make timer_dict single level
		DONE: use '-base' to isolate logic from text descriptions (switch descriptions => door descriptions)
		DONE: move broach_found => generalized max_count dict

Updates for v 1.7
		DONE: reduce path_dict to only valid paths and create random text for banging into wall
		DONE: intro => description_dict
		DONE: move 'invalid_path' to static_dict
		DONE: help text => description_dict
		DONE: credits => description_dict & valid 1-word command
		DONE: pre_action_trigger_lst => static_dict
		DONE: post_action_trigger_lst => static_dict
		DONE: written_on_dict => static_dict
		consolidate single_depth static lists & dicts
		consolidate some variable single-level dicts (e.g.score_dict => state_dict ? [aka 'global_dict])
		use '.lower().strip() on input'
		consider using 'import textwrap'
		normalize each "if verb"
		clean up variable passing
		separate descriptions into text file and import at start of game
		document the terms of art (e.g. items vs. features vs. view_only)
	More testing - Offer the boys $0.50 to finish the game and $0.35 bug bounty
	docstrings for all functions [?]

Updates for v 1.8
	Post to GitHub using working Copy


Maintenance, clean-up, and features I should implement someday
		"close" verb
		5th room - mouse hole - to exercise existing capabilities (e.g. "food" that can be eaten)
			copper key opens cabinet which holds potion
			potion shrinks for set turn count (can only drink twice); toes tingle just before you expand
			enter mouse hole
			maybe fight mouse?
			silver key in mouse trap; need to swap with copper key
			find a use for close command?
			would be fun to use every verb ;-D
	more directions
	landscape / path changes
	Text Adventure Link: https://inventwithpython.com/blog/2014/12/11/making-a-text-adventure-game-with-the-cmd-and textwrap-python-modules/
	Find a more efficient way to tell the player "you can't go that way" - unique path descriptins won't scale well to 10 cardinal directions for 10+ rooms
	Fix trigger so that it no longer sometimes returns a value and sometimes doesn't
	repeat option like 'again' / 'g' in Zork (JE request)
	Future deployment options: Cloud web, instance, container, Lambda / serverless, mobile, text, echo
	create a "generalized" verb block with trigger & score for every verb
	shorter variable names!!
	'wear' implementation has similar limitations to containers... no limits on how many similar items can be worn
	Containers implementation is very cheesey 
			No concept of the container being _in_ in the room - contents basically just dumped to room
			no capacity limits
			no 'put'
		No 'close' command for doors or containers...
			I could implement this pretty easily but there are no puzzles that need it yet
		move 'can_be' lists to local elif ?
	   	Review variable passing
		normalize variable names (e.g. consistent _dict, _lst, _txt suffixes)
		Convert simple elifs to switchers
		Consider making state_dict['active_timers'] a list to allow for multiple simultaneous active timers
		Add "return" at end of each function
		Re-do format of long print sections with "x" + "y" across multiple lines
		Make sure the hedgehog description is updated again after return_of_sword code is written
		Eventually maybe just variable and constant dictionaries??
		Merge all dictionaries of dictionaires (e.g. food, writing, creatures) into one master entities_dict
		Create constants_dict ??
		Create a "repeat" command that lets you put the same text on the command line but then lets you edit it (like 'g' in Zork)
		Evolving my dictionary vision... maybe descriptions, keys, entities, and states... but need to understand classes first
		Clean up hedgehog timer conditionals

	Make silver_sword puzzle more beginner-friendly... consider making stale_biscuts supply 'bottomless'
		Note from Burt's Mom telling him to whistle for more biscuts
		Perhaps have Baker weinner dog Schnitzel come woofing along with more biscuts from entrance... 
		need a state_dict variable to track total world biscut population
		would give time for Baker history and great, great grandmother McVities 
		Never forget Burty... you may not be biscuts and weiner dogs.. but you're from biscuts and weiner dogs.. never forget where ya from
		Maybe somehow also fit in tale of Goblin?? (Bright Castle caretakeer, 'a real goblin of a man.. and that was back in the good days')
		Could use as hedgehog run-away reset as well?

	Create a Save routine... what is needed to caputure state?
		Create save_dict with same entries as state_dict, score_dict, and room_dict and any other variable dictionaries
		Save => write state_dict to save_dict
		Restore => write save_dict to state_dict
		Above will work within session but will need to write to file to survive between sessions
 		Will need to run description_update() based on state_dict[hedgehog_state] 

	Associate Epilogs with Each end game score
		Functionality
			Associate endings with accomplishments from score_dict 
			Provide ending text for accomplishments and whether Burt lived to wander back to the pub or died
		Implementation
			Create epilog_dict to hold text
			Add logic to end() to call and print correct epilog for accomplishment values from epilog_dict
