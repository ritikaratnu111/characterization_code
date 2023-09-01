set_multi_cpu_usage -local_cpu 8 -cpu_per_remote_host 1 -remote_host 0 -keep_license true
set FABRIC_PATH $::env(FABRIC_PATH)
set ITER $::env(ITER)
set START_TIME $::env(START_TIME)
set END_TIME $::env(END_TIME)
read_db ${FABRIC_PATH}/phy/db/silagonn.dat
set VCDNAME "activity_${ITER}.vcd"
set OUTFILE "/media/storage1/ritika/power_reports/mmm/left_col/iter_${ITER}.pwr"
set_power_output_dir -reset
set_power_output_dir .
read_activity_file -reset
set_power -reset
set_dynamic_power_simulation -reset
set_default_switching_activity -input_activity 0 -global_activity 0 -macro_activity 0 -sequential_activity 0
read_activity_file -format VCD -scope /testbench/DUT -block {} ${VCDNAME} -start ${START_TIME}ns -end ${END_TIME}ns
report_power -no_wrap -cell {all} -out_file ${OUTFILE}
exit
