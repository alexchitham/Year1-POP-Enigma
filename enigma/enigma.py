
# Part 1 : Classes and functions you must implement - refer to the jupyter notebook
# You may need to write more classes, which can be done here or in separate files, you choose.


class PlugLead: # A class representing the lead connecting two letters
    def __init__(self, mapping): # The parameter is the two letter mapping
      list(mapping)
      if mapping[0] == mapping[1]: # Checks its in the correct form
        raise ValueError("A lead cannot plug a letter into itself")
      if len(mapping) != 2:
        raise ValueError("A lead has to be plugged into two letters")
      self.letterOne = mapping[0]
      self.letterTwo = mapping[1]
       
    # Function that encodes a letter if connected by a lead
    def encode(self, character): 
      if character == self.letterOne:
        return self.letterTwo
      elif character == self.letterTwo:
        return self.letterOne 
      else: return character


# A class that contains a list of all the plugleads
class Plugboard:
  def __init__(self):
    self.plugLeads = [] # Initiates an empty list

  # A function that adds a new pluglead to the board, that has a maximum of 10
  def add(self,Pluglead):
    if len(self.plugLeads) < 10:
      self.plugLeads.append(Pluglead)
    else: ValueError("You only have 10 plug leads")


  # A function that encodes a letter by checking all the plugleads
  def encode(self,character):
    for lead in self.plugLeads:
      newChar = lead.encode(character)
      if newChar != character:
        return newChar
    return character


# A generic class for a rotor, that has all the atttributes for a reflector
class Rotor:
    def __init__(self,name,mapping):
      # For a reflector, only the name and the mapping are needed
      if len(mapping) != 26:
        raise ValueError("You must have a mapping that's 26 letters long")
      self.name = name
      self.mappings = mapping
      self.offset = 0 # Not needed for reflector, but is for all other rotors
      
    # A function for encoding a letter via a rotor, right to left
    def encode_right_to_left(self, character,offset=0):
      index = ord(character) - 65 + offset 
      index = rollOverLetter(index, 25) # Calculates index for letter entering the rotor
      char = self.mappings[index] # Finds the new letter
      newIndex = ord(char) - offset # Calculates index for letter leaving the rotor
      newIndex = rollOverLetter(newIndex, 90)
      newChar = chr(newIndex) 
      return newChar # Returns the new letter

    # A function for encoding a letter via a rotor, left to right
    def encode_left_to_right(self, character,offset=0):
      index = ord(character) + offset # Finds the new index
      index = rollOverLetter(index,90)
      offsetChar = chr(index)
      newIndex = self.mappings.index(offsetChar) # Maps the letter to a new one
      offsetIndex = newIndex + 65 - offset # Finds letter leaving the rotor
      offsetIndex = rollOverLetter(offsetIndex,90)
      newChar = chr(offsetIndex)
      return newChar # Return the new letter

      
# A child class of Rotor objects, with additional attributes and methods
class NoNotchRotor(Rotor):
  def __init__(self,name,mapping,ring_setting,initial_position):
    super().__init__(name,mapping) # Calls the constructor of parent class
    # Checking for invalid inputs
    if int(ring_setting) > 26 or int(ring_setting) < 1:
      raise ValueError("The ring setting must be in the range 1-26")
    if len(initial_position) != 1:
      raise ValueError("The initial position must be one letter")
    elif ord(initial_position) > 90 or ord(initial_position) < 65:
      raise ValueError("The initial postion must be a letter")
    self.initialPos = initial_position
    self.ringSetting = ring_setting
    self.currentPos = initial_position

  # A function that increments the current position of the rotor
  def rotate(self):
    index = ord(self.currentPos)
    index = index + 1
    if index > 90:
      index = index - 26
    self.currentPos = chr(index)

  # Finds the offset using position and ring settings, used when a letter enters
  # a rotor and when a letter is leaving a rotor
  def setOffset(self):
    self.offset = ord(self.currentPos) - 64 - int(self.ringSetting) 
    
    
# A child class of a NoNotchRotor, just has the notch as another attribute
class NotchRotor(NoNotchRotor):
  def __init__(self,name,mapping,notch,ring_setting,initial_position):
    # Calls the parents constructor method
    super().__init__(name,mapping,ring_setting,initial_position)
    if len(notch) != 1:
      raise ValueError("The notch must be one letter")
    elif ord(notch) > 90 or ord(initial_position) < 65:
      raise ValueError("The notch must be a letter")
    self.notch = notch

