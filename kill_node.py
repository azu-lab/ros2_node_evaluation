import os
import glob
import subprocess
import shutil
import re
from distutils.dir_util import copy_tree
import sqlite3
import sys

args = sys.argv

kill_node_path = args[1]


files = glob.glob(kill_node_path + '/ros2_run_*')
# print(files)

kill_list = []

for i in files:
    f = open(i, 'r') 
    words = f.read()
    list_words = words.split()
    kill_list.append(list_words[3])
    f.close()

print(kill_list)

for node in kill_list:
    subprocess.run(['killall', '-2', node], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)


