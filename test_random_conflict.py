import csv
import matplotlib.pyplot as plt
import json
import os

#configJson = {"ARCH", "CONFIGFIX_TEST_PATH", "CONFIGFIX_TEST_CONFIG_DIR", "CONFIGFIX_TEST_PROBABILITY", "CONFIGFIX_TEST_MIN_CONFLICT_SIZE", "CONFIGFIX_TEST_MAX_CONFLICT_SIZE", "NO_CONFLICTS"}
#architectureList = ["alpha", "arc", "arm", "arm64", "c6x", "csky", "h8300", "hexagon", "ia64", "m68k", "microblaze", "mips", "nds32", "nios2", "openrisc", "parisc", "powerpc", "riscv", "s390", "sh", "sh64", "sparc32", "sparc64", "um", "i386", "x86_64", "xtensa"]
# def switch():
# x = 3
# for case in switch():
#     if case(1):
#         ARCH = "alpha"
#         break
#     elif case(2):
#         ARCH = "arc"
#         break
#     else:
#     print("Invalid choice")
#


configJson = {}
architectureList = ["arc"]
i = 10
# the json file where the output must be stored
CONFIGFIX_ROOT = "/home/dorina/CLionProjects/TestRandomConflict/tests_59"

for arct in architectureList:
    for prob in range(1, 2):
        CONFIGFIX_TEST_CONFIG_DIR = "{}/{}/config.{}".format(CONFIGFIX_ROOT, arct, i * prob);
        configJson["KERNELVERSTION"] = "5.9.6"
        configJson["CC_VERSION_TEXT"] = "gcc (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
        configJson["ARCH"] = arct
        configJson["SRCARCH"] = arct
        configJson["srctree"] = "."
        configJson["CC"] = "gcc"
        configJson["LD"] = "ld"
        configJson["CONFIGFIX_TEST_PATH"] = CONFIGFIX_ROOT
        configJson["CONFIGFIX_TEST_CONFIG_DIR"] = CONFIGFIX_TEST_CONFIG_DIR
        configJson["CONFIG_BASE"] = ".config.base"
        configJson["KCONFIG_CONFIG"] = "config."
        configJson["CONFIGFIX_TEST_PROBABILITY"] = str(i * prob)
        configJson["CONFIGFIX_TEST_MIN_CONFLICT_SIZE"] = 1
        configJson["CONFIGFIX_TEST_MAX_CONFLICT_SIZE"] = 1
        configJson["NO_CONFLICTS"] = 1

        with open("config.json", "w") as out_file:
            json.dump(configJson, out_file, indent=4)
        ##out_file.close()

       ## os.system("./TestRandomConflicts --config config.json")


#choose a style
plt.style.use('classic')
plt.style.use('fivethirtyeight')

#define values
ARCHITECTURE_IDX = 0
CONFIG_IDX = 8
CONFIG_TIME = 9
my_data =[]
my_data_01 =[]

TIME_RESOLUTION = 5
#get values
with open("../configfix_test/tests_59_new/results.csv", newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        architecture = row[ARCHITECTURE_IDX]
        configuration = row[CONFIG_IDX]
        time = float(row[CONFIG_TIME])
        my_data.append(int(time/TIME_RESOLUTION)*TIME_RESOLUTION)
        my_data_01.append(configuration)
        print(architecture,configuration,time)

#print(", ".join(row));
#print(row)

# the data
print(my_data)
plt.hist(my_data, edgecolor='black', density=True)

plt.xlabel('Time')
plt.ylabel('Occurrence')
plt.title('Histogram')
#plt.xlim(0, 40)
#plt.ylim(0, 11)

plt.show()