# A class representing a complete enigma machine
class EnigmaMachine:
  def __init__(self,rotors,plugboard):
    if len(rotors) > 5 or len(rotors) < 4:
      raise ValueError("There are too many or not enough rotors")
    self.rotors = rotors
    self.plugboard = plugboard
    self.numRotors = len(rotors)
  
  # A function that's able to encode a full string to letters
  def encode(self,text):
    newText = ""
    rotorList1 = self.rotors.copy()
    rotorList1.pop(0)
    for char in text: # Iterates through every letter in the code
      
      # Rotates the appropriate rotors based on their notches
      if getRotorType(self.rotors[-1].name) == "notch":
        if self.rotors[-1].currentPos == self.rotors[-1].notch:
          if getRotorType(self.rotors[-2].name) == "notch":
            if self.rotors[-2].currentPos == self.rotors[-2].notch:
              self.rotors[-3].rotate()
          self.rotors[-2].rotate()
      self.rotors[-1].rotate()

      self.rotors[-1].setOffset() # Finds the offset of all three rotors
      self.rotors[-2].setOffset()
      self.rotors[-3].setOffset()

      char = self.plugboard.encode(char) # Encode using plugboard
    
      # Put the letter through all the rotors and reflector, right to left
      for x in range(len(self.rotors)):
        rotor = len(self.rotors) - x - 1
        char = self.rotors[rotor].encode_right_to_left(char,self.rotors[rotor].offset)
      # Put the letter through all the rotors again, but left to right
      for rotor in rotorList1:
        char = rotor.encode_left_to_right(char,rotor.offset)
      
      char = self.plugboard.encode(char) # Encode using plugboard again
      newText = newText + char 
    return newText # Return the encode text

# Returns the notch of a rotor based on its name
def getNotch(name):
  if name == "I": 
    return "Q"
  elif name == "II":
    return "E"
  elif name == "III":
    return "V"
  elif name == "IV":
    return "J"
  elif name == "V":
    return "Z"
  else: return ""
    
# Function that returns the type of rotor from its name
def getRotorType(name):
  if name == "I" or name == "II" or name == "III" or name == "IV" or name == "V":
    return "notch"
  elif name == "Beta" or name == "Gamma":
    return "no notch"
  elif name == "A" or name == "B" or name == "C":
    return "reflector"
  elif len(name) == 26:
    return "modified reflector"
  else: return ""

# Function that ensures a letter cycles back to A after Z
def rollOverLetter(index,max):
  if index > max:
    index = index - 26
  if index < max - 25:
    index = index + 26
  return index

# Function that increments a letter by 1, e.g. changes A to B
def incrementLetter(letter):
  index = ord(letter) + 1
  index = rollOverLetter(index,90)
  return chr(index)

# Converts a mapping string to a list of all the pairs instead
# This function and the one below are used in code 5 to change the mapping of a reflector
def mappingStringToList(mappingString):
  mappings = []
  index = 0
  while len(mappings) != 13:
    ignore = False
    letter1 = chr(index + 65)
    for maps in mappings:
      if maps[1] == letter1:
        ignore = True

    if ignore == False:
      letter2 = mappingString[index]
      mappings.append(letter1 + letter2)
    index += 1
  return mappings

# Converts a list of pairs that map together, to a string
def listToMappingString(mappings):
  newMapString = "00000000000000000000000000"
  newMap = list(newMapString)
  for maps in mappings:
    index1 = ord(maps[0]) - 65
    index2 = ord(maps[1]) - 65
    newMap[index1] = maps[1]
    newMap[index2] = maps[0]

  newMapString = "".join(newMap)
  return newMapString



# method which returns a Rotor object
# @param - name - name of the Rotor e.g. I or Gamma
def rotor_from_name(name):
  if getRotorType(name) != "":
    if name == "I":
      mappings = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    elif name == "II":
      mappings = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    elif name == "III":
      mappings = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    elif name == "IV":
      mappings = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    elif name == "V":
      mappings = "VZBRGITYUPSDNHLXAWMJQOFECK"
    elif name == "Beta":
      mappings = "LEYJVCNIXWPBQMDRTAKZGFUHOS"
    elif name == "Gamma":
      mappings = "FSOKANUERHMBTIYCWLQPZXVGJD"
    elif name == "A":
      mappings = "EJMZALYXVBWFCRQUONTSPIKHGD"
    elif name == "B":
      mappings = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    elif name == "C":
      mappings = "FVPJIAOYEDRZXWGCTKUQSBNMHL"

    # This here for code 5 when the reflectors are changed, can't specify it by name anymore
    elif len(name) == 26:
      return Rotor("Non-standard Reflector", name)

    return Rotor(name,mappings) 


