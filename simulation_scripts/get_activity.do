set FABRIC_PATH $::env(FABRIC_PATH)
set ITER $::env(ITER)
set START_TIME $::env(START_TIME)
set END_TIME $::env(END_TIME)
set CLOCK_PERIOD $::env(CLOCK_PERIOD)
set VCD_DIR $::env(VCD_DIR)
set PER_CYCLE_FLAG $::env(PER_CYCLE_FLAG)
set COMPONENT_FLAG $::env(COMPONENT_FLAG)
set RUN_TIME [expr $END_TIME - $START_TIME];
set COMPONENT $::env(COMPONENT)
set TILE $::env(TILE)
set STATE $::env(STATE)
set VCD_SIGNALS "{sim:/testbench/DUT/${TILE}/* }"

vlib work
vlib dware

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
vlog -work work /opt/stdc_libs/28HPC/SRAM/Macros/ts1n28hpcsvtb128x128m4swbasod_170b/VERILOG/ts1n28hpcsvtb128x128m4swbasod_170b_tt0p9v0p9v25c.v
vlog -work work $FABRIC_PATH/phy/db/silagonn_simulation.v
vcom -2008 -work work $FABRIC_PATH/rtl/SRAM/SRAM_model.vhd

vcom -2008 -work work const_package.vhd
vcom -2008 -work work testbench_rtl.vhd

