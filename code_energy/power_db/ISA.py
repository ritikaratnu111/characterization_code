class ISA():

    CLOCK_PERIOD = 12

    def __init__(self):

        self.segment_values = {}
        self.components = {}
        self.active_cycles = {}
        self.set_ISA()

    def init_segment_values(self):
#        self.segment_values['route'] = {'instr_delay': 0,'no_of_hops' : 1}
#        self.segment_values['sram'] = {'instr_delay': 0,'no_of_hops' : 1}
#        self.segment_values['refi'] = {'instr_delay': 0,'init_delay' : 6, 'l1_iter' : 0, 'l2_iter' : 0}

# segment_values is the segment values of each instruction
        self.segment_values = {
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
            },
            'WAIT' : {
                'cycle': 0,
                'cycle_sd': 0
            },
            'HALT' : {
            }
        }

    def set_segment_values(self,instr):
        for attribute in self.segment_values[instr['name']]:
            self.segment_values[instr['name']][attribute]  = instr['segment_values'][attribute]


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
                'regfile': ['reg_top']
            },
            'WAIT': {
                'sequencer' : ['seq_gen']
            },
            'HALT': {
                'sequencer' : ['seq_gen']
            }
        }

    def get_components(self,instr_name):
        return self.components[instr_name]

    def set_active_cycles_route(self,start):
        offset = start
        self.active_cycles['ROUTE'] = {
            'sequencer': {'start': 0, 'end': 0},
            'noc': {'start': 0, 'end': 0}
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['ROUTE']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }
        offset = sequencer_end
        noc_end = offset + 1 * self.CLOCK_PERIOD + (self.segment_values['ROUTE']['horizontal_hops'] + self.segment_values['ROUTE']['vertical_hops']) * self.CLOCK_PERIOD + 1 * self.CLOCK_PERIOD
        self.active_cycles['ROUTE']['noc'] = {
            'start': offset,
            'end': noc_end
        }

    def set_active_cycles_sram(self,start):        
        offset = start
        self.active_cycles['SRAM'] = {
            'sequencer': {'start': 0, 'end': 0},
            'wait': {'start': 0, 'end': 0},
            'dimarch_agu': {'start': 0, 'end': 0},
            'sram': {'start': 0, 'end': 0},
            'dimarch': {'start': 0, 'end': 0}
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['SRAM']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }
        offset = sequencer_end
        wait_end = offset + self.segment_values['SRAM']['hops'] * self.CLOCK_PERIOD
        self.active_cycles['SRAM']['wait'] = {
            'start': offset,
            'end': wait_end
        }
        offset = wait_end
        dimarch_agu_end = offset + 2 * self.CLOCK_PERIOD
        self.active_cycles['SRAM']['dimarch_agu'] = {
            'start': offset,
            'end': dimarch_agu_end
        }
        offset = dimarch_agu_end
        sram_end = offset + 2 * self.CLOCK_PERIOD
        self.active_cycles['SRAM']['sram'] = {
            'start': offset,
            'end': sram_end
        }
        offset = sram_end
        dimarch_end = offset + (self.segment_values['SRAM']['hops'] + 1 ) * self.CLOCK_PERIOD + 1 * self.CLOCK_PERIOD
        self.active_cycles['SRAM']['dimarch'] = {
            'start': offset,
            'end': dimarch_end
        }

    def set_active_cycles_refi(self,start):        
        offset = start
        self.active_cycles['REFI'] = {
            'sequencer': {'start': 0, 'end': 0},
            'wait': {'start': 0, 'end': 0},
            'regfile_agu': {'start': 0, 'end': 0},
            'reg_file': {'start': 0, 'end': 0},
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD

        self.active_cycles['REFI']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }
        offset = sequencer_end

        wait_end = offset + self.segment_values['REFI']['init_delay'] * self.CLOCK_PERIOD -3 * self.CLOCK_PERIOD
        self.active_cycles['REFI']['wait'] = {
            'start': offset,
            'end': wait_end
        }
        offset = wait_end
        regfile_agu_end = offset  + 2 * self.CLOCK_PERIOD
        self.active_cycles['REFI']['regfile_agu'] = {
            'start': offset,
            'end': regfile_agu_end
        }
        offset = wait_end + 1 * self.CLOCK_PERIOD
        regfile_end = offset + self.segment_values['REFI']['l1_iter'] * self.segment_values['REFI']['l2_iter'] * self.CLOCK_PERIOD  + 1 * self.CLOCK_PERIOD

        self.active_cycles['REFI']['regfile'] = {
            'start': offset,
            'end': regfile_end
        }

    def set_active_cycles_wait(self,start):        
        offset = start
        self.active_cycles['WAIT'] = {
            'sequencer': {'start': 0, 'end': 0},
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD

        self.active_cycles['WAIT']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }

    def set_active_cycles_halt(self,start):        
        offset = start
        self.active_cycles['HALT'] = {
            'sequencer': {'start': 0, 'end': 0},
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD

        self.active_cycles['HALT']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }

    def set_active_cycles(self,instr,start):
        if (instr['name'] == 'ROUTE'):
            self.set_active_cycles_route(start)
        elif (instr['name'] == 'SRAM'): 
            self.set_active_cycles_sram(start)
        elif (instr['name'] == 'REFI'):
            self.set_active_cycles_refi(start)
        elif (instr['name'] == 'WAIT'):
            self.set_active_cycles_wait(start)
        elif (instr['name'] == 'HALT'):
            self.set_active_cycles_halt(start)

    def get_active_cycles(self, instr):
        start = instr['start_time'] 
        self.set_segment_values(instr)
        self.set_active_cycles(instr,start)
        return self.active_cycles[instr['name']]

                

    def set_ISA(self):
        #Here we read the ISA file and find the instructions, their segment_values, typical value of the segment_values, their active components, cycle model.
        #In this function, we set the segment_values to their typical values. But later, when assembly is read, we need to return the specific dictionary instruction item with the value from the assembly file.
        #All of the below hard code will be removed, then  we will do:
#        name = "route"
#        attribute = no_of_hops,...
#        components = sequencer, noc, ...
#        active_cycles = [sequencer, ...], [noc, ...]
#        self.Dict[name] = [atributes, components, active_cycles]
        self.init_segment_values()
        self.set_components()

    def print_ISA(self):
        for key,value in self.segment_values.items():
            print(key, value)

ISA()
