import player
import grammar
import gameMap

import random

what_next = ["What do you do? ", "What next? ", \
                "What do you do next? "]
try:
	input = raw_input
except NameError:
	print("Cannot port input.")

def whatNext():
	return what_next[random.randint(0, len(what_next)-1)]

def do(p_input, map_o, player_o, grammar):
	functionName, misc = grammar.getGrammarType(p_input)
	if functionName is None:
		print("Did not catch that...")
		return 1
	function = getattr(map_o, functionName)
	function(player_o, *misc)
	return 0

def gameLoop(map_o, player_o, grammar_o):
	map_o.whereAmI(player_o)
	said = ""
	bad_said = 0
	while True:
		try:
			said = raw_input(whatNext()).lower()
		except KeyboardInterrupt, EOFError:
			print("\n\nBuh-bye.")
			quit()
		except:
			print("\nThat did not make sense to me.\nIf you wish to exit, type 'quit' or 'q' or press ctrl-C.")
			continue

		if said == "quit" or said == "q":
			break

		if said == "save":
			print("Saving game...")
			gameMap.saveGame(map_o.fsm, player_o)
			print("Your progress has been saved.\n")
			continue

		if do(said, map_o, player_o, grammar_o):
			bad_said += 1
		else:
			bad_said = 0
		print("")
		if bad_said >= 3:
			print("To display a list of commands you can use, type 'help'.")
			bad_said = 0


def main():
	if gameMap.welcome():
		map_o = gameMap.Map()
		player_o = player.Player()
		print("Starting a new game.")
	else:
		map_, playerp_, playerd_, playerh_ = gameMap.loadGame()
		if map_ is not None:
			print("Loading your saved game.")
			map_o = gameMap.Map(map_)
			player_o = player.Player(playerp_, playerh_, playerd_)
		else:
			print("Starting a new game.")
			map_o = gameMap.Map()
			player_o = player.Player()
	try:
		input("Press enter to continue...")
	except (KeyboardInterrupt, EOFError):
		print("\nBye.")
		quit()

	grammar_o = grammar.Grammar()
	gameLoop(map_o, player_o, grammar_o)

if __name__ == "__main__":
	main()
