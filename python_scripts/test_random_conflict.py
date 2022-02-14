import csv
#import matplotlib.pyplot as plt
import json
import shutil
import os


#return current working directory
CWD = os.getcwd()
#get the bin path
#BIN_PATH = os.path.abspath(os.path.join(CWD, "../bin"))
BIN_PATH = "/home/dorina/CLionProjects/test_config/cmake-build-debug"
BIN_NAME = "test_random_conflict"

print("1.Alpha 2.ARC 3.ARM 32-bit 4.ARM 64-bit 5.TINBSPTMS320C6x 6.C-SKY 7.H8/300 8.Qualcomm Hexagon 9.IA-64\n"
      "10.Motorola 68000 11.MicroBlaze 12.MIPS 13.NDS32 14.Nios II 15.OpenRISC 16.PA-RISC 17.PowerPC 18.RISC-V\n"
      "19.IBM System/390 and z/Architecture 20.SuperH 32-bit 21.SuperH 64-bit 22.SPARC 32-bit 23.SPARC 64-bit\n"
      "24.User-Mode Linux 25.x86-32 26.x86-64 27.Xtensa")

choice = input("Please choose a architecture:")
choice = int(choice)
if choice == 1:
    archName = "alpha"
elif choice == 2:
    archName = "arc"
elif choice == 3:
    archName = "arm"
elif choice == 4:
    archName = "arm64"
elif choice == 5:
    archName = "c6x"
elif choice == 6:
    archName = "csky"
elif choice == 7:
    archName = "h8300"
elif choice == 8:
    archName = "hexagon"
elif choice == 9:
    archName = "ia64"
elif choice == 10:
    archName = "m68k"
elif choice == 11:
    archName = "microblaze"
elif choice == 12:
    archName = "mips"
elif choice == 13:
    archName = "nds32"
elif choice == 14:
    archName = "nios2"
elif choice == 15:
    archName = "openrisc"
elif choice == 16:
    archName = "parisc"
elif choice == 17:
    archName = "powerpc"
elif choice == 18:
    archName = "riscv"
elif choice == 19:
    archName = "s390"
elif choice == 20:
    archName = "sh"
elif choice == 21:
    archName = "sh64"
elif choice == 22:
    archName = "sparc32"
elif choice == 23:
    archName = "sparc64"
elif choice == 24:
    archName = "um"
elif choice == 25:
    archName = "i386"
elif choice == 26:
    archName = "x86_64"
elif choice == 27:
    archName = "xtensa"
else:
    archName = "x86_64"

NO_CONFIG = int(input("Please input how many number of configurations you want to run:") or "1")

#declare arguments for running the configfix_testing_framework script
ARGS = "-s /home/dorina/CLionProjects/test_config/cmake-build-debug/Kconfig"

for prob in range(1, NO_CONFIG+1):
    CONFIG_FOLDER_NAME = "config"
    path_prob = CONFIG_FOLDER_NAME + "." + str(prob * 10)

    config_path_initial = "/home/dorina/CLionProjects/test_config/tests/" + archName + "/" + path_prob + "/" + "config.json"
    config_path_final = "/home/dorina/CLionProjects/test_config/cmake-build-debug/config.json"

    if os.path.isfile(config_path_final):
        os.remove(config_path_final)
        shutil.copyfile(config_path_initial, config_path_final)
    else:
        shutil.copyfile(config_path_initial, config_path_final)

    def run_generate(bin_path, bin_name):
        # get generate_random_config from the bin path
        bin_exec_path = os.path.join(bin_path, bin_name)
        # go into the bin execute the arguments and the generate_random_config file
        os.chdir(bin_path)
        cmd = "{} {}".format(bin_exec_path, ARGS)
        os.system(cmd)

    run_generate(BIN_PATH, BIN_NAME)
