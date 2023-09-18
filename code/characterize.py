import os
import logging
import random
import constants
from openpyxl import Workbook
from simulation import Simulation

class Characterize():
	
	def __init__(self, tb, cells):     
		self.tb = tb
		os.environ['VCD_DIR'] ='./vcd/'
		os.chdir(tb)
		os.makedirs("vcd", exist_ok=True)
		self.cells = cells

	def run_simulation(self, window, i):
		start = window['start']
		end = window['end']
		for cell in self.cells:
			Simulation.trigger_vsim(i, start, end, False, False, None, cell.tile, None)
			Simulation.trigger_innovus(i, start, end, False, None, None, None, None)

	def run_simulation_per_component(self, i):
		for cell in self.cells:
			for component in cell.active_components.active_components:
				print(component.name)
				tile =component.signals[0].split('*')[0]
				for window in component.active: 
					state = "active"
					Simulation.trigger_vsim(i, window['start'], window['end'], False, True, state, tile, component.name)
					Simulation.trigger_innovus(i, start, end, False, True, state, tile, component.name)
				for window in component.inactive: 
					state = "inactive"
					Simulation.trigger_vsim(i, window['start'], window['end'], False, True, state, tile, component.name)
					Simulation.trigger_innovus(i, window['start'], window['end'], False, True, state, tile, component.name)

	def run_simulation_per_cycle(self):
		window = self.cells[0].total_window
		Simulation.trigger_vsim(0, window['start'], window['end'],  True, None, None, None, None)
		Simulation.trigger_innovus(0, window['start'], window['end'],  True, None, None, None, None)

	def run_randomized_simulation(self,count):
		print("Running randomized simulation")    
		Simulation.generate_randomized_mem_init_files(count)
		for i in range(count):
			Simulation.update_mem_init_file(self.tb,i)
			self.run_simulation(self.assembly.window,i)
			self.run_simulation_per_component(i)

	def get_per_cycle_power(self):
		print("Getting per cycle power")
		for cell in self.cells:
			for component in cell.components.active:
				print(component.name)
				print(component.active_window)
				component.init_profiler()
				component.set_per_cycle_power()
#				component.set_active_power(component.signals)
#				component.set_inactive_power(component.signals)

#	def get_active_component_active_energy(self):
#		print("Getting active component active energy")
#		self.energy.set_active_component_active_energy()
#
#	def get_active_component_inactive_energy(self):
#		print("Getting active component inactive energy")
#		self.energy.set_active_component_inactive_energy()
#
#	def get_inactive_component_energy(self):
#		print("Getting inactive component energy")
#		self.energy.set_inactive_component_energy()

	def write_db(self):
		print("Writing to database")
		experiment_names = ["Experiment 1", "Experiment 2", "Experiment 3"]
		component_names = ["Component 1", "Component 2", "Component 3"]
		power_types = ["Active Power", "Inactive Power"]
		sub_types = ["Internal", "Switching", "Leakage"]

		wb = Workbook()
		sheet = wb.active

		header_row = ["Experiment"]
		for component in component_names:
			for power_type in power_types:
				for sub_type in sub_types:
					header_row.append(f"{component} {power_type} {sub_type}")
		sheet.append(header_row)

		for experiment in experiment_names:	
			row = [experiment]
			for component in component_names:
				for power_type in power_types:
					for sub_type in sub_types:
						row.append(self.energy.get_power(component, power_type, sub_type))
			sheet.append(row)

		Workbook.save(wb, filename = f"{self.tb}_energy.xlsx")		

	def log(self):
		print("Logging")