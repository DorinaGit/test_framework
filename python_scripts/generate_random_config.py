import os
import sys
import subprocess
import shutil
import json
from subprocess import Popen, PIPE

configJson = {}
#return current working directory
CWD = os.getcwd()
#get the bin path
#BIN_PATH = os.path.abspath(os.path.join(CWD, "../bin"))
BIN_PATH = "/home/dorina/CLionProjects/test_config/cmake-build-debug"

#get the tests path
TESTS_PATH = os.path.abspath(os.path.join(CWD, "../tests"))

BIN_NAME = "generate_random_config"
CONFIG_NAME = ".config"
CONFIG_FOLDER_NAME = "config"

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
    archName = "microblaze"
elif choice == 11:
    archName = "mips"
elif choice == 12:
    archName = "nds32"
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

NO_CONFIG = int(input("Please input number of configurations:") or "1")
MIN_CONFLICT_SIZE = int(input("Please input min number of conflicts:") or "1")
MAX_CONFLICT_SIZE = int(input("Please input max number of conflicts:") or "1")
NO_CONFLICTS = int(input("Please input number of conflicts:") or "1")

path_arch = TESTS_PATH + "/" + archName
if not os.path.exists(path_arch):
    os.mkdir(path_arch)
    fileArch = open('arch_list.json')
    CONFIG_ALL = json.load(fileArch)
    fileArch.close()


    #declare arguments for running the qconf script
    # ARGS = "-s /home/dorina/CLionProjects/test_config/cmake-build-debug/Kconfig"\
    #        "--oldconfig " \
    #        "--allnoconfig " \
    #        "--allyesconfig " \
    #        "--allmodconfig " \
    #        "--alldefconfig " \
    #        "--randconfig " \
    #        "--listnewconfig " \
    #        "--olddefconfig " \
    #        "--syncconfig " \
    #        "--helpnewconfig " \
    #        "--yes2modconfig " \
    #        "--mod2yesconfig "

    ARGS = "--randconfig " \
           "-s /home/dorina/CLionProjects/test_config/cmake-build-debug/Kconfig"


    def run_generate(bin_path, bin_name, config_name, envs=None):

        # get generate_random_config from the bin path
        bin_exec_path = os.path.join(bin_path, bin_name)
        #get ".config" from the bin path
        config_path_initial = os.path.join(bin_path, config_name)

        #if ".config" is in the intial path then remove it
        if os.path.isfile(config_path_initial):
            os.remove(config_path_initial)

        if envs:
            for key, value in envs.items():
                os.environ[key] = value

        for prob in range(1, 2):
            # go into the bin execute the arguments and the generate_random_config file
            os.chdir(bin_path)
            cmd = "{} {}".format(bin_exec_path, ARGS)
            os.system(cmd)

            # rename the .config file to .config.base
            config_name_base = ".config.base"
            config_path_initial_base = os.path.join(bin_path, config_name_base)
            os.rename(config_path_initial, config_path_initial_base)

            # copying the renamed config file to the folder
            if os.path.isfile(config_path_initial_base):
                config_path_final = path_arch + "/" + ".config.base"
                shutil.move(config_path_initial_base, config_path_final)
            else:
                print("ERROR: File {} was not generated".format(config_path_initial_base))



        for prob in range(1, NO_CONFIG+1):
             #go into the bin execute the arguments and the generate_random_config file
             os.chdir(bin_path)
             cmd = "{} {}".format(bin_exec_path, ARGS)
             os.system(cmd)

             # proc = subprocess.Popen(bin_exec_path, stdin=subprocess.PIPE)
             # proc.stdin.write('here, have some data\n')

            #  process = Popen([ARGS, bin_exec_path], stdout=PIPE, stderr=PIPE)
            # # process = Popen("KCONFIG_SEED", stdout=PIPE, stderr=PIPE)
            #  output, err = process.communicate()
            #  print("output= ", output)
            #  print("err= ", err)

             #create the probabiliy folder
             path_prob = path_arch + "/" + CONFIG_FOLDER_NAME + "." + str(prob*10)
             if not os.path.exists(path_prob):
                 os.mkdir(path_prob)

             #rename the .config file to .config.prob
             config_name_prob = CONFIG_NAME + "." + str(prob * 10)
             config_path_initial_prob = os.path.join(bin_path, config_name_prob)
             os.rename(config_path_initial, config_path_initial_prob)
             shutil.copyfile(config_path_initial_prob, config_path_initial)

             # copying the renamed config file to the folder
             if os.path.isfile(config_path_initial_prob):
                 config_path_final = path_arch + "/" + CONFIG_FOLDER_NAME + "." + str(prob * 10)
                 shutil.move(config_path_initial_prob, config_path_final)
             else:
                print("ERROR: File {} was not generated".format(config_path_initial_prob))

             # Config json
             CONFIGFIX_TEST_CONFIG_DIR = "{}/{}/config.{}".format(TESTS_PATH, archName, 10 * prob)
             CC_VERSION_TEXT = "gcc (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
             configJson["ENV"] = {
                "CC_VERSION_TEXT": CC_VERSION_TEXT,
                "SRCARCH": SRCARCH,
                "srctree": ".",
                "LD": "ld",
                "CC": "gcc",
            }
             configJson["KERNELVERSION"] = "5.9.6"
             configJson["ARCH"] = ARCH
             configJson["CONFIGFIX_TEST_PATH"] = TESTS_PATH
             configJson["CONFIGFIX_TEST_CONFIG_DIR"] = CONFIGFIX_TEST_CONFIG_DIR
             configJson["CONFIG_BASE"] = ".config.base"
             configJson["KCONFIG_CONFIG"] = "config."
             configJson["CONFIGFIX_TEST_PROBABILITY"] = str(10 * prob)
             configJson["CONFIGFIX_TEST_MIN_CONFLICT_SIZE"] = MIN_CONFLICT_SIZE
             configJson["CONFIGFIX_TEST_MAX_CONFLICT_SIZE"] = MAX_CONFLICT_SIZE
             configJson["NO_CONFLICTS"] = NO_CONFLICTS
             configJson["KCONFIG_SEED"] = "0xB952EF3A"
             path_json = config_path_final
             name_json = "config"

             with open("{}/{}.json".format(path_json, name_json), "w") as out_file:
                json.dump(configJson, out_file, indent=4)

    if __name__ == "__main__":

        envVar = CONFIG_ALL[archName]
        for key, value in envVar.items():
            ARCH = envVar["ARCH"]
            SRCARCH = envVar["SRCARCH"]
            envs = {
                    "LD": "ld",
                    "CC": "gcc",
                    "ARCH": ARCH,
                    "SRCARCH": SRCARCH,
                    "srctree": ".",
                    "CC_VERSION_TEXT": "gcc (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
            }

    run_generate(BIN_PATH, BIN_NAME, CONFIG_NAME, envs)

else:
    #shutil.rmtree(path_arch)
    #os.mkdir(path_arch)
    print("This file already exist.")



