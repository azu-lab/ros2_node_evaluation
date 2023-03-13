import os
import glob
import subprocess
import shutil
import re
from distutils.dir_util import copy_tree
import sqlite3
import sys

args = sys.argv

rosbag_path = args[1]
rate = args[2]

if rate:
    print('rate is ' + rate)
    playbag_exec = subprocess.run(['ros2', 'bag', 'play', '-r', rate, rosbag_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
else:
    print('rate is 1.0')
    playbag_exec = subprocess.run(['ros2', 'bag', 'play', rosbag_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
