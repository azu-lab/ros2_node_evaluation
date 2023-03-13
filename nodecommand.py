import os
import argparse
from datetime import datetime
import sys
import time
import yaml


def get_params_file_name(ns, node_name):
    ns_modified = ns
    if ns_modified[0] == '/':
        ns_modified = ns_modified[1:]
    params_file_name = ns_modified + "/" + node_name + ".yaml"
    return  params_file_name.replace("/", "__")


def main(package_name, executable_name, ns, node_name, remapping_file):
    time.sleep(3)

    remappings = {}
    remapping_file_path = remapping_file
    print(remapping_file_path)
    with open(remapping_file_path, 'r') as f:
        remappings = yaml.safe_load(f)

    params_file_name = get_params_file_name(ns, node_name)

    currentdir = os.getcwd()

    os.chdir(args[6])
    print(os.getcwd())

    os.system("ros2 param dump " + ns + "/" + node_name + " --output-dir " + args[6])

    with open("ros2_run_" + package_name + "_" + executable_name, "w") as f:
        exec_command = "ros2 run " + package_name + " " + executable_name + \
                       " --ros-args --params-file " + params_file_name + \
                       " -r __ns:=" + ns + " -r __node:=" + node_name

        for k, v in remappings.items():
            exec_command = exec_command + " -r " + k + ":=" + v

        f.write(exec_command)

    
    os.chdir(currentdir)


if __name__ == "__main__":
    args = sys.argv
    main(args[1], args[2], args[3], args[4], args[5])

