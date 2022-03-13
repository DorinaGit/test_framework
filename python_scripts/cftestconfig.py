import json
import shutil
import os
import sys

class ConflictFrameworkSetup:
    def __init__(self):
        ##paths
        CWD = os.getcwd()
        self.working_path = os.path.abspath(os.path.join(CWD, "../linux_branch_cmake"))

        self.testing_path = os.path.abspath(os.path.join(self.working_path, "../tests"))
        self.config_sample_dir = self.testing_path + "/x86_64/config.10"

        ##values needed by program
        self.config_sample_folder = "config."
        self.config_prob = "10"

        self.mode = "2"
        self.arch = "arm"
        self.srcarch = "arm"
        self.num_threads = 1
        self.num_conflicts = 1
        self.num_config_prob = 9
        self.min_conf_size = 1
        self.max_conf_size = 2
        self.arch_list = "arch_list_3_arch.json"

def init_default():
    os.environ["RUSTC"] = "rustc"
    os.environ["CC_VERSION_TEXT"] = "gcc (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
    os.environ["CC"] = "gcc"
    os.environ["LD"] = "ld"
    os.environ["srctree"] = "."


SETUP = ConflictFrameworkSetup()


def init_console():
    if os.getenv(SETUP.mode):
        SETUP.mode = os.getenv(SETUP.mode)
    else:
        SETUP.mode = SETUP.mode

def init():
    os.environ["working_path"] = SETUP.working_path
    #os.environ["root_path"] = SETUP.root_path

    os.environ["testing_path"] = SETUP.testing_path
    os.environ["config_sample_dir"] = SETUP.config_sample_dir
    os.environ["config_sample_foldr"] = SETUP.config_sample_folder
    os.environ["config_prob"] = SETUP.config_prob

    os.environ["ARCH"] = SETUP.arch
    os.environ["SRCARCH"] = SETUP.srcarch


BIN_NAME = "cftestgenconfig"
BIN_GEN_NAME ="generate_random_config"


def run_tests():
    if(SETUP.mode=="1"):
        run_mode_1()
    elif(SETUP.mode=="2"):
        run_mode_2()
    elif(SETUP.mode=="3"):
        run_mode_3()

### Generates conflicts for an already existing configuration
def run_mode_1():
    ARGS = "-s /home/dorina/CLionProjects/cftestconfig_python/linux_branch_cmake/Kconfig"
    for conflict_size in range(SETUP.min_conf_size, SETUP.max_conf_size):
        os.environ["conflict_size"] = str(conflict_size)
        for j in range(0, SETUP.num_conflicts):
            # get generate_random_config from the bin path
            bin_exec_path = os.path.join(SETUP.working_path, BIN_NAME)
            # go into the bin execute the arguments and the generate_random_config file
            os.chdir(SETUP.working_path)
            cmd = "{} {}".format(bin_exec_path, ARGS)
            os.system(cmd)

