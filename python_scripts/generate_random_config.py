import os
import sys
import subprocess
import shutil
import json

configJson = {}
#return current working directory
CWD = os.getcwd()
#get the bin path
BIN_PATH = os.path.abspath(os.path.join(CWD, "../bin"))
#get the tests path
TESTS_PATH = os.path.abspath(os.path.join(CWD, "../tests"))

BIN_NAME = "generate_random_config"
CONFIG_NAME = ".config"

archName = "Alpha"
path_arch = TESTS_PATH + "/" + archName
if not os.path.exists(path_arch):
    os.mkdir(path_arch)

for prob in range(1, 3):
    CONFIG_FILENAME = CONFIG_NAME + "." + str(prob*10)
    path_prob = path_arch + "/" + CONFIG_FILENAME
    if not os.path.exists(path_prob):
        os.mkdir(path_prob)

#declare arguments for running the qconf script
ARGS = "--oldconfig " \
       "--allnoconfig " \
       "--allyesconfig " \
       "--allmodconfig " \
       "--alldefconfig " \
       "--randconfig " \
       "--listnewconfig " \
       "--olddefconfig " \
       "--syncconfig " \
       "--helpnewconfig " \
       "--yes2modconfig " \
       "--mod2yesconfig " \
       "-s /home/dorina/CLionProjects/TestRandomConflict/cmake-build-debug/Kconfig"

def run_generate(bin_path, bin_name, tests_path, config_name, envs=None):

    # get generate_random_config from the bin path
    bin_exec_path = os.path.join(bin_path, bin_name)
    #get ".config" from the bin path
    config_path_initial = os.path.join(bin_path, config_name)
    #get the path in where to move ".config"
    #config_path_final_base = os.path.join(tests_path, config_name)
    #config path arch
    #config_path_final = os.path.join(path_arch, config_name)


    # if ".config" is in the intial path then remove it
    if os.path.isfile(config_path_initial):
        os.remove(config_path_initial)

    if envs:
        for key, value in envs.items():
            os.environ[key] = value

    for prob in range(1, 3):
         #go into the bin execute the arguments and the generate_random_config file
         os.chdir(bin_path)
         cmd = "{} {}".format(bin_exec_path, ARGS)
         os.system(cmd)

         CONFIG_FILENAME = CONFIG_NAME + "." + str(prob * 10)
         config_path_final = path_arch + "/" + CONFIG_FILENAME
         if not os.path.exists(config_path_final):
             os.mkdir(config_path_final)

         config_name_prob = CONFIG_NAME + "." + str(prob * 10)
         config_path_initial_prob = os.path.join(bin_path, config_name_prob)
         os.rename(config_path_initial, config_path_initial_prob)

         # copying files
         if os.path.isfile(config_path_initial_prob):
            #shutil.move(config_path_initial, config_path_final)
            shutil.move(config_path_initial_prob, config_path_final)
         else:
            print("ERROR: File {} was not generated".format(config_path_initial_prob))

if __name__ == "__main__":

    fileArch = open('config_arch.json')
    CONFIG_ALL = json.load(fileArch)
    fileArch.close()
    envVar = CONFIG_ALL[archName]
    for key, value in envVar.items():
        ARCH = envVar["ARCH"]
        SRCARCH = envVar["SRCARCH"]
        envs = {
                "LD": "ld",
                "CC": "gcc",
                "ARCH" : ARCH,
                "SRCARCH": SRCARCH,
                "srctree": ".",
                "CC_VERSION_TEXT": "gcc (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
        }

        CONFIGFIX_ROOT = "/home/dorina/CLionProjects/TestRandomConflict/tests_59"
        CONFIGFIX_TEST_CONFIG_DIR = "{}/{}/config.{}".format(CONFIGFIX_ROOT, ARCH, 10 * prob)

        CC_VERSION_TEXT = "gcc (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
        configJson["ENV"] = {
            "CC_VERSION_TEXT": CC_VERSION_TEXT,
            "SRCARCH": SRCARCH,
            "ARCH": ARCH,
            "srctree": ".",
            "LD": "ld",
            "CC": "gcc",
        }
        configJson["KERNELVERSTION"] = "5.9.6"
        configJson["CONFIGFIX_TEST_PATH"] = CONFIGFIX_ROOT
        configJson["CONFIGFIX_TEST_CONFIG_DIR"] = CONFIGFIX_TEST_CONFIG_DIR
        configJson["CONFIG_BASE"] = ".config.base"
        configJson["KCONFIG_CONFIG"] = "config."
        configJson["CONFIGFIX_TEST_PROBABILITY"] = str(10 * prob)
        configJson["CONFIGFIX_TEST_MIN_CONFLICT_SIZE"] = 1
        configJson["CONFIGFIX_TEST_MAX_CONFLICT_SIZE"] = 1
        configJson["NO_CONFLICTS"] = 1

        with open("config.json", "w") as out_file:
            json.dump(configJson, out_file, indent=4)

        # config_name_json = "config.json"
        # config_path_json = os.path.join(CWD, config_name_json)
        # config_path_final_json = "/home/dorina/CLionProjects/TestRandomConflict/tests/Alpha/.config.10"
        # # copying files
        # if os.path.isfile(config_path_json):
        #     shutil.move(CWD, config_path_final_json)
        # else:
        #     print("ERROR: File {} was not generated".format(config_path_json))


    # generate configurations
    run_generate(BIN_PATH, BIN_NAME, TESTS_PATH, CONFIG_NAME, envs)


