class ISA():

    CLOCK_PERIOD = 12

    def __init__(self):

        self.attributes = {}
        self.components = {}
        self.active_cycles = {}
        self.set_ISA()

    def set_active_cycles(self,start):
        offset = start
        self.active_cycles['ROUTE'] = {'sequencer':{'start': 0,'end': 0},
                                        'noc': {'start': 0,'end': 0} }
        self.active_cycles['ROUTE']['sequencer'] = {'start': offset,'end': offset + 1 * self.clock_period}
        offset = self.active_cycles['ROUTE']['sequencer']['end']
        self.active_cycles['ROUTE']['noc'] =  {'start': offset, 'end': offset + 1 * self.clock_period + (self.attributes['ROUTE']['horizontal_hops'] + self.attributes['ROUTE']['vertical_hops']) * self.clock_period  + 1 * self.clock_period  }

        self.active_cycles['SRAM'] = {'sequencer':{'start': 0,'end': 0},
                                        'wait': {'start': 0,'end': 0},
                                        'dimarch_agu': {'start': 0,'end': 0},
                                        'sram': {'start': 0,'end': 0},
                                        'dimarch': {'start': 0,'end': 0}}
        self.active_cycles['SRAM']['sequencer'] = {'start': offset,'end': offset + 1 * self.clock_period }
        offset = self.active_cycles['SRAM']['sequencer']['end']
        self.active_cycles['SRAM']['wait'] =  {'start': offset , 'end': offset + self.attributes['SRAM']['hops'] * self.clock_period}
        offset = self.active_cycles['SRAM']['wait']['end']
        self.active_cycles['SRAM']['dimarch_agu'] =  {'start': offset , 'end':offset + 2 * self.clock_period }
        offset = self.active_cycles['SRAM']['dimarch_agu']['end']
        self.active_cycles['SRAM']['SRAM'] =  {'start': offset , 'end':offset + 2 * self.clock_period }
        offset = start
        self.active_cycles['SRAM']['dimarch'] =  {'start': offset , 'end':offset  + self.attributes['SRAM']['hops'] * self.clock_period  + 1 * self.clock_period  }

        self.active_cycles['REFI'] = {'sequencer':{'start': 0,'end': 0},
                                        'wait': {'start': 0,'end': 0},
                                        'regfile_agu': {'start': 0,'end': 0},
                                        'reg_file': {'start': 0,'end': 0}}
        self.active_cycles['REFI']['sequencer'] = {'offset': offset,'end': offset + 1 * self.clock_period }
        offset = self.active_cycles['REFI']['sequencer']['end']
        self.active_cycles['REFI']['wait'] = {'start': offset ,'end': offset  + self.attributes['REFI']['init_delay'] * self.clock_period  -3 * self.clock_period  }
        offset = self.active_cycles['REFI']['wait']['end']
        self.active_cycles['REFI']['regfile_agu'] = {'start': offset ,'end': offset  + 2 * self.clock_period }
        offset = self.active_cycles['REFI']['regfile_agu']['end']
        self.active_cycles['REFI']['reg_file'] = {'start': offset - 1 * self.clock_period ,'end': start + 1 * self.clock_period  + self.attributes['REFI']['init_delay'] * self.clock_period  -3 * self.clock_period  + 1 * self.clock_period  + self.attributes['REFI']['l1_iter'] * self.attributes['REFI']['l2_iter'] * self.clock_period  + 1 * self.clock_period } 
    def set_attributes(self):
#        self.attributes['route'] = {'instr_delay': 0,'no_of_hops' : 1}
#        self.attributes['sram'] = {'instr_delay': 0,'no_of_hops' : 1}
#        self.attributes['refi'] = {'instr_delay': 0,'init_delay' : 6, 'l1_iter' : 0, 'l2_iter' : 0}

# Attributes is the segment values of each instruction
        self.attributes = {
            'ROUTE': {
                'direction': 0,
                'horizontal_dir': 1,
                'horizontal_hops': 0,
                'select_drra_row': 0,
                'vertical_dir': 0,
                'vertical_hops': 0
            },
            'SRAM': {
                'hops': 0,
                'init_addr': 0,
                'init_addr_sd': 0,
                'init_delay': 0,
                'init_delay_sd': 0,
                'l1_delay': 0,
                'l1_delay_sd': 0,
                'l1_iter': 0,
                'l1_iter_sd': 0,
                'l1_step': 0,
                'l1_step_sd': 0,
                'l2_delay': 0,
                'l2_delay_sd': 0,
                'l2_iter': 0,
                'l2_iter_sd': 0,
                'l2_step': 0,
                'l2_step_sd': 0,
                'rw': 0
            },
            'REFI': {
                'compress': 0,
                'dimarch': 1,
                'extra': 2,
                'init_addr': 0,
                'init_addr_sd': 0,
                'init_delay': 4,
                'init_delay_sd': 0,
                'l1_delay': 0,
                'l1_delay_ext': 0,
                'l1_delay_sd': 0,
                'l1_iter': 0,
                'l1_iter_sd': 0,
                'l1_step': 1,
                'l1_step_sd': 0,
                'l1_step_sign': 0,
                'l2_delay': 0,
                'l2_delay_sd': 0,
                'l2_iter': 0,
                'l2_iter_ext': 0,
                'l2_iter_sd': 0,
                'l2_step': 0,
                'l2_step_ext': 0,
                'port_no': 0,
                'unused_0': 2,
                'unused_1': 3,
                'unused_2': 0,
                'unused_3': 0
            }
        }



    def set_components(self):
        self.components = {
            'ROUTE': {
                'sequencer': ['seq_gen'],
                'noc': ['noc', 'partition', 'splitter']
            },
            'SRAM': {
                'sequencer': ['seq_gen'],
                'dimarch_agu': ['DiMArch*AGU'],
                'SRAM': ['SRAM'],
                'dimarch': ['DiMArch']
            },
            'REFI': {
                'sequencer': ['seq_gen'],
                'regfile_agu': ['reg_top*addr'],
                'reg_file': ['reg_top']
            },
            'WAIT': {
            },
            'HALT': {
            }
        }

    def get_components(self,instr_name):
        return self.components[instr_name]


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
        self.set_active_cycles(0)

    def print_ISA(self):
        for key,value in self.attributes.items():
            print(key, value)

ISA()