# method with returns an fully set up enigma machine object
# @param - rotors - string of the rotors used in this enigma machine e.g. "I II III"
# @param - reflector - string of the reflector used in this enigma machine e.g. "B"
# @param - ring_settings - string of the ring settings for the rotors, numbered from 01-26 e.g. "01 02 03"
# @param - initial_positions - string of the starting positions of the rotors, from A-Z e.g. "A A Z"
# @param - plugboard_pairs - list of the plugboard pairs to be used, default is an empty list
def create_enigma_machine(rotors,reflector,ring_settings,initial_positions,plugboard_pairs=[]):
  
  rotors = rotors.split() 
  # Assign the relevant variables
  rotorOne = rotor_from_name(rotors[0])
  rotorTwo = rotor_from_name(rotors[1])
  rotorThree = rotor_from_name(rotors[2])
  if len(rotors) == 4: # Works for four rotors too
    rotorFour = rotor_from_name(rotors[3])

  Reflector = rotor_from_name(reflector)
  plugboard = Plugboard()
  ringSets = ring_settings.split()
  initialPos = initial_positions.split()

  # Creates the relevant Rotor object (notched or not) for each rotor, passing in all the parameters
  name = rotorOne.name
  if getRotorType(name) == "notch":
    RotorOne = NotchRotor(name,rotorOne.mappings,getNotch(name),ringSets[0],initialPos[0])
  elif getRotorType(name) == "no notch":
    RotorOne = NoNotchRotor(name,rotorOne.mappings,ringSets[0],initialPos[0])

  name = rotorTwo.name
  if getRotorType(name) == "notch":
    RotorTwo = NotchRotor(name,rotorTwo.mappings,getNotch(name),ringSets[1],initialPos[1])
  elif getRotorType(name) == "no notch":
    RotorTwo = NoNotchRotor(name,rotorTwo.mappings,ringSets[1],initialPos[1])
  
  name = rotorThree.name
  if getRotorType(name) == "notch":
    RotorThree = NotchRotor(name,rotorThree.mappings,getNotch(name),ringSets[2],initialPos[2])
  elif getRotorType(name) == "no notch":
    RotorThree = NoNotchRotor(name,rotorThree.mappings,ringSets[2],initialPos[2])
  
  # Creates a list of rotors used as an attribute for the enigma machine class
  rotorList = [Reflector,RotorOne,RotorTwo,RotorThree] 
  
  if len(rotors) == 4: # Assigns the fourth rotor if there's four
    name = rotorFour.name
    if getRotorType(name) == "notch":
      RotorFour = NotchRotor(name,rotorFour.mappings,getNotch(name),ringSets[3],initialPos[3])
    elif getRotorType(name) == "no notch":
      RotorFour = NoNotchRotor(name,rotorFour.mappings,ringSets[3],initialPos[3])
    rotorList.append(RotorFour)

  if len(plugboard_pairs) > 0: # Assigns mappings to plugboard if there are any
    for pairs in plugboard_pairs:
      plugboard.add(PlugLead(pairs))

  enigma = EnigmaMachine(rotorList,plugboard)
  return enigma # Creates the enigma machine class and returns it






# Part 2 : functions to implement to demonstrate code breaking.
# each function should return a list of all the possible answers
# code_one provides an example of how you might declare variables and the return type


def code_one(): # Takes one second to execute and find solution
    
  # Assigns all the settings to their variables
  rotors = "Beta Gamma V"
  ring_settings = "04 02 14"
  initial_positions = "M J M"
  plugboard = ["KI", "XN", "FL"]
  # Reflector is unknown

  code = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"
  crib = "SECRETS"
  possibilities = [] # Creates an empty list for the possible decryptions

  reflector = "A" # Start with the first reflector
  for i in range(3): # Repeat three times as there's 3 reflectors
  
    enigma = create_enigma_machine(rotors,reflector,ring_settings,initial_positions,plugboard)
    plainText = enigma.encode(code) # Encodes the text using the enigma object
  
    if crib in plainText: # Checks if the crib word is in the plaintext
      possibilities.append(plainText)

    reflector = incrementLetter(reflector) # Look at the next reflector

  return possibilities # Return the list of possible decryptions



