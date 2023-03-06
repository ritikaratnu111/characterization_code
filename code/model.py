#This class interprets the instruction read by assembly
from ISA import ISA

class Model():

    def __init__(self):
        self.ISA = ISA()

    def set_model(self,name, attribute_values):
        self.ISA.attributes[name] = attribute_values
        self.ISA.set_active_cycles()

Model()
