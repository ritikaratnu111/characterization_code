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
		self.count = 0

	def run_simulation(self, window, i):
		start = window['start']
		end = window['end']
		for cell in self.cells:
			Simulation.trigger_vsim(i, start, end, False, False, None, cell.tile, None)
			Simulation.trigger_innovus(i, start, end, False, None, None, None, None)

	def run_simulation_per_component(self, i):
		for cell in self.cells:
			for component in cell.components.active:
				print(component.name)
				tile =component.signals[0].split('*')[0]
				for window in component.active_window: 
					state = "active"
					Simulation.trigger_vsim(i, window['start'], window['end'], False, True, state, tile, component.name)
					Simulation.trigger_innovus(i, window['start'], window['end'], False, True, state, tile, component.name)
				for window in component.inactive_window: 
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
			print(i)
			#Simulation.update_mem_init_file(self.tb,i)
			for cell in self.cells:
				self.run_simulation(cell.total_window,i)
				#self.run_simulation_per_component(i)

	def get_per_cycle_power(self):
		print("Getting per cycle power")
		for cell in self.cells:
			for component in cell.components.active:
				print(component.name)
				logging.info("Setting per_cycle power for %s", component.name)
				component.set_per_cycle_power()

	def get_active_AEC_power(self):
		print("Getting active component active energy")
		for cell in self.cells:
			for component in cell.components.active:
				print(component.name)
				logging.info("Setting active power for %s", component.name)
				component.set_active_power(0)
#
	def get_inactive_AEC_power(self):
		print("Getting active component inactive energy")
		for cell in self.cells:
			for component in cell.components.active:
				print(component.name)
				logging.info("Setting inactive power for %s", component.name)
				component.set_inactive_power(0)

	def get_active_AEC_energy(self):
		print("Getting active component active energy")
		for cell in self.cells:
			for component in cell.components.active:
				print(component.name)
				logging.info("Setting active energy for %s", component.name)
				component.set_active_energy(0)

	def get_inactive_AEC_energy(self):
		print("Getting active component inactive energy")
		for cell in self.cells:
			for component in cell.components.active:
				print(component.name)
				logging.info("Setting inactive energy for %s", component.name)
				component.set_inactive_energy(0)		
	
	def get_remaining_power(self):
		print("Getting remaining power")
		for cell in self.cells:
			cell.set_remaining_power(0)
                        
	def get_total_power(self):
		print("Getting total power")
		for cell in self.cells:
			cell.set_total_power(0)
	    
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
