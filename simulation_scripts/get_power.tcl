set FABRIC_PATH $::env(FABRIC_PATH)
set ITER $::env(ITER)
set START_TIME $::env(START_TIME)
set END_TIME $::env(END_TIME)
set CLOCK_PERIOD $::env(CLOCK_PERIOD)
set VCD_DIR $::env(VCD_DIR)
set PER_CYCLE_FLAG $::env(PER_CYCLE_FLAG)

set NUM_CPUS 8
set_multi_cpu_usage -local_cpu ${NUM_CPUS} -cpu_per_remote_host 1 -remote_host 0 -keep_license true
set DB ${FABRIC_PATH}/phy/db/silagonn.dat
read_db ${DB}

set_power_output_dir -reset
set_power_output_dir .
read_activity_file -reset
set_power -reset
set_dynamic_power_simulation -reset
set_default_switching_activity -input_activity 0 -global_activity 0 -macro_activity 0 -sequential_activity 0

    if {${PER_CYCLE_FLAG}==True} {
        set i ${START_TIME}
        while {$i < ${END_TIME}} {
            set_power_output_dir -reset
            set_power_output_dir .
            read_activity_file -reset
            set_power -reset
            set_dynamic_power_simulation -reset
            set_default_switching_activity -input_activity 0 -global_activity 0 -macro_activity 0 -sequential_activity 0
            set VCDNAME "${VCD_DIR}/${i}.vcd"
            set OUTFILE "${VCDNAME}.pwr"
            set RUN_TIME [expr $i + $CLOCK_PERIOD]
            read_activity_file -format VCD -scope /testbench/DUT -block {} ${VCDNAME} -start ${i}ns -end ${RUN_TIME}ns
            report_power -no_wrap -cell {all} -out_file ${OUTFILE}
            set i ${RUN_TIME}
        }
    } else {
        set VCDNAME "${VCD_DIR}/iter_${ITER}.vcd"
        set OUTFILE "${VCDNAME}.pwr"
        read_activity_file -format VCD -scope /testbench/DUT -block {} ${VCDNAME} -start ${START_TIME}ns -end ${END_TIME}ns
        report_power -no_wrap -cell {all} -out_file ${OUTFILE}
    }
exit
