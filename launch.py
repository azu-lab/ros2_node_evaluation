import os
import argparse
from datetime import datetime
import sys
import os, sys, time
import sys
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import subprocess
import time
import re
from tkinter import filedialog
import glob
import yaml
import rclpy
from rclpy.node import Node
import time
import os
import signal



def main(launchpath, mappath, vehicle, sensor):
    print(launchpath)
    print(mappath)
    print(vehicle)


    launch_exec = subprocess.Popen(['ros2', 'launch', launchpath, mappath, vehicle, sensor], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) #launchファイル起動


if __name__ == "__main__":
    args = sys.argv
    main(args[1], args[2], args[3], args[4])

