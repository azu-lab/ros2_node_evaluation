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
import signal
import pprint
import csv
import shutil

home_path = '/home/tatsuya/2022_syuron'
remap_path = '/home/tatsuya/new_visualization_tool/visualization_tool/remap.csv'

before_node = ['before_node']
roop_cnt = 0

os.chdir(home_path)

if not os.path.exists('remap_yaml_list'):
	os.mkdir('remap_yaml_list')
	os.chdir('remap_yaml_list')
	output_path = home_path + 'remap_yaml_list'

	with open(remap_path, 'r')as f:
		for current_node in csv.reader(f): #csvファイルを1行ずつ読み取り

			if roop_cnt != 0: #2行目以降は以下の処理に入る

				if current_node[0] != before_node[0]: #前回のnodeと今回のnodeの名前を比較

					node_name = str(current_node[0]) #listをstring型に変換
					node_name = node_name.replace('[\'', '')
					node_name = node_name.replace('\']', '')
					genelate_file = node_name + '.yaml'

					if not os.path.exists(genelate_file): #追記するyamlファイルが存在するか判定

						file = open(genelate_file, 'w') #yamlが無いため生成
						file.write(current_node[1] + ': ' + current_node[2] + '\n') #remap情報を記述
						file.close()

					else:
						file = open(genelate_file, 'a')
						file.write(current_node[1] + ': ' + current_node[2] + '\n')
						file.close()

				elif current_node[0] == before_node[0]:

					with open(genelate_file, 'a')as yaml:
						yaml.write(current_node[1] + ': ' + current_node[2] + '\n')

			before_node[0] = current_node[0] #今回のnode名をｂ[0]に記憶させる

			roop_cnt+=1

elif os.path.exists('remap_yaml_list'):

	if os.path.exists('remap_yaml_list_2'):
		shutil.rmtree('remap_yaml_list_2')

	# if not os.path.exists('remap_yaml_list_2'):
	# 	os.mkdir('remap_yaml_list_2')

	os.mkdir('remap_yaml_list_2')
	os.chdir('remap_yaml_list_2')

	output_path = home_path + 'remap_yaml_list_2'

	with open(remap_path, 'r')as f:
		for current_node in csv.reader(f): #csvファイルを1行ずつ読み取り	

			if roop_cnt != 0: #2行目以降は以下の処理に入る

				if current_node[0] != before_node[0]: #前回のnodeと今回のnodeの名前を比較

					node_name = str(current_node[0]) #listをstring型に変換
					node_name = node_name.replace('[\'', '')
					node_name = node_name.replace('\']', '')
					genelate_file = node_name + '.yaml'

					if not os.path.exists(genelate_file): #追記するyamlファイルが存在するか判定

						file = open(genelate_file, 'w') #yamlが無いため生成
						file.write(current_node[1] + ': ' + current_node[2] + '\n') #remap情報を記述
						file.close()

					else:
						file = open(genelate_file, 'a')
						file.write(current_node[1] + ': ' + current_node[2] + '\n')
						file.close()

				elif current_node[0] == before_node[0]:

					with open(genelate_file, 'a')as yaml:
						yaml.write(current_node[1] + ': ' + current_node[2] + '\n')

			before_node[0] = current_node[0] #今回のnode名をｂ[0]に記憶させる

			roop_cnt+=1

	find_file_exec = subprocess.run(["find", output_path, "-name", "*.yaml"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	find_file = find_file_exec.stdout.strip().split('\n')

	os.chdir(home_path)

	for yaml_list in find_file:
		yaml_list_replace = yaml_list.replace('remap_yaml_list_2', 'remap_yaml_list')
		# print(yaml_list)
		# print(yaml_list_replace)
		os.replace(yaml_list, yaml_list_replace)

#以下、重複するメッセージの削除
replace_path = home_path + 'remap_yaml_list'
find_file_exec = subprocess.run(["find", replace_path, "-name", "*.yaml"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
find_file = find_file_exec.stdout.strip().split('\n')

for yaml_list in find_file:
	with open(yaml_list, 'r')as yaml_replace:
		read_file = yaml_replace.read()
		print(read_file)
		find_file_list = read_file.split('\n')
		find_file_list = list(find_file_list)

	with open(yaml_list, 'w')as yaml_replace:
		print(yaml_list)
		a = set(find_file_list)
		if '' in a:
			a.remove('')
		print(a)
		b = '\n'.join(a)
		yaml_replace.write(b)

if os.path.exists('remap_yaml_list_2'):
	shutil.rmtree('remap_yaml_list_2')

print('\ngenelated remap files\n')
