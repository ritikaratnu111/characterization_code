set FABRIC_PATH $::env(FABRIC_PATH)
set ITER $::env(ITER)
set START_TIME $::env(START_TIME)
set END_TIME $::env(END_TIME)
vlib work
proc compile_vhdl_files { library file_list } { 
    set DIRECTORY [file dirname $file_list]
    set fp [open $file_list]
    set lines [split [read $fp] "\n"]
    close $fp;
    foreach line $lines {
        regsub "^\[ \t]*$" $line {} line
        if {$line != ""} { 
            vcom -2008 -work $library $DIRECTORY/$line;
        }   
    }   
}
compile_vhdl_files "work" $FABRIC_PATH/rtl/pkg_hierarchy.txt

vlog -work work /opt/stdc_libs/28HPC/stclib/9-track/30p140/nvt/TSMCHOME/digital/Front_End/verilog/tcbn28hpcbwp30p140_100a/tcbn28hpcbwp30p140.v
vcom -2008 -work work $FABRIC_PATH/rtl/SRAM/SRAM_model.vhd
vlog -work work $FABRIC_PATH/phy/db/silagonn_simulation.v
vcom -2008 -work work const_package.vhd
vcom -2008 -work work testbench_file.vhd
vsim work.testbench -t ns -vopt -voptargs=+acc
run $START_TIME ns;
set VCDNAME "activity_${ITER}.vcd";
vcd file $VCDNAME;
vcd add -r {sim:/testbench/DUT/Silago_top_l_corner_inst_0_0/* };
vcd add -r {sim:/testbench/DUT/Silago_bot_l_corner_inst_0_1/* };
vcd add -r {sim:/testbench/DUT/DiMArchTile_bot_l_inst_0_1/* };
set RUN_TIME [expr $END_TIME - $START_TIME];
run $RUN_TIME ns;
quit -sim;
exit