import json
import sets

map_file = "map.json"

description = "description"
prerequisites = "prerequisites"
objects = "objects"
directions = "directions"
north = "north"
east = "east"
south = "south"
west = "west"
take = "take"
message = "message"
noPrerequisites = "noPrerequisites"
problem = "problem"
solution = "solution"
fighters = "fighters"
killable = "killable"
altDescription = "altDescription"
mustUse = "mustUse"
openObject = "openObject"
canOpen = "canOpen"
onOpen = "onOpen"
forOpen = "forOpen"
action = "action"
objectAdd = "objectAdd"

def _byteify(data, ignore_dicts = False):
	if isinstance(data, unicode):
		return data.encode('utf-8')
	if isinstance(data, list):
		return [ _byteify(item, ignore_dicts=True) for item in data ]
	if isinstance(data, dict) and not ignore_dicts:
		return {
		_byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
		for key, value in data.iteritems()
		}
	return data


class Map:
	def __init__(self):
		with open(map_file, 'r') as map_f:
			self.fsm = json.load(map_f, object_hook=_byteify)
			print(self.fsm)
			

	def goToNextState(self, p_player, p_direction):
		print("Trying to go "+p_direction)
		prerequisites_d = {}
		try:
			newState = self.fsm[p_player.position][directions][p_direction]
		except KeyError:
			print("There is nothing " + p_direction + ".")
			return
		print(newState)
		try:
			prerequisites_d =  self.fsm[newState][prerequisites]
		except KeyError:
			pass
		for item in prerequisites_d:
			for key in item:
				if set(key) > set(p_player.have):
					try:
						print(item[key][problem])
					except KeyError:
						print("You cannot go there.")
					return
				else:
					try:
						print(item[key][solution])
					except KeyError:
						continue
		p_player.moveToNewState(newState, p_direction)
		self.whereAmI(p_player)
		return

	def takeObject(self, p_player, p_object):
		try:
			obj_l = self.fsm[p_player.position][objects]
			if p_object in p_player.have:
				print("You already have that!")
				return
			for obj in obj_l:
				for key in obj:
					if p_object == key:
						print(obj[key][message])
						if obj[key][take]:
							print("TAKING")
							p_player.takeItem(p_object)
							obj[key][take] = False
						return
			print("You see no such thing here.")
		except KeyError:
			print("You cannot do that.")
		
	def killFighter(self, p_player, p_fighter, p_weapon):
		foundFighter = None
		if p_weapon not in p_player.have:
			print("You do not possess this " + p_weapon + " of which you speak.")
			return
		try:
			fighters_l = self.fsm[p_player.position][fighters]
			for fighter in fighters_l:
				for key in fighter:
					if p_fighter == str(key):
						foundFighter = str(key)
						if foundFighter[0].upper() == foundFighter[0]:
							say = foundFighter
						else:
							say = "The " + foundFighter
						say += " ogles you keenly."
						print(say)
						if not fighter[key][killable]:
							say = "You cannot kill "
							if foundFighter[0].upper() != foundFighter[0]:
								say += "the "
							say = foundFighter + "."
							return
						fighter[key][killable] = False
						if p_weapon in fighter[key][mustUse]:
							say = "You draw your " + p_weapon + \
								" and slay "
							if foundFighter[0].upper() != foundFighter[0]:
								say += "the "
	                	                        say += foundFighter + "."
							print(say)
						else:
							say = "You do not possess a weapon worthy " + \
								"of this battle. You decide to live " + \
								"and let live."
							print(say)
							return
						for obj in self.fsm[p_player.position][objects]:
							for k in obj:
								if k == foundFighter:
									obj[k][description] = \
			                                	        str(fighter[key][altDescription])
        		        	                        	obj[k][take] = False
		except KeyError:
			print("There is no " + p_fighter + " you can tussle with here. With a word you can get what you came for.")
			
	'''
	Prints the description of current position
	'''
	def whereAmI(self, p_player):
		try:
			print(self.fsm[p_player.position][description])
			for obj in self.fsm[p_player.position][objects]:
				for k in obj:
					try:
						print(obj[k][description])
					except:
						pass
		except KeyError: # map has no description (but, why?)
			print("There is darkness everywhere. All you can hear is your heavy breathing...")
			
	
	def openObject(self, p_player, p_object):
		try:
                        obj_l = self.fsm[p_player.position][objects]
                        for obj in obj_l:
                                for key in obj:
                                        if p_object == str(key):
                                                if obj[key][openObject][canOpen]:
							if set(obj[key][openObject][forOpen]).\
									issubset(set(p_player.have)) or \
									obj[key][openObject][forOpen] == []:
								try:
									print(obj[key][openObject]\
										[onOpen][action])
									# TODO call to grammar function
								except KeyError:
									pass
								# Seperate try-except because action/objectAdd
								try:
									print(obj[key][openObject][onOpen][objectAdd])
									self.fsm[p_player.position][objects].append(obj[key][openObject][onOpen][objectAdd])
	                                                        	print(obj[key][openObject][onOpen][message])
									obj[key][openObject][canOpen] = False	
								except KeyError:
									pass
								return
			print("That can't be opened.")
                except KeyError:
                        print("You cannot do that.")


if __name__ == "__main__":
	map_o = Map()
