#!/usr/bin/env python
import sys, os, getopt, subprocess
import innovus

INPUTDIR                        =   ""
FACTOR                          =   1000
ListOfPowerFiles                =   []
CellModules                     =   []
ListOfPowerProfiles             =   []
POWER_PROFILE                   =   ""              
HEADER_LINE_COUNT               =   49
TAIL_LINE_COUNT                 =   6
CELL_COUNT                      =   1

def SetParams(inputdir,factor):
    global INPUTDIR, FACTOR, POWER_PROFILE
    INPUTDIR = inputdir
    FACTOR = factor
    POWER_PROFILE = INPUTDIR + "/" + "power_profile.txt"

def GetModules():
    global CellModules
    # List of modules stores module alias and name
    for cell in range(0, CELL_COUNT):
        sequencer_name = "MTRF_COLS[" + str(cell) + "]" + ".MTRF_ROWS[" + str(cell) + "].if_drra_top_l_corner.Silago_top_l_corner_inst/SILEGO_cell/MTRF_cell/seq_gen"
        ConfigSWB_name = "MTRF_COLS[" + str(cell) + "]" + ".MTRF_ROWS[" + str(cell) + "].if_drra_top_l_corner.Silago_top_l_corner_inst/SILEGO_cell/config_swb"
        SWB_name = "MTRF_COLS[" + str(cell) + "]" + ".MTRF_ROWS[" + str(cell) + "].if_drra_top_l_corner.Silago_top_l_corner_inst/SILEGO_cell/swb"
        NOC_name = "DiMArch_COLS[" + str(cell) + "]" + ".DiMArch_ROWS[" + str(cell) + "].if_dimarch_bot_l_corner.DiMArchTile_bot_l_inst/noc_bus_out"
        SegmentBus_name = "DiMArch_COLS[" + str(cell) + "]" + ".DiMArch_ROWS[" + str(cell) + "].if_dimarch_bot_l_corner.DiMArchTile_bot_l_inst/u_segmented_bus"
        STile_name = "DiMArch_COLS[" + str(cell) + "]" + ".DiMArch_ROWS[" + str(cell) + "].if_dimarch_bot_l_corner.DiMArchTile_bot_l_inst/u_STILE/"
        ShadowReg_name = "MTRF_COLS[" + str(cell) + "]" + ".MTRF_ROWS[" + str(cell) + "].if_drra_top_l_corner.Silago_top_l_corner_inst/SILEGO_cell/MTRF_cell/shadowReg"
        RegisterFile_name = "MTRF_COLS[" + str(cell) + "]" + ".MTRF_ROWS[" + str(cell) + "].if_drra_top_l_corner.Silago_top_l_corner_inst/SILEGO_cell/MTRF_cell/reg_top/RegisterFile"
        DPU_name = "MTRF_COLS[" + str(cell) + "]" + ".MTRF_ROWS[" + str(cell) + "].if_drra_top_l_corner.Silago_top_l_corner_inst/SILEGO_cell/MTRF_cell/dpu_gen"
        MTRFCell_name = "MTRF_COLS[" + str(cell) + "]" + ".MTRF_ROWS[" + str(cell) + "].if_drra_top_l_corner.Silago_top_l_corner_inst/SILEGO_cell/MTRF_cell"
        SilegoCell_name = "MTRF_COLS[" + str(cell) + "]" + ".MTRF_ROWS[" + str(cell) + "].if_drra_top_l_corner.Silago_top_l_corner_inst/SILEGO_cell/"
        Cell_name = "MTRF_COLS[" + str(cell) + "]" + ".MTRF_ROWS[" + str(cell) + "].if_drra_top_l_corner.Silago_top_l_corner_inst/" + "*" + "DiMArch_COLS[" + str(cell) + "]" + ".DiMArch_ROWS[" + str(cell) + "].if_dimarch_bot_l_corner.DiMArchTile_bot_l_inst/"
        CellModules.append([cell, [["Sequencer", sequencer_name], ["ConfigSWB", ConfigSWB_name], ["SWB", SWB_name], ["NOC", NOC_name], ["SegmentBus", SegmentBus_name], 
                        ["STile", STile_name], ["ShadowReg", ShadowReg_name], ["RegisterFile", RegisterFile_name], ["DPU", DPU_name], ["MTRFCell", MTRFCell_name], 
                        ["SilegoCell", SilegoCell_name], ["Cell", Cell_name] ] ])

def GetPowerFiles():
    global ListOfPowerFiles
    for file in os.listdir(INPUTDIR):
        if file.endswith('.vcd.pwr'):
            ListOfPowerFiles.append(file)
    ListOfPowerFiles.sort()

