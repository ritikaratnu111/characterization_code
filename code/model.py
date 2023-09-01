#This class interprets the instruction read by assembly
from ISA import ISA

class Model():

    def __init__(self):
        self.ISA = ISA()

    def set_active_cycles_route(self,start):
        offset = start
        self.active_cycles['ROUTE'] = {
            'sequencer': {'start': 0, 'end': 0},
            'dimarch': {'start': 0, 'end': 0},
            'dimarch_wrap': {'start': 0, 'end': 0},
            'dimarch_rest': {'start': 0, 'end': 0},
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['ROUTE']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }
        noc_end = sequencer_end + 1 * self.CLOCK_PERIOD + (self.segment_values['ROUTE']['horizontal_hops'] 
                + self.segment_values['ROUTE']['vertical_hops']) * self.CLOCK_PERIOD + 1 * self.CLOCK_PERIOD
        self.active_cycles['ROUTE']['noc'] = {
            'start': start,
            'end': noc_end
        }
        dimarch_start = start + (self.segment_values['ROUTE']['horizontal_hops'] + self.segment_values['ROUTE']['vertical_hops']) * self.CLOCK_PERIOD
        dimarch_end = dimarch_start + 8 * self.CLOCK_PERIOD
        self.active_cycles['ROUTE']['dimarch'] = {
            'start': dimarch_start,
            'end': dimarch_end
        }
        self.active_cycles['ROUTE']['dimarch_wrap'] = {
            'start': dimarch_start,
            'end': dimarch_end
        }
        self.active_cycles['ROUTE']['dimarch_rest'] = {
            'start': dimarch_start,
            'end': dimarch_start + 4 * self.CLOCK_PERIOD
        }

    def set_active_cycles_sram(self,start):        
        offset = start
        self.active_cycles['SRAM'] = {
            'sequencer': {'start': 0, 'end': 0},
            'wait': {'start': 0, 'end': 0},
            'dimarch_agu': {'start': 0, 'end': 0},
            'sram': {'start': 0, 'end': 0}
#            'dimarch': {'start': 0, 'end': 0}
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['SRAM']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }
        offset = sequencer_end
        wait_end = sequencer_end + (self.segment_values['SRAM']['hops'] + 1) * self.CLOCK_PERIOD
        self.active_cycles['SRAM']['wait'] = {
            'start': offset,
            'end': wait_end
        }
        offset = wait_end
        dimarch_agu_end = offset + 3 * self.CLOCK_PERIOD
        self.active_cycles['SRAM']['dimarch_agu'] = {
            'start': offset,
            'end': dimarch_agu_end
        }
        offset = wait_end + 1 * self.CLOCK_PERIOD
        sram_end = offset + 2 * self.CLOCK_PERIOD
        self.active_cycles['SRAM']['sram'] = {
            'start': offset,
            'end': sram_end
        }
        offset = sram_end
#        dimarch_end = offset + (self.segment_values['SRAM']['hops'] ) * self.CLOCK_PERIOD + 2 * self.CLOCK_PERIOD 
#        self.active_cycles['SRAM']['dimarch'] = {
#            'start': wait_end,
#            'end': dimarch_end
#        }

    def set_active_cycles_refi(self,start):        
        offset = start
        self.active_cycles['REFI'] = {
            'sequencer': {'start': 0, 'end': 0},
            'wait': {'start': 0, 'end': 0},
 #           'regfile_agu': {'start': 0, 'end': 0},
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
#        regfile_agu_end = offset  + 2 * self.CLOCK_PERIOD
#        self.active_cycles['REFI']['regfile_agu'] = {
#            'start': offset,
#            'end': regfile_agu_end
#        }
#        offset = wait_end + 1 * self.CLOCK_PERIOD
        regfile_end = offset + self.segment_values['REFI']['l1_iter'] * self.segment_values['REFI']['l2_iter'] * self.CLOCK_PERIOD  + 4 * self.CLOCK_PERIOD

        self.active_cycles['REFI']['regfile'] = {
            'start': start,
            'end': regfile_end
        }

    def set_active_cycles_raccu(self,start):
        offset = start
        self.active_cycles['RACCU'] = {
            'sequencer': {'start': 0, 'end': 0},
            'raccu': {'start': 0, 'end': 0},
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['RACCU']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }
        offset = sequencer_end
        raccu_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['RACCU']['raccu'] = {
            'start': offset,
            'end': raccu_end
        }

    def set_active_cycles_dpu(self,start):
        offset = start
        self.active_cycles['DPU'] = {
            'sequencer': {'start': 0, 'end': 0},
            'dpu': {'start': 0, 'end': 0},
            'swb': {'start': 0, 'end': 0}
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['DPU']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }
        offset = sequencer_end
        self.active_cycles['DPU']['dpu'] = {
            'start': start,
            'end': start + 1 * self.CLOCK_PERIOD
        }

    def set_active_cycles_loop(self,start):
        offset = start
        self.active_cycles['LOOP'] = {
            'sequencer': {'start': 0, 'end': 0},
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['LOOP']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }

    def set_active_cycles_swb(self,start):
        offset = start
        self.active_cycles['SWB'] = {
            'sequencer': {'start': 0, 'end': 0},
            'swb': {'start': 0, 'end': 0},
        }
        sequencer_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['SWB']['sequencer'] = {
            'start': offset,
            'end': sequencer_end
        }
        offset = sequencer_end
        swb_end = offset + 1 * self.CLOCK_PERIOD
        self.active_cycles['SWB']['swb'] = {
            'start': offset,
            'end': swb_end
        }

    def set_active_cycles_wait(self,start):        
        offset = start
        self.active_cycles['WAIT'] = {
            'sequencer': {'start': 0, 'end': 0},
        }
        sequencer_end = offset + self.segment_values['WAIT']['cycle'] * self.CLOCK_PERIOD + 1 * self.CLOCK_PERIOD

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
        elif (instr['name'] == 'RACCU'):
            self.set_active_cycles_raccu(start)
        elif (instr['name'] == 'DPU'):
            self.set_active_cycles_dpu(start)
        elif (instr['name'] == 'LOOP'):
            self.set_active_cycles_loop(start)
        elif (instr['name'] == 'SWB'):
            self.set_active_cycles_swb(start)
        elif (instr['name'] == 'HALT'):
            self.set_active_cycles_halt(start)