if {$COMPONENT_FLAG ==True} {
	vsim work.testbench -t ps -vopt -voptargs=+acc;
	run $START_TIME ns;
    set VCDNAME "${VCD_DIR}/iter_${ITER}_${COMPONENT}_${STATE}_${START_TIME}.vcd";
    vcd file $VCDNAME;
	if {$TILE == "Silago_top_l_corner_inst_0_0"} {
          vcd add -r {sim:/testbench/DUT/Silago_top_l_corner_inst_0_0/* };
	} elseif {$TILE == "Silago_top_r_corner_inst_7_0"} {
		vcd add -r {sim:/testbench/DUT/Silago_top_r_corner_inst_7_0/* };
	} elseif {$TILE == "Silago_bot_l_corner_inst_0_1"} {
		vcd add -r {sim:/testbench/DUT/Silago_bot_l_corner_inst_0_1/* };
	} elseif {$TILE == "Silago_bot_r_corner_inst_7_1"} {
		vcd add -r {sim:/testbench/DUT/Silago_bot_r_corner_inst_7_1/* };
	} elseif {$TILE == "Silago_top_inst_1_0"} {
		vcd add -r {sim:/testbench/DUT/Silago_top_inst_1_0/* };
	} elseif {$TILE == "Silago_top_inst_2_0"} {
		vcd add -r {sim:/testbench/DUT/Silago_top_inst_2_0/* };
	} elseif {$TILE == "Silago_top_inst_3_0"} {
		vcd add -r {sim:/testbench/DUT/Silago_top_inst_3_0/* };
	} elseif {$TILE == "Silago_top_inst_4_0"} {
		vcd add -r {sim:/testbench/DUT/Silago_top_inst_4_0/* };
	} elseif {$TILE == "Silago_top_inst_5_0"} {
		vcd add -r {sim:/testbench/DUT/Silago_top_inst_5_0/* };
	} elseif {$TILE == "Silago_top_inst_6_0"} {
		vcd add -r {sim:/testbench/DUT/Silago_top_inst_6_0/* };
	} elseif {$TILE == "Silago_bot_inst_1_1"} {
		vcd add -r {sim:/testbench/DUT/Silago_bot_inst_1_1/* };
	} elseif {$TILE == "Silago_bot_inst_2_1"} {
		vcd add -r {sim:/testbench/DUT/Silago_bot_inst_2_1/* };
	} elseif {$TILE == "Silago_bot_inst_3_1"} {
		vcd add -r {sim:/testbench/DUT/Silago_bot_inst_3_1/* };
	} elseif {$TILE == "Silago_bot_inst_4_1"} {
		vcd add -r {sim:/testbench/DUT/Silago_bot_inst_4_1/* };
	} elseif {$TILE == "Silago_bot_inst_5_1"} {
		vcd add -r {sim:/testbench/DUT/Silago_bot_inst_5_1/* };
	} else {
		vcd add -r {sim:/testbench/DUT/Silago_bot_inst_6_1/* };
	}
	run $RUN_TIME ns;
	quit -sim;
} else {
    if {$PER_CYCLE_FLAG ==True} {
        set i ${START_TIME}
        while {$i < ${END_TIME}} {
			vsim work.testbench -t ps -vopt -voptargs=+acc;
			run $i ns;
			echo $i
        	set VCDNAME "${VCD_DIR}/${i}.vcd";
            vcd file $VCDNAME;
			if {$TILE == "Silago_top_l_corner_inst_0_0"} {
            vcd add -r {sim:/testbench/DUT/Silago_top_l_corner_inst_0_0/* };
			} elseif {$TILE == "Silago_top_r_corner_inst_7_0"} {
				vcd add -r {sim:/testbench/DUT/Silago_top_r_corner_inst_7_0/* };
			} elseif {$TILE == "Silago_bot_l_corner_inst_0_1"} {
				vcd add -r {sim:/testbench/DUT/Silago_bot_l_corner_inst_0_1/* };
			} elseif {$TILE == "Silago_bot_r_corner_inst_7_1"} {
				vcd add -r {sim:/testbench/DUT/Silago_bot_r_corner_inst_7_1/* };
			} elseif {$TILE == "Silago_top_inst_1_0"} {
				vcd add -r {sim:/testbench/DUT/Silago_top_inst_1_0/* };
			} elseif {$TILE == "Silago_top_inst_2_0"} {
				vcd add -r {sim:/testbench/DUT/Silago_top_inst_2_0/* };
			} elseif {$TILE == "Silago_top_inst_3_0"} {
				vcd add -r {sim:/testbench/DUT/Silago_top_inst_3_0/* };
			} elseif {$TILE == "Silago_top_inst_4_0"} {
				vcd add -r {sim:/testbench/DUT/Silago_top_inst_4_0/* };
			} elseif {$TILE == "Silago_top_inst_5_0"} {
				vcd add -r {sim:/testbench/DUT/Silago_top_inst_5_0/* };
			} elseif {$TILE == "Silago_top_inst_6_0"} {
				vcd add -r {sim:/testbench/DUT/Silago_top_inst_6_0/* };
			} elseif {$TILE == "Silago_bot_inst_1_1"} {
				vcd add -r {sim:/testbench/DUT/Silago_bot_inst_1_1/* };
			} elseif {$TILE == "Silago_bot_inst_2_1"} {
				vcd add -r {sim:/testbench/DUT/Silago_bot_inst_2_1/* };
			} elseif {$TILE == "Silago_bot_inst_3_1"} {
				vcd add -r {sim:/testbench/DUT/Silago_bot_inst_3_1/* };
			} elseif {$TILE == "Silago_bot_inst_4_1"} {
				vcd add -r {sim:/testbench/DUT/Silago_bot_inst_4_1/* };
			} elseif {$TILE == "Silago_bot_inst_5_1"} {
				vcd add -r {sim:/testbench/DUT/Silago_bot_inst_5_1/* };
			} else {
				vcd add -r {sim:/testbench/DUT/Silago_bot_inst_6_1/* };
			}
            run $CLOCK_PERIOD ns;
        	set new_i [expr $i + $CLOCK_PERIOD];
            set i ${new_i};
            quit -sim;
		}
    } else {
		vsim work.testbench -t ps -vopt -voptargs=+acc;
		run $START_TIME ns;
        set VCDNAME "${VCD_DIR}/iter_${ITER}.vcd";
        vcd file $VCDNAME;
		if {$TILE == "Silago_top_l_corner_inst_0_0"} {
	          vcd add -r {sim:/testbench/DUT/Silago_top_l_corner_inst_0_0/* };
		} elseif {$TILE == "Silago_top_r_corner_inst_7_0"} {
			vcd add -r {sim:/testbench/DUT/Silago_top_r_corner_inst_7_0/* };
		} elseif {$TILE == "Silago_bot_l_corner_inst_0_1"} {
			vcd add -r {sim:/testbench/DUT/Silago_bot_l_corner_inst_0_1/* };
		} elseif {$TILE == "Silago_bot_r_corner_inst_7_1"} {
			vcd add -r {sim:/testbench/DUT/Silago_bot_r_corner_inst_7_1/* };
		} elseif {$TILE == "Silago_top_inst_1_0"} {
			vcd add -r {sim:/testbench/DUT/Silago_top_inst_1_0/* };
		} elseif {$TILE == "Silago_top_inst_2_0"} {
			vcd add -r {sim:/testbench/DUT/Silago_top_inst_2_0/* };
		} elseif {$TILE == "Silago_top_inst_3_0"} {
			vcd add -r {sim:/testbench/DUT/Silago_top_inst_3_0/* };
		} elseif {$TILE == "Silago_top_inst_4_0"} {
			vcd add -r {sim:/testbench/DUT/Silago_top_inst_4_0/* };
		} elseif {$TILE == "Silago_top_inst_5_0"} {
			vcd add -r {sim:/testbench/DUT/Silago_top_inst_5_0/* };
		} elseif {$TILE == "Silago_top_inst_6_0"} {
			vcd add -r {sim:/testbench/DUT/Silago_top_inst_6_0/* };
		} elseif {$TILE == "Silago_bot_inst_1_1"} {
			vcd add -r {sim:/testbench/DUT/Silago_bot_inst_1_1/* };
		} elseif {$TILE == "Silago_bot_inst_2_1"} {
			vcd add -r {sim:/testbench/DUT/Silago_bot_inst_2_1/* };
		} elseif {$TILE == "Silago_bot_inst_3_1"} {
			vcd add -r {sim:/testbench/DUT/Silago_bot_inst_3_1/* };
		} elseif {$TILE == "Silago_bot_inst_4_1"} {
			vcd add -r {sim:/testbench/DUT/Silago_bot_inst_4_1/* };
		} elseif {$TILE == "Silago_bot_inst_5_1"} {
			vcd add -r {sim:/testbench/DUT/Silago_bot_inst_5_1/* };
		} else {
			vcd add -r {sim:/testbench/DUT/Silago_bot_inst_6_1/* };
		}
		run $RUN_TIME ns;
		quit -sim;
        }
}

exit