def code_two(): # Takes about 1 minute to execute and find solution

  rotors = "Beta I III"
  reflector = "B"
  ring_settings = "23 02 10"
  # initial_positions are unknown
  plugboard = ["VH", "PT", "ZG", "BJ", "EY", "FS"]

  code = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
  crib = "UNIVERSITY"
  possibilities = []

  initial_positions = "A A A" # Start with default positions
  for combos in range(26 * 26 * 26): # There are that many different possibilities
    
    enigma = create_enigma_machine(rotors,reflector,ring_settings,initial_positions,plugboard)
    plainText = enigma.encode(code)

    if crib in plainText:
      possibilities.append(plainText)

    # Increments the positions so that all possibilities are tested
    newPositions = initial_positions.split()
    newPositions[-1] = incrementLetter(newPositions[-1])
    if newPositions[-1] == "A":
      newPositions[-2] = incrementLetter(newPositions[-2])
      if newPositions[-2] == "A":
        newPositions[-3] = incrementLetter(newPositions[-3])
  
    initial_positions = newPositions[0] + " " + newPositions[1] + " " + newPositions[2]

  return possibilities



def code_three(): # Takes about 3 mins to execute and find solution

  initial_positions = "E M Y"
  plugboard = ["FH", "TS", "BE", "UQ", "KD", "AL"]
  code = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"
  crib = "THOUSANDS"
  possibilities = []
  # Reflector is unknown
  # Rotors and ring settings are restricted to these lists of values
  posRotors = ["Beta","Gamma","II","IV"]
  posRingSets = ["02","04","06","08","20","22","24","26"]
  newRotors = posRotors.copy()

  reflector = "A"
  for x in range(3): # Three iterations as there are three reflectors

    for ringOne in posRingSets: # Trying each possible ring settings for each of the 3 rotors
      for ringTwo in posRingSets:
        for ringThree in posRingSets:

          ring_settings = ringOne + " " + ringTwo + " " + ringThree

          # Tries all possible rotor combinations, removes the rotor from the list each time
          # as you can't use the same rotor more than once in a single enigma machine
          for rotorOne in newRotors:
            newRotors.remove(rotorOne)
            for rotorTwo in newRotors:
              newRotors.remove(rotorTwo)
              for rotorThree in newRotors:

                rotors = rotorOne + " " + rotorTwo + " " + rotorThree
        
                enigma = create_enigma_machine(rotors,reflector,ring_settings,initial_positions,plugboard)
                plainText = enigma.encode(code)

                if crib in plainText:
                  possibilities.append(plainText)
              
              newRotors.insert(0, rotorTwo)
            newRotors.insert(0, rotorOne) # Adds the rotors back into the list
              
    reflector = incrementLetter(reflector)

  
  return possibilities

def code_four(): # Takes a few seconds to execute and find the solutions

  rotors = "V III IV"
  reflector = "A"
  ring_settings = "24 12 10"
  initial_positions = "S W U"

  code = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"
  crib = "TUTOR"
  possibilities = []
  
  plugboard = ["WP", "RJ", "VF", "HN", "CG", "BS"]

  allowedLetters = [] # An empty list that will contain all the letters that can be used
  letter = "A"
  index = 0
  for i in range(26):
    allowedLetters.append(letter) # So currently all letter are allowed
    letter = incrementLetter(letter)
  
  for plugs in plugboard: # Remove any letters that are already used in the plugboard
    allowedLetters.remove(plugs[0])
    allowedLetters.remove(plugs[1])

  allowedLetters.remove("A")
  allowedLetters.remove("I")

  # Testing all possible combinations, removing each time as the same letter cannot be used twice
  for letter1 in allowedLetters:
    plugboard.append("A" + letter1)
    allowedLetters.remove(letter1)
    for letter2 in allowedLetters:
      plugboard.append("I" + letter2)

      enigma = create_enigma_machine(rotors,reflector,ring_settings,initial_positions,plugboard)
      plainText = enigma.encode(code)

      if crib in plainText:
        possibilities.append(plainText)
      
      plugboard.pop()

    allowedLetters.insert(index, letter1) # Adds the letter back in the correct place
    index += 1
    plugboard.pop()

  return possibilities