### Generates configuration and conflicts for a given architecture
def run_mode_2():
    os.environ["ARCH"] = SETUP.arch
    os.environ["SRCARCH"] = SETUP.srcarch

    path_arch = SETUP.testing_path + "/" + SETUP.arch

    ARGS = "--randconfig " \
           "-s /home/dorina/CLionProjects/cftestconfig_python/linux_branch_cmake/Kconfig"

    for i in range(1, 2):
        # get generate_random_config from the bin path
        bin_exec_path = os.path.join(SETUP.working_path, BIN_GEN_NAME)
        # go into the bin execute the arguments and the generate_random_config file
        os.chdir(SETUP.working_path)
        cmd = "{} {}".format(bin_exec_path, ARGS)
        os.system(cmd)

        prob = i*10
        config_prob = str(prob)
        config_sample_dir = SETUP.testing_path + "/" + SETUP.arch + "/" + SETUP.config_sample_folder + config_prob

        # create architecture
        if not os.path.exists(path_arch):
            os.mkdir(path_arch)

        if not os.path.exists(config_sample_dir):
            os.mkdir(config_sample_dir)

        # create the probabiliy folder
        oldfile = SETUP.working_path + "/.config"
        newfile = config_sample_dir + "/" + "." + SETUP.config_sample_folder + config_prob

        if os.path.exists(newfile):
            os.remove(newfile)
            shutil.copyfile(oldfile,newfile)
        else:
            shutil.copyfile(oldfile,newfile)

        os.environ["arch"] = SETUP.arch
        os.environ["srcarch"] = SETUP.srcarch
        os.environ["config_sample_dir"] = str(config_sample_dir)
        os.environ["config_prob"] = str(config_prob)

        for conflict_size in range(SETUP.min_conf_size, SETUP.max_conf_size):
            os.environ["conflict_size"] = str(conflict_size)
            for j in range(0, SETUP.num_conflicts):
                # get generate_random_config from the bin path
                bin_exec_path = os.path.join(SETUP.working_path, BIN_NAME)
                # go into the bin execute the arguments and the generate_random_config file
                os.chdir(SETUP.working_path)
                cmd = "{} {}".format(bin_exec_path, ARGS)
                os.system(cmd)


### Generates configuration and conflicts with a given list of architecture
def run_mode_3():
    ARGS = "--randconfig " \
           "-s /home/dorina/CLionProjects/cftestconfig_python/linux_branch_cmake/Kconfig"

    arch_list_test = SETUP.testing_path + "/" + SETUP.arch_list
    file_arch = open(arch_list_test)
    config_arch = json.load(file_arch)
    file_arch.close()

    for key, value in config_arch.items():
        key = config_arch[key]
        print(key)
        arch = key["ARCH"]
        srcarch = key["SRCARCH"]

        os.environ["arch"] = arch
        os.environ["srcarch"] = srcarch

        os.environ["ARCH"] = arch
        os.environ["SRCARCH"] = srcarch

        for i in range(1, 2):
            # get generate_random_config from the bin path
            bin_exec_path = os.path.join(SETUP.working_path, BIN_GEN_NAME)
            # go into the bin execute the arguments and the generate_random_config file
            os.chdir(SETUP.working_path)
            cmd = "{} {}".format(bin_exec_path, ARGS)
            os.system(cmd)

            prob = i*10
            config_prob = str(prob)
            config_sample_dir = SETUP.testing_path + "/" + arch + "/" + SETUP.config_sample_folder + config_prob

            # create architecture
            path_arch = SETUP.testing_path + "/" + arch
            if not os.path.exists(path_arch):
                os.mkdir(path_arch)

            if not os.path.exists(config_sample_dir):
                os.mkdir(config_sample_dir)

            # create the probabiliy folder
            oldfile = SETUP.working_path + "/.config"
            newfile = config_sample_dir + "/" + "." + SETUP.config_sample_folder + config_prob

            if os.path.exists(newfile):
                os.remove(newfile)
                shutil.copyfile(oldfile,newfile)
            else:
                shutil.copyfile(oldfile,newfile)

            os.environ["arch"] = arch
            os.environ["srcarch"] = srcarch
            os.environ["config_sample_dir"] = str(config_sample_dir)
            os.environ["config_prob"] = str(config_prob)

            for conflict_size in range(SETUP.min_conf_size, SETUP.max_conf_size):
                os.environ["conflict_size"] = str(conflict_size)
                for j in range(0, SETUP.num_conflicts):
                    # get generate_random_config from the bin path
                    bin_exec_path = os.path.join(SETUP.working_path, BIN_NAME)
                    # go into the bin execute the arguments and the generate_random_config file
                    os.chdir(SETUP.working_path)
                    cmd = "{} {}".format(bin_exec_path, ARGS)
                    os.system(cmd)


def main():
    init_default()
    init_console()
    init()
    run_tests()
if __name__ == "__main__":
    main()