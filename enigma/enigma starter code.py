
# Part 1 : Classes and functions you must implement - refer to the jupyter notebook
# You may need to write more classes, which can be done here or in separate files, you choose.

class PlugLead:
    def __init__(self, mapping):
        # Your code here
        raise NotImplementedError()

    def encode(self, character):
        # Your code here
        raise NotImplementedError()


class Plugboard:
    # Your code here
    raise NotImplementedError()


class Rotor:
    def __init__(self):
        # Your code here
        raise NotImplementedError()

    def encode_right_to_left(self, character):
        # Your code here
        raise NotImplementedError()

    def encode_left_to_right(self, character):
        # Your code here
        raise NotImplementedError()


class EnigmaMachine:
    def __init__(self):
        # Your code here
        raise NotImplementedError()

    def encode(self,text):
        # Your code here
        raise NotImplementedError()

# method which returns a Rotor object
# @param - name - name of the Rotor e.g. I or Gamma
def rotor_from_name(name):
    raise NotImplementedError()

# method with returns an fully set up enigma machine object
# @param - rotors - string of the rotors used in this enigma machine e.g. "I II III"
# @param - reflector - string of the reflector used in this enigma machine e.g. "B"
# @param - ring_settings - string of the ring settings for the rotors, numbered from 01-26 e.g. "01 02 03"
# @param - initial_positions - string of the starting positions of the rotors, from A-Z e.g. "A A Z"
# @param - plugboard_pairs - list of the plugboard pairs to be used, default is an empty list
def create_enigma_machine(rotors,reflector,ring_settings,initial_positions,plugboard_pairs=[]):
    raise NotImplementedError()

# Part 2 : functions to implement to demonstrate code breaking.
# each function should return a list of all the possible answers
# code_one provides an example of how you might declare variables and the return type

def code_one():
    rotors = "Beta Gamma V"
    reflector = "B"
    ring_settings = "23 02 10"
    # initial_positions are unknown
    plugboard = ["VH", "PT", "ZG", "BJ", "EY", "FS"]

    code = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
    crib = "UNIVERSITY"

    return [code]

def code_two():
    return []

def code_three():
    return []

def code_four():
    return []

def code_five():
    return []

if __name__ == "__main__":
    # You can use this section to test your code.  However, remember that your code
    # is automarked in the jupyter notebook so make sure you have followed the
    # instructions in the notebook to make sure your code works and passes the
    # example tests.

    # NOTE - if your code does not work in the notebook when we
    # run the autograded tests you will receive a 0 mark for functionality.
    pass
