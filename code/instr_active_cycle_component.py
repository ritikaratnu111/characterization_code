class ISA():

    def __init__(self):
        self.Dict = {'route': [],
                        'sram':[],
                        'refi':[]}
        self.set_route(1)
        self.set_sram(1)
        self.set_refi(6,0,0)
#        self.print_instr_attributes()
#        self.print_instr_active_components()
#        self.print_instr_active_component_cycles()

    def set_route(self, no_of_hops):
        self.Dict['route'] = [['no_of_hops'],['sequencer','noc'],[['sequencer',1], ['noc', 1 + int(no_of_hops) + 1 ]]]         

    def set_sram(self, no_of_hops):
        self.Dict['sram'] = [['no_hops'],['sequencer','dimarch_agu','SRAM','dimarch'],[['sequencer',1], ['wait',1], ['dimarch_agu',2], ['SRAM',2], ['dimarch', 1 + int(no_of_hops) + 1]]] 

    def set_refi(self, init_delay, l1_iter, l2_iter):
        self.Dict['refi'] = [["init_delay","l1_iter","l2_iter"],['sequencer','regfile_agu','reg_file'],[['sequencer',1], ['regfile_agu',2], ['wait',int(init_delay)-2], ['reg_file', 1 + int(l1_iter)*int(l2_iter) + 1]]]  

    def print_instr_attributes(self):
        for key,value in self.Dict.items():
            print(key, value[0])

    def print_instr_active_components(self):
        for key,value in self.Dict.items():
            print(key, value[1])

    def print_instr_active_component_cycles(self):
        for key,value in self.Dict.items():
            print(key, value[2])

    def get_attributes(self,instr):
        return(self.Dict[instr][0])

    def get_active_components(self,instr):
        return(self.Dict[instr][1])

    def get_active_component_cycles(self,instr):
        return(self.Dict[instr][2])
ISA()