def code_five(): # Takes about a minute to execute and find the solution

  rotors = "V II IV"
  ring_settings = "06 18 07"
  initial_positions = "A J L"
  plugboard = ["UG", "IE", "PO", "NX", "WT"]

  code = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"
  cribs = ["FACEBOOK", "TWITTER", "WHATSAPP", "INSTAGRAM"] # Got a few different crib words to try
  possibilities = []
  combinationsTried = [] # Keeps track of what it's tried to stop it testing the same combination twice

  reflector = "A"
  for x in range(3):

    reflectorObject = rotor_from_name(reflector)
    mappingString = reflectorObject.mappings # Get the mapping of the reflector

    mappings = mappingStringToList(mappingString) # Turns it into a list of pairs instead
    
    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    
    # Chooses 4 of the 13 pairs of mappings in the reflector
    # Removes them each time as we can't change the same pair twice
    for mapping1 in mappings:
      mappings.remove(mapping1) 
      for mapping2 in mappings:
        mappings.remove(mapping2)
        for mapping3 in mappings:
          mappings.remove(mapping3)
          for mapping4 in mappings:
            mappings.remove(mapping4)
            ignore = False

            listOfMaps = [mapping1, mapping2, mapping3, mapping4]
            listOfMaps.sort() # Puts it in alphabetical order

            # Will only try the combination of 4 pairs if it hasn't tried it already
            for combo in combinationsTried:
              if listOfMaps == combo:
                ignore = True

            if ignore == False:
              combinationsTried.append(listOfMaps)

              for arrangements in range(3):
                # The different ways to pair up the four reflector cables
                if arrangements == 0:
                  map2 = mapping2
                  map3 = mapping3
                  map4 = mapping4
                elif arrangements == 1:
                  map2 = mapping3
                  map3 = mapping2
                  map4 = mapping4
                else:
                  map2 = mapping4
                  map3 = mapping2
                  map4 = mapping3

                # Tries all the possible ways of changing the letters for each pair of wires
                for maps in range(2):
                  if maps == 0:
                    newMap1 = mapping1[0] + map2[0]
                    newMap2 = mapping1[1] + map2[1]
                  else:
                    newMap1 = mapping1[1] + map2[0]
                    newMap2 = mapping1[0] + map2[1]
                
                  for maps2 in range(2):
                    if maps2 == 0:
                      newMap3 = map3[0] + map4[0]
                      newMap4 = map3[1] + map4[1]
                    else:
                      newMap3 = map3[1] + map4[0]
                      newMap4 = map3[0] + map4[1]

                    # Add each new map to the list of pairs
                    mappings.append(newMap1)
                    mappings.append(newMap2)
                    mappings.append(newMap3)
                    mappings.append(newMap4)

                    # Turns it back into a string as that's the format used in the encode functions
                    newMappingString = listToMappingString(mappings)
                    
                    enigma = create_enigma_machine(rotors,newMappingString,ring_settings,initial_positions,plugboard)
                    plainText = enigma.encode(code)
                    #print(plainText)
                    
                    # Tests all words in the possible cribs
                    for crib in cribs:
                      if crib in plainText:
                        possibilities.append(plainText)
                
                    for i in range(4):
                      mappings.pop() # Remove all those changed mappings off the list

            # Adds all the original mappings back on so another four can be chosen
            mappings.insert(counter4, mapping4)
            counter4 += 1

          mappings.insert(counter3, mapping3)
          counter3 += 1
        
        mappings.insert(counter2, mapping2)
        counter2 += 1

      mappings.insert(counter1, mapping1)
      counter1 += 1

    reflector = incrementLetter(reflector)
    mappings.clear() # Clears the mapping pairs so the process can repeat for all reflectors

  return possibilities



if __name__ == "__main__":
    # You can use this section to test your code.  However, remember that your code
    # is automarked in the jupyter notebook so make sure you have followed the
    # instructions in the notebook to make sure your code works and passes the
    # example tests.

    # NOTE - if your code does not work in the notebook when we
    # run the autograded tests you will receive a 0 mark for functionality.

  pass