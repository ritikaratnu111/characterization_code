import constants
from instr import Instr
import logging 
import copy

class Assembly():
    def __init__(self,row=None, col=None):
        self.instructions = []
        self.window = {}
        self.loop_instr = {}
        self.gloabal_start = 0
        self.row = row if row is not None else 0
        self.col = col if col is not None else 0

    def set_ISA(self,ISA):
        self.ISA = ISA

    def set_hop_cycles(self, row, col):
        self.row = row
        self.col = col
        self.hop_cycles = (self.row + self.col) * constants.CLOCK_PERIOD
        logging.info(f"hop cycles: {self.hop_cycles}")

    def set_window(self,window):
        self.window['start'] = window['start'] + self.hop_cycles
        self.window['end'] = window['end'] + self.hop_cycles
        self.global_start = window['start']
        logging.info(f"Assembly window: {self.window}")

    def add_instr(self, instr):
        instr_offset = instr['start'] * constants.CLOCK_PERIOD
        new_instr = Instr(instr['start'],
                            instr['name'],
                            self.global_start + instr_offset,
                            None,
                            instr['segment_values'],
                            None)
        self.instructions.append(new_instr)

    def set_assembly(self,instructions):
        for instr in instructions:
            self.add_instr(instr)

    def set_pc(self):
        for idx, instr in enumerate(self.instructions):
            if (idx == 0):
                prev_instr = instr
            else:
                instr.set_pc(self.ISA,prev_instr)
                prev_instr = instr

    def set_delay_for_dpu_swb(self):
        all_dpu_id = []
        from_different_cell = 0
        for idx, instr in enumerate(self.instructions):
            if (instr.name == 'DPU'):
                all_dpu_id.append(instr.id)
            elif (instr.name == 'SWB'):
                if(instr.segment_values['send_to_other_row'] == 1):
                    from_different_cell = 1

        for dpu_id in all_dpu_id:
            delay = 0
            print(f"dpu_id: {dpu_id}")
            for idx,instr in enumerate(self.instructions):
                if (instr.id < dpu_id and instr.name == 'REFI'):
                    if(instr.segment_values['port_no'] == 2 or instr.segment_values['port_no'] == 3):
                        l1_iter = instr.segment_values['l1_iter']
                        l2_iter = instr.segment_values['l2_iter']
                        l1_delay = instr.segment_values['l1_delay']
                        l2_delay = instr.segment_values['l2_delay']
                        init_delay = instr.segment_values['init_delay']
                        print(f"instr.id {instr.id} l1_iter: {l1_iter}, l2_iter: {l2_iter}, l1_delay: {l1_delay}, l2_delay: {l2_delay}, init_delay: {init_delay}")
                        delay_current = (l2_iter + 1) * (l1_iter + 1 + l1_iter * l1_delay) + (l2_iter * l2_delay) 
                        print(f"delay_current: {delay_current}")
                        if delay < delay_current:
                            delay = delay_current
            
            for idx,instr in enumerate(self.instructions):
                if instr.id == dpu_id:
                    instr.segment_values['dpu_delay'] = delay
                    if(from_different_cell == 1):
                        instr.segment_values['swb_delay'] = delay
                    else:
                        instr.segment_values['swb_delay'] = -2


    def adjust_swb(self):

        for idx, instr in enumerate(self.instructions):
            if( instr.name == 'SWB'):
                instr.segment_values['first'] = 1

    def identify_loop_instructions(self):
        for idx, instr in enumerate(self.instructions):
            if (instr.name == 'LOOP'):
                loop_instr_pc = instr.pc
                startpc = instr.pc + 1
                endpc = instr.segment_values['endpc']
                start = 0
                end = 0
                iter = instr.segment_values['iter']
                repeating_instructions = []
                for idx1, instr in enumerate(self.instructions):
                    if (instr.pc< startpc):
                        continue
                    elif (instr.pc == startpc):    
                        start = instr.start
                        repeating_instructions.append(instr)
                    elif (instr.pc <= endpc):
                        repeating_instructions.append(instr)
                    else:
                        if (end == 0):
                            end = instr.start
                no_of_instructions = len(repeating_instructions)
                self.instructions[idx + 1].segment_values["no_of_loop_instructions"] = no_of_instructions
                
                self.loop_instr[loop_instr_pc] = {"startpc": startpc, 
                                                  "endpc": endpc, 
                                                  "iter": iter, 
                                                  "repeating_instructions": repeating_instructions,
                                                  "no_of_instructions": no_of_instructions,
                                                  "unrolled_instructions": [],
                                                  "start" : start,
                                                  "end" : end,
                                                  "total" : end - start }
            else:
                if(idx < len(self.instructions) - 2):
                    self.instructions[idx + 1].segment_values["no_of_loop_instructions"] = 0

    def unroll_loop_instructions(self):
        #This function will unroll the loop instructions iter times and update the start times of the instructions accordingly
        for loop_instr_pc, loop_info in self.loop_instr.items():
            i = 0
            iter = loop_info['iter']
            unrolled_instr = []
            end = 0
            while (i < iter):     
                for instr in loop_info['repeating_instructions']:
                    segment_values = copy.deepcopy(instr.segment_values)
                    if(instr.name == 'SWB'):
                        segment_values['first'] = 0
                    modified_instr = Instr(
                                    instr.id,
                                    instr.name,
                                    instr.start + i* loop_info['total'],
                                    instr.pc,
                                    segment_values,
                                    None)
                    unrolled_instr.append(modified_instr)
                i = i + 1

            loop_info['unrolled_instructions'] = unrolled_instr
            loop_info['end'] = loop_info["start"] + iter * loop_info['total']
            loop_info['total'] = loop_info['total']

    def fit_loop_instructions(self):
        if (self.loop_instr):
            for loop_instr_pc, loop_info in self.loop_instr.items():
                startpc = loop_info['startpc']
                endpc = loop_info['endpc']
                start_idx = 0
                end_idx = 0
                iter = loop_info['iter']
                loop_instructions = loop_info['unrolled_instructions']
                for idx, instr in enumerate(self.instructions):
                    if (instr.pc < startpc):
                        continue
                    elif (instr.pc == startpc):
                        start_idx = idx
                    elif (instr.pc == endpc):
                        end_idx = idx
                    else:
                        instr.start = instr.start + (iter - 1) * loop_info['total']
                        #print(instr.name, loop_info['end'], instr.start)
                self.instructions = self.instructions[:start_idx] + loop_instructions + self.instructions[end_idx + 1:]


    def unroll_loop(self):
        self.identify_loop_instructions()
        self.unroll_loop_instructions()
        self.fit_loop_instructions()

    def set_dependent_segment_values(self):
        for idx, instr in enumerate(self.instructions):
            if(instr.name == 'LOOP'):
                endpc = instr.segment_values['endpc']

    def add_assembly(self, assembly):
        if (assembly):
            for instr in assembly:
                self.add_instr(instr, self.window)

    def set_instr_active_components(self,row,col):
        for idx,instr in enumerate(self.instructions):
            instr.set_components(row,col,self.ISA)

    def set_instr_active_component_cycles(self):
        for idx,instr in enumerate(self.instructions):
            instr.set_active_cycles(self.ISA)

    def modify_cycles_of_dependent_instructions(self):
        for idx, instr in enumerate(self.instructions):
            if(instr.name == 'DPU'):
                dpu_end = instr.components.active[1].active_window['end']
#                wait_cycles = self.instructions[idx + 1].segment_values['cycle']
                wait_cycles = 9
                wait_time = wait_cycles * constants.CLOCK_PERIOD
                for component in instr.components.active:
                    if component.name == 'dpu':
                        component.active_window['end'] = dpu_end + wait_time
                    elif component.name == 'swb':
                        component.active_window['start'] = dpu_end
                        component.active_window['end'] = dpu_end + wait_time


    def print(self):
        for instr in self.instructions:
            instr.print()
