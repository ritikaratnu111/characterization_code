import os
import re
import random

CLOCK_PERIOD = 12
HALF_PERIOD = 6


class VesylaOutput():
    # Write a function to change the clock_period from 10NS to CLOCK_PERIOD and half_period from 5NS to HALF_PERIOD
    def update_clock_period(tb):

        PACKAGE_FILE = f"{tb}/const_package.vhd"

        with open(PACKAGE_FILE) as file:
            contents = file.read()
            # Check if the clock period is 10NS
            file_clock_period = int(
                re.search(
                "CONSTANT period\s+:\s+time\s+:=\s+(\d+)\s+NS;",
                contents,
                ).group(1)
            )
            # Replace the old values with the new values if file_clock_period is not the same as self.CLOCK_PERIOD
            if(file_clock_period != CLOCK_PERIOD):
                updated_contents = contents.replace("CONSTANT period                 : time    := 10 NS;",
                                                 f"CONSTANT period                 : time    := {self.CLOCK_PERIOD} NS;")
                updated_contents = updated_contents.replace("CONSTANT half_period            : time    := 5 NS;",
                                                         f"CONSTANT half_period            : time    := {self.HALF_PERIOD} NS;")

            # Write the updated contents back to the file
                with open(PACKAGE_FILE, "w") as file:
                    file.write(updated_contents)
            file_clock_period = int(
                re.search(
                "CONSTANT period\s+:\s+time\s+:=\s+(\d+)\s+NS;",
                contents,
                ).group(1)
            )

    def return_execution_cycle(tb):
        PACKAGE_FILE = f"{tb}/const_package.vhd"
        with open(PACKAGE_FILE) as file:
            file_contents = file.read()
        execution_start_cycle = int(
            re.search(
                "CONSTANT execution_start_cycle\s*:\s*integer\s*:=\s*(\d+)\s*;",
                file_contents,
            ).group(1)
        )
        total_execution_cycle = int(
            re.search(
                "CONSTANT total_execution_cycle\s*:\s*integer\s*:=\s*(\d+)\s*;",
                file_contents,
            ).group(1)
        )

        execution_start_time = CLOCK_PERIOD * execution_start_cycle + HALF_PERIOD 
        execution_end_time = CLOCK_PERIOD * total_execution_cycle + HALF_PERIOD 

        return execution_start_time, execution_end_time

class AssemblyProcessing():
    def sort(active_window):
        merged_intervals = []
        intervals = sorted(active_window, key=lambda x: x['start'])
        for interval in intervals:
            if not merged_intervals or interval['start'] > merged_intervals[-1]['end']:
                merged_intervals.append(interval)
            else:
                merged_intervals[-1]['end'] = max(merged_intervals[-1]['end'], interval['end'])
        merged_adjacent_intervals = []
        for interval in merged_intervals:
            if not merged_adjacent_intervals or interval['start'] > merged_adjacent_intervals[-1]['end']:
                merged_adjacent_intervals.append(interval)
            else:
                merged_adjacent_intervals[-1]['end'] = max(merged_adjacent_intervals[-1]['end'], interval['end'])
        sorted_active_window = merged_adjacent_intervals
        return(sorted_active_window)

