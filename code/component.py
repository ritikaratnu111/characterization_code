import csv

class CreateComponent(object):
    def __init__(self, name, signals):
        self.name = ""
        self.signals = None
        self.set_name(name)
        self.set_signals(signals)
        #self.print_component()

    def set_name(self, name):
        self.name = name

    def set_signals(self, signals):
        self.signals = signals

    def print_component(self):
        print(self.name, self.signals)

class Components():
    def __init__(self):
        self.components = {}
        self.COMPONENT_FILE = None
        self.set_component_file()
        self.set_components()
        self.print_components()

    def set_component_file(self):
        self.COMPONENT_FILE = "../input_files/components.csv"

    def set_components(self):
        with open(self.COMPONENT_FILE, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                component = CreateComponent(row[0],row[1:])
                self.components[component.name] = component.signals

    def print_components(self):
        print(self.components)

Components()
