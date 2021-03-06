+++ To Dos +++


*** Future Versions and Features ***

2.x Website To Do

Flask Testing
	- DONE: Change version naming to x.y.z notation
	- DONE: Read about Flask functions
	- DONE: re-read number input / output example
	- 2.0.1 Learn Flask basics: 
		- https://realpython.com/introduction-to-flask-part-1-setting-up-a-static-site/
	- 2.0.2 Basic test local site with input
	- 2.0.3 Basic test local site with input box; prints a locally asigned variable
	- 2.0.4 Created a very basic processing.py script to enable input / output testing
	- 2.0.5 Good updates - have input and output linked to web site & sub function calling working
	- 2.0.6 Sessions working (?) but still can't retain text_lst values
	- 2.0.7 Finally got session variable to be persistent!!
	- 2.0.8 Sorted out the KeyError issue and got session.pop() working (well, most of the time)
	- 2.0.9 Wrote pseudo code for how flask wrapper would work if all stateful data was stored in session dictionaries 	
	- 2.0.10 get flask test into git
	- 2.0.11 got git branching working (I think)
	- 2.0.12 working through a really frustrating working copy / pythonista remote file call bug :(
	- 2.0.13 After much adventure got flask_test3.py running smoothly on pythonanywhere with git integration
	- 2.1.0 NEXT TO DO - REALLY FIGURE OUT HOW TO USE GIT BRANCHING / FORKS
		- July 13: Reading up on Git branching - sounds like tags will be helpful - more research to do
		- July 14: Read up on app versioning - I need to get more consistent about this
			- Less clear is coding across platforms... it's beginning to look like there's no one simple solution to this
			- I will need to roll my own
			- Maybe start by functionalizing Dark Castle and make that version work at the command line


To Dos:
- set a versioning scheme (x.y.z) and official version notes; also create a version command in Dark Castle 
	- Link: https://medium.com/@GabEarnsh/versioning-mobile-app-releases-like-a-pro-25137766150a



	struggling with very basic import issues... not sure what's going on
	branch flask test
	update test to match pseudo code
	branch dark_castle.py for flask version
		decide on how to store data... maybe first pass is client-side cookies, then server-side JSON then Redis
		Need to re-apply description updates on load.. or maybe just JSON?? Or maybe special dict just for those?
		Create dynamic description dict and update descript_dict on load (for update in update_dict descript_dict[update] = update_dict[update])
	Need to buckle down and take some flask courses independent of my project (just do it)

Next
	- Sort out Git Branching
	- convert interpreter_text to function using print to buffer approach (redirect stdio)
	- flaskify main routine
	- get it working on local host website
	- get working on python anywhere or Heroku
	- figure out sessions
	- Git integration
	- Investigate AWS implemenations
	- Future deployment options: Cloud web, instance, container, Lambda / serverless, mobile, text, echo
	- Initial function thinking:
		- dark_castle includes:
			- fask code, dictionaries, imports, while != end_state (input, interpreter_text(), print buffer)
			- pass buffer and end_state in interpeter_text()
		- interpreter_text includes: 
			- imports, check for quit, timer code, std code (all prints to buffer)
			- end() => updates end_state
	- Functionalize thoughts:
		- What is the value of functionalizing? Maybe just convert output to buffer??

3.x Minor Edits:
	Joshua idea: give the player an option to be a boy (Burt) or a girl (Rose); or maybe let them choose their own name
	make synthetic score_keys more consistent (e.g. always '-success'; 'gator-crown' => 'croc-crown-success')
	provide printtw() options for double spacing (add print() to inner for) and also change column width
	use .strip() on input
	Fix trigger so that it no longer sometimes returns a value and sometimes doesn't
	maybe put the throne attop a 'dias' (just to be more purple prose ;-D)
	add guiding error message for unseen verbs
	docstrings for all functions [?]
	map routines graphicaly; consider "flattening" function calls (?)
	normalize variable names (e.g. consistent _dict, _lst, _txt suffixes)
	Consider making state_dict['active_timers'] a list to allow for multiple simultaneous active timers

3.x General
	add 'close' 
	add 'lock'
	consider adding 'put' for containers
	consider implementing 'give' for creatures
	implement 'stow' for backpack
	implement container capacity limits
	consider normalizing pre - and post checks for verbs (??)
		- create a "generalized" verb block with trigger & score for every verb
	'wear' implementation has similar limitations to containers... no limits on how many similar items can be worn
	Create a "repeat" command that lets you put the same text on the command line but then lets you edit it (like 'g' in Zork)

3.x Make silver_sword puzzle more beginner-friendly... consider making stale_biscuts supply 'bottomless'
	Note from Burt's Mom telling him to whistle for more biscuts
	Perhaps have Baker weinner dog Schnitzel come woofing along with more biscuts from entrance... 
	need a state_dict variable to track total world biscut population
	would give time for Baker history and great, great grandmother McVities 
	Never forget Burty... you may not be biscuts and weiner dogs.. but you're from biscuts and weiner dogs.. never forget where ya from
	Maybe somehow also fit in tale of Goblin?? (Bright Castle caretakeer, 'a real goblin of a man.. and that was back in the good days')
	Could use as hedgehog run-away reset as well?

3.x Create a Save routine... what is needed to caputure state?
	Create save_dict with same entries as state_dict, score_dict, and room_dict and any other variable dictionaries
	Save => write state_dict to save_dict
	Restore => write save_dict to state_dict
	Above will work within session but will need to write to file to survive between sessions
	Will need to run description_update() based on state_dict[hedgehog_state] 

3.x Associate Epilogs with Each end game score
	Functionality
		Associate endings with accomplishments from score_dict 
		Provide ending text for accomplishments and whether Burt lived to wander back to the pub or died
	Implementation
		Create epilog_dict to hold text
		Add logic to end() to call and print correct epilog for accomplishment values from epilog_dict


4.x Object Oriented Ideas:
	Classes
	Text Adventure Link: https://inventwithpython.com/blog/2014/12/11/making-a-text-adventure-game-with-the-cmd-and textwrap-python-modules/
	Link score increases to item, room, and door objects
	embed smarts / behavior into switches; create a generic switch model
	idea: embed paths into rooms
	idea: need a more elegant way to handle 'untakable' path (e.g. e, w, s @ entrance) descriptions 
	idea: brief vs. verbose modes
	create "availability" categories - (i.e. viewable, interactable, hand) [??]
	verbs to functions with switcher?? (too much variable passing?)
	concept of the container being _in_ the room - currently contents basically just dumped to room

5.x Additional rooms
	5th room
		mouse hole - to exercise existing capabilities (e.g. "food" that can be eaten)
		copper key opens cabinet which holds potion
		find a use for 'close' verb; maybe potion refill
		possibly create 'return' verb to put things back (or maybe 'swap')
		potion shrinks for set turn count (can only drink twice); toes tingle just before you expand
		enter mouse hole
		maybe fight mouse?
		silver key in mouse trap; need to swap with copper key
		find a use for close command?
		would be fun to use every verb ;-D
		maybe a guard mouse that only lets you past if you're wearing the hedgehog_broach
		Indiana Jones reference for mouse trap and ball chasing you out ;-D
		make hedgehog_broach wearable
		link puzzle to total number of moves? Or to score?
		repeat option like 'again' / 'g' in Zork (JE request)
	Possibly add a room 6 with time travel??
		find a use for the word "griffonage" (illegible handwriting)

5.x Future Ideas:
	fun idea - small creature - like a mouse - as an item
	more directions
	landscape / path changes
	create 'win' test routine with checksum



