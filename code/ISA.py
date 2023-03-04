class ISA():

    def __init__(self):

        self.attributes = {}
        self.components = {}
        self.active_cycles = {}
        self.set_ISA()
#        self.set_route(1)
#        self.set_sram(1)
#        self.set_refi(6,0,0)
#        self.print_instr_attributes()
#        self.print_instr_active_components()
#        self.print_instr_active_component_cycles()

    def set_attributes(self):
        self.attributes['route'] = {'instr_delay': 0,'no_of_hops' : 1}
        self.attributes['sram'] = {'instr_delay': 0,'no_of_hops' : 1}
        self.attributes['refi'] = {'instr_delay': 0,'init_delay' : 6, 'l1_iter' : 0, 'l2_iter' : 0}

    def set_components(self):
        self.components['route'] = {'sequencer' : ['seq_gen'] ,'noc' : ['noc', 'partition', 'splitter'] }
        self.components['sram'] = {'sequencer' : ['seq_gen'] ,'dimarch_agu' : ['DiMArch*AGU'] ,'SRAM' : ['SRAM'] ,'dimarch' : ['DiMArch']}
        self.components['refi'] = {'sequencer' : ['seq_gen'] ,'regfile_agu' : ['reg_top*addr'],'reg_file' : ['reg_top']}

    def set_active_cycles(self):
        start = self.attributes['route']['instr_delay']
        self.active_cycles['route'] = {'sequencer':{'start': 0,'end': 0},
                                        'noc': {'start': 0,'end': 0} }
        self.active_cycles['route']['sequencer'] = {'start': start,'end': start + 1}
        self.active_cycles['route']['noc'] =  {'start': start + 1, 'end': start + 1 + self.attributes['route']['no_of_hops'] + 1 }

        self.active_cycles['sram'] = {'sequencer':{'start': 0,'end': 0},
                                        'wait': {'start': 0,'end': 0},
                                        'dimarch_agu': {'start': 0,'end': 0},
                                        'sram': {'start': 0,'end': 0},
                                        'dimarch': {'start': 0,'end': 0}}
        start = self.attributes['sram']['instr_delay']
        self.active_cycles['sram']['sequencer'] = {'start': start,'end': start + 1}
        self.active_cycles['sram']['wait'] =  {'start': start + 1, 'end':start + 2}
        self.active_cycles['sram']['dimarch_agu'] =  {'start': start + 2, 'end':start + 4}
        self.active_cycles['sram']['sram'] =  {'start': start + 4, 'end':start + 6}
        self.active_cycles['sram']['dimarch'] =  {'start': start + 6, 'end':start + 6 + self.attributes['sram']['no_of_hops'] + 2 }

        self.active_cycles['refi'] = {'sequencer':{'start': 0,'end': 0},
                                        'regfile_agu': {'start': 0,'end': 0},
                                        'wait': {'start': 0,'end': 0},
                                        'reg_file': {'start': 0,'end': 0}}
        start = self.attributes['refi']['instr_delay']
        self.active_cycles['refi']['sequencer'] = {'start': start,'end': start + 1}
        self.active_cycles['refi']['regfile_agu'] = {'start': start + 1,'end': start + 3}
        self.active_cycles['refi']['wait'] = {'start': start + 3,'end': start + 3 + self.attributes['refi']['init_delay'] -2 }
        self.active_cycles['refi']['reg_file'] = {'start':start + 3 + self.attributes['refi']['init_delay'] -2,'end': start + 3 + self.attributes['refi']['init_delay'] -2 + 1 + self.attributes['refi']['l1_iter'] * self.attributes['refi']['l2_iter'] + 1} 

    def set_ISA(self):
        #Here we read the ISA file and find the instructions, their attributes, typical value of the attributes, their active components, cycle model.
        #In this function, we set the attributes to their typical values. But later, when assembly is read, we need to return the specific dictionary instruction item with the value from the assembly file.
        #All of the below hard code will be removed, then  we will do:
#        name = "route"
#        attribute = no_of_hops,...
#        components = sequencer, noc, ...
#        active_cycles = [sequencer, ...], [noc, ...]
#        self.Dict[name] = [atributes, components, active_cycles]
        self.set_attributes()
        self.set_components()
        self.set_active_cycles()

    def print_ISA(self):
        for key,value in self.attributes.items():
            print(key, value)

ISA()
