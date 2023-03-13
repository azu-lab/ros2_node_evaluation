import os
import glob
import subprocess
import shutil
import re
from distutils.dir_util import copy_tree
import sqlite3
import sys
import time

args = sys.argv

run_node_path = args[1]

currentdir = os.getcwd()
os.chdir(run_node_path)

files = glob.glob('ros2_run_*')
print(files)

for i in files:
    subprocess.Popen(['bash', i], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    time.sleep(3)

os.chdir(currentdir)