def ProcessPowerFiles():
    for powerfile in ListOfPowerFiles:
        INPUT_POWER_FILE = INPUTDIR + "/" + powerfile
        OUTPUT_POWER_FILE =  INPUT_POWER_FILE
        with open(INPUT_POWER_FILE, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(OUTPUT_POWER_FILE, 'w') as fout:
            fout.writelines(data[HEADER_LINE_COUNT:len(data)-TAIL_LINE_COUNT]) 

def GetPerCycleModulePower():
    global ListOfPowerProfiles
    ListOfPowerProfiles.append(["cell", "start", "end","Sequencer", "ConfigSWB", "SWB", "NOC", "SegmentBus", "STile", "ShadowReg", "RegisterFile", "DPU", "MTRFCell", "SilegoCell", "Cell"])
    for cell_modules in CellModules:
        cell = cell_modules[0]
        Modules = cell_modules[1]
        for powerfile in ListOfPowerFiles:
            start_cycle = powerfile.split("_")[-2] 
            end_cycle = (powerfile.split("_")[-1]).split(".")[0]
            innovus.SetParams(INPUTDIR,powerfile)
            innovus.GetAllCells()
            innovus.GetDRRACells()
            innovus.GetDiMArchCells()
            for module in Modules:
                module_alias = module[0]
                module_name = module[1]
                module_power = innovus.GetPower(module_name,module_alias,FACTOR)
                if (module_alias == "Sequencer"):
                    Sequencer_power = module_power
                elif (module_alias == "ConfigSWB"):
                    ConfigSWB_power = module_power 
                elif (module_alias == "SWB"):
                    SWB_power = module_power 
                elif (module_alias == "NOC"):
                    NOC_power = module_power 
                elif (module_alias == "SegmentBus"):
                    SegmentBus_power = module_power 
                elif (module_alias == "STile"):
                    STile_power = module_power 
                elif (module_alias == "ShadowReg"):
                    ShadowReg_power = module_power 
                elif (module_alias == "RegisterFile"):
                    RegisterFile_power = module_power 
                elif (module_alias == "DPU"):
                    DPU_power = module_power 
                elif (module_alias == "MTRFCell"):
                    MTRFCell_power = module_power 
                elif (module_alias == "SilegoCell"):
                    SilegoCell_power = module_power 
                elif (module_alias == "Cell"):
                    Cell_power = module_power 
            ListOfPowerProfiles.append([cell,start_cycle,end_cycle,Sequencer_power,ConfigSWB_power,SWB_power,NOC_power,SegmentBus_power,STile_power,ShadowReg_power,RegisterFile_power,DPU_power,MTRFCell_power,SilegoCell_power,Cell_power])  
            print(cell,start_cycle,end_cycle,Sequencer_power,ConfigSWB_power,SWB_power,NOC_power,SegmentBus_power,STile_power,ShadowReg_power,RegisterFile_power,DPU_power,MTRFCell_power,SilegoCell_power,Cell_power)

def WriteModulePower():
    #print("Writing to power_profile...")
    with open(POWER_PROFILE, 'w') as f:
        for power_profiles in ListOfPowerProfiles:
            #f.write(f"{power_profiles}\n")
            f.write("{0:^5} {1:^5} {2:^5} {3:^12} {4:^12} {5:^12} {6:^12} {7:^12} {8:^12} {9:^12} {10:^12} {11:^12} {12:^12} {13:^12} {14:^12}".format(power_profiles[0],power_profiles[1],power_profiles[2],power_profiles[3],power_profiles[4],power_profiles[5],power_profiles[6],power_profiles[7],power_profiles[8],power_profiles[9],power_profiles[10],power_profiles[11],power_profiles[12],power_profiles[13], power_profiles[14]))
            f.write("\n")

def PrintFinishMessage():
    print("Finished!")

def main(argv):
    inputdir = ''
    try:
        opts, args = getopt.getopt(argv,"hi:f:",["inputdir=","factor="])
    except getopt.GetoptError:
        print ('read_power.py -i <inputdir> -f <factor>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('read_power.py -i <inputdir> -f <factor>')
            sys.exit()
        elif opt in ("-i", "--inputdir"):
            inputdir = arg
        elif opt in ("-f", "--factor"):
            factor = arg 
    SetParams(inputdir,factor)
    GetModules()
    GetPowerFiles()
    ProcessPowerFiles()
    GetPerCycleModulePower()
    WriteModulePower()
    PrintFinishMessage()

if __name__ == "__main__":
   main(sys.argv[1:])
