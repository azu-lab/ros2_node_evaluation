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
from datetime import datetime
import shutil
from caret_analyze.plot import Plot
from caret_analyze import Application, Architecture, Lttng
from bokeh.plotting import output_notebook, figure, show
import visualize_callback
import visualize_paths
import architecture
import start_trace


class UpperFrame_tab_one(tk.Frame):
    def __init__(self, master=None):
        self.package = ''
        self.nodename = ''
        self.namespace = ''
        self.executable = ''
        self.args = ''
         

        def start_launch():
            launch_path = self.launch_entry.get() #launchファイルまでのパス
            
            if upper_frame_tab_three.rdo_var.get() == 0:
                print(upper_frame_tab_three.map_entry.get())
                cmd1 = 'map_path:=' + upper_frame_tab_three.map_entry.get() 
                cmd2 = 'vehicle_model:=' + upper_frame_tab_three.vehicle_entry.get()
                cmd3 = 'sensor_model:=' + upper_frame_tab_three.sensor_entry.get()

                subprocess.run(['python3', 'launch.py', launch_path, cmd1, cmd2, cmd3])


            else:
                launch_exec = subprocess.Popen(['ros2', 'launch', launch_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) #launchファイル起動
                
                # nodeが起動するまで待機
                launch_exec_flag = False
                while launch_exec_flag == False:                         #launchからノードを立ち上げると立ち上がる前に次のsubprocessが実行されるためここで待機
                    time.sleep(1)
                    node_list_exec = subprocess.run(['ros2', 'node', 'list'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)       #起動したノード名を取得
                    node_list = node_list_exec.stdout.strip().split('\n') #ros2 node listの結果を1行ずつをリストに格納
                    print(node_list)
                    if len(node_list) > 0:
                        launch_exec_flag = True
                    else:
                        print('waiting for launched node...')

                
                # print(upper_frame_tab_three.rdo_var.get())
                # print(launch_exec.returncode)




        def stop_launch():
            cmd = "ps aux | grep ros | grep -v grep | awk '{ print \"kill -9\", $2 }' | sh"
            result = subprocess.run(cmd, shell=True)


        def filedialog_launch_clicked():
            iDir = os.path.abspath(os.path.dirname(__file__)) #ディレクトリ名取得
            filepath = filedialog.askopenfilename(initialdir=iDir) 
            self.entry0.set(filepath)


        def update_nodelist():
            self.node_env = subprocess.run(['ros2', 'node', 'list'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            self.node_list = self.node_env.stdout.strip().split('\n')
            self.node_list = [node for node in self.node_list if not node.startswith('/caret_trace')]
            self.node_combo["values"] = self.node_list #値を渡す
            self.node_combo.current()



        # ボタンクリックイベント
        def generate_nodecommand():
             #self.node = self.node_combo.get().split()             #getしたノード起動コマンドをrunできるようにリストに変換（node[0] = package_name, node[1] = node_name）
             self.node = self.node_combo.get()
             self.nodelist = self.node.rsplit('/',1) #ネームスペースとノード名に最後の/で分割する
             self.namespace = self.nodelist[0]
             self.nodename = self.nodelist[1]
             self.package = self.pkg_combo.get()
             self.executable = self.exe_combo.get()
             self.remap_yaml = self.remap_yaml_entry.get()
             self.datepath = datepath
             subprocess.run(['python3', 'nodecommand.py', self.package, self.executable, self.namespace, self.nodename, self.remap_yaml, self.datepath])
             print('Generate nodecommand')




        def filedialog_remap_yaml_clicked():
            iDir = os.path.abspath(os.path.dirname(__file__)) #ディレクトリ名取得
            filepath = filedialog.askopenfilename(initialdir=iDir) 
            self.entry_remapyaml.set(filepath)

        def dirdialog_run_node_clicked():
            iDir = os.path.abspath(os.path.dirname(__file__))
            iDirPath = filedialog.askdirectory(initialdir = iDir)
            self.entry_runnode.set(iDirPath)

        def run_node():
            run_node_path = self.run_node_entry.get()
            runnode_gen = subprocess.run(['python3', 'noderun.py', run_node_path])
            print('Run Node')

        def stop_node():
            kill_node_path = self.run_node_entry.get()
            kiiinode_gen = subprocess.run(['python3', 'kill_node.py', kill_node_path])
            print('Kill Node')



        def dirdialog_process_bag_clicked():
            iDir = os.path.abspath(os.path.dirname(__file__))
            iDirPath = filedialog.askdirectory(initialdir = iDir)
            self.entry_processbag.set(iDirPath)

        def process_bag():
            rosbag_path = self.process_bag_entry.get()
            bagfiles = glob.glob(rosbag_path + '/*.db3') #指定したファイルを取得
            self.datepath = datepath
            if bagfiles:
                rosbag_gen = subprocess.run(['python3', 'process_bag.py', rosbag_path, self.datepath])
            else:
                print('please select a rosbag2 folder')

        
        def dirdialog_play_bag_clicked():
            iDir = os.path.abspath(os.path.dirname(__file__))
            iDirPath = filedialog.askdirectory(initialdir = iDir)
            self.entry_playbag.set(iDirPath)


        def play_bag():
            rosbagplay_path = self.play_bag_entry.get()
            bagfiles = glob.glob(rosbagplay_path + '/*.db3') #指定したファイルを取得
            rate =  self.rate_bag_entry.get()
            if bagfiles:
                rosbagplay_gen = subprocess.run(['python3', 'play_bag.py', rosbagplay_path, rate])
                print('End Play')
            else:
                print('please select a rosbag2 folder')


        def kill_node():
            subprocess.run(['killall', '-2', self.node[1]], stdin=subprocess.DEVNULL)
            self.launch_log.close()
            print('trace stop', f'kill {self.node[1]}', sep='\n')
            self.node_combo["state"] = "normal"

        def change_node_list(var, indx, mode):
            value = self.sv1.get()
            self.narrow_down = [data for data in self.node_list if value in data]
            self.node_combo["values"] = self.narrow_down

        def change_pkg_list(var, indx, mode):
            value = self.sv2.get()
            self.narrow_down = [data for data in self.pkg_list if data.startswith(value)]
            self.pkg_combo["values"] = self.narrow_down
            
            for v in self.pkg_list:
                if v == self.pkg_combo.get():
                    self.exe_env = subprocess.run(['ros2', 'pkg', 'executables', v], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    self.exe_list = self.exe_env.stdout.strip().split('\n')

                    break

                else:
                    self.exe_list = ''
                    self.exe_combo.delete(0,tk.END)
                        

            self.new_exe_list = [s.split(' ')[-1] for s in self.exe_list] #self.exe_listの各要素を半角で分割して、一番うしろの文字列を抽出
            self.exe_combo["values"] = self.new_exe_list #値を渡す [v,c]
            self.exe_combo.current()


        def change_exe_list(var, indx, mode):
            value = self.sv3.get()
            self.narrow_down = [data for data in self.new_exe_list if data.startswith(value)]
            self.exe_combo["values"] = self.narrow_down



        super().__init__(master)

        #起動したときに実行

        aaa = UpperFrame_tab_three()


        self.launch_label = tk.Label(self, text = "SelectLaunchFile")
        self.launch_label.grid(row=0, column=0, padx=2, pady=2)


        self.entry0 = StringVar()
        self.launch_entry = tk.Entry(self, textvariable=self.entry0, width=50)
        self.launch_entry.grid(row=0, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)


        self.btn03 = ttk.Button(self, text="Search", command=filedialog_launch_clicked, width=10)
        self.btn03.grid(row=0, column=3, padx=2, pady=2)

        self.btn04 = ttk.Button(self, text="Start", command=lambda:[start_launch(), self.btn04.grid_remove(),self.btn05.grid(row=0, column=4, padx=2, pady=2)])
        self.btn04.grid(row=0, column=4, padx=2, pady=2)

        self.btn05 = tk.Button(self, text='Stop', command=lambda:[stop_launch(), self.btn05.grid_remove(), self.btn04.grid()])


        self.sv1 = tk.StringVar()  #ウィジェット変数
        self.sv1.trace_add("write", change_node_list)  #ウィジェットに対する操作に対して自動的に特定の処理を実行させる

        self.node_label = tk.Label(self, text = "TargetNode")
        self.node_label.grid(row=1, column=0, padx=2, pady=2)

        self.node_combo = ttk.Combobox(self, state='normal', width=50, textvariable=self.sv1)
        self.node_combo.grid(row=1, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.node_env = subprocess.run(['ros2', 'node', 'list'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.node_list = self.node_env.stdout.strip().split('\n')

        self.node_combo["values"] = self.node_list #値を渡す
        self.node_combo.current()

        self.btn13 = ttk.Button(self, text="Update", command=update_nodelist, width=10)
        self.btn13.grid(row=1, column=3, padx=2, pady=2)


        self.sv2 = tk.StringVar()  #ウィジェット変数
        self.sv2.trace_add("write", change_pkg_list)  #ウィジェットに対する操作に対して自動的に特定の処理を実行させる

        self.pkg_label = tk.Label(self, text = "Targetpkg")
        self.pkg_label.grid(row=2, column=0, padx=2, pady=2)

        self.pkg_combo = ttk.Combobox(self, state='normal', width=50, textvariable=self.sv2)
        self.pkg_combo.grid(row=2, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.pkg_env = subprocess.run(['ros2', 'pkg', 'list'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.pkg_list = self.pkg_env.stdout.strip().split('\n')

        self.pkg_combo["values"] = self.pkg_list #値を渡す
        self.pkg_combo.current()


        self.sv3 = tk.StringVar()  #ウィジェット変数
        self.sv3.trace_add("write", change_exe_list)  #ウィジェットに対する操作に対して自動的に特定の処理を実行させる

        self.exe_label = tk.Label(self, text = "Targetexe")
        self.exe_label.grid(row=3, column=0, padx=2, pady=2)

        self.exe_combo = ttk.Combobox(self, state='normal', width=50, textvariable=self.sv3)
        self.exe_combo.grid(row=3, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)



        self.remap_yaml_label = tk.Label(self, text = "Remap_yaml")
        self.remap_yaml_label.grid(row=4, column=0, padx=2, pady=2)

        self.entry_remapyaml = StringVar()
        self.remap_yaml_entry = tk.Entry(self, textvariable=self.entry_remapyaml, width=50)
        self.remap_yaml_entry.grid(row=4, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.btn43 = ttk.Button(self, text="Search", command=filedialog_remap_yaml_clicked, width=10)
        self.btn43.grid(row=4, column=3, padx=2, pady=2)


        self.btn44 = tk.Button(self, text='Generate', command=generate_nodecommand) #処理を順に
        self.btn44.grid(row=4, column=4, padx=2, pady=2)



        self.run_node_label = tk.Label(self, text = "Run_node")
        self.run_node_label.grid(row=5, column=0, padx=2, pady=2)

        self.entry_runnode = StringVar()
        self.run_node_entry = tk.Entry(self, textvariable=self.entry_runnode, width=50)
        self.run_node_entry.grid(row=5, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.btn53 = ttk.Button(self, text="Search", command=dirdialog_run_node_clicked, width=10)
        self.btn53.grid(row=5, column=3, padx=2, pady=2)

        self.btn54 = ttk.Button(self, text="Run", command=lambda:[run_node(), self.btn54.grid_remove(),self.btn55.grid(row=5, column=4, padx=2, pady=2)])
        self.btn54.grid(row=5, column=4, padx=2, pady=2)

        self.btn55 = tk.Button(self, text='Stop', command=lambda:[stop_node(), self.btn55.grid_remove(), self.btn54.grid()])

        #空間を開けるためのダミー
        self.run_node_label = tk.Label(self, text = "")
        self.run_node_label.grid(row=6, column=0, padx=2, pady=2)


        self.process_bag_label = tk.Label(self, text = "Process_bag")
        self.process_bag_label.grid(row=7, column=0, padx=2, pady=2)

        self.entry_processbag = StringVar()
        self.process_bag_entry = tk.Entry(self, textvariable=self.entry_processbag, width=50)
        self.process_bag_entry.grid(row=7, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.btn73 = ttk.Button(self, text="Search", command=dirdialog_process_bag_clicked, width=10)
        self.btn73.grid(row=7, column=3, padx=2, pady=2)

        self.btn74 = ttk.Button(self, text="Process", command=process_bag, width=10)
        self.btn74.grid(row=7, column=4, padx=2, pady=2)


        self.play_bag_label = tk.Label(self, text = "Play_bag")
        self.play_bag_label.grid(row=8, column=0, padx=2, pady=2)

        self.entry_playbag = StringVar()
        self.play_bag_entry = tk.Entry(self, textvariable=self.entry_playbag, width=50)
        self.play_bag_entry.grid(row=8, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.btn83 = ttk.Button(self, text="Search", command=dirdialog_play_bag_clicked, width=10)
        self.btn83.grid(row=8, column=3, padx=2, pady=2)

        self.btn84 = ttk.Button(self, text="Play", command=play_bag, width=10)
        self.btn84.grid(row=8, column=4, padx=2, pady=2)

        self.rate_bag_label = tk.Label(self, text = "Rate")
        self.rate_bag_label.grid(row=9, column=0, padx=1, pady=1)

        self.entry_ratebag = StringVar()
        self.rate_bag_entry = tk.Entry(self, textvariable=self.entry_ratebag, width=5)
        self.rate_bag_entry.grid(row=9, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)
        self.rate_bag_entry.insert(0,'1.0')






class UpperFrame_tab_two(tk.Frame):
    def __init__(self, master=None):

        
        def trace():
            self.tracedata_name = self.tracedata_name_entry.get()
            # export_path = os.getenv('LD_PRELOAD')
            start_trace.generate_tracedata(self.tracedata_name, datepath)
           


        def dirdialog_select_tracedata_clicked():
            iDir = os.path.abspath(os.path.dirname(__file__))
            iDirPath = filedialog.askdirectory(initialdir = iDir)
            self.entry_selecttracedata.set(iDirPath)


        def generate_architecturefile():
            self.select_tracedata = self.select_tracedata_entry.get()
            architecture.generate_architecture(self.select_tracedata, datepath)
            print('Generate architecturefile')


        def dirdialog_tracedata_clicked():
            iDir = os.path.abspath(os.path.dirname(__file__))
            iDirPath = filedialog.askdirectory(initialdir = iDir)
            self.entry_tracedata.set(iDirPath)

        def filedialog_architecturefile_clicked():
            iDir = os.path.abspath(os.path.dirname(__file__)) #ディレクトリ名取得
            filepath = filedialog.askopenfilename(initialdir=iDir) 
            self.entry_architecturefile.set(filepath)

        def genarate_app():
            self.arcitecturefile = self.architecturefile_entry.get()
            # print(self.arcitecturefile)
            # print(type(self.arcitecturefile))
            self.tracedata = self.tracedata_entry.get()
            self.arch = Architecture('yaml', self.arcitecturefile)
            self.lttng = Lttng(self.tracedata)
            self.app = Application(self.arch, self.lttng)
            self.trace_node_list = self.app.node_names
            if '/rosbag2_player' in self.trace_node_list:
                self.trace_node_list.remove('/rosbag2_player')
            self.trace_node_combo["values"] = self.trace_node_list #値を渡す
            self.source_node_combo["values"] = self.trace_node_list #値を渡す
            self.source_node_combo.current() 
            self.end_node_combo["values"] = self.trace_node_list #値を渡す
            self.end_node_combo.current()  


        def change_trace_node(var, indx, mode):
            value = self.trace_nodename.get()
            self.narrow_down = [data for data in self.trace_node_list if data.startswith(value)]
            self.trace_node_combo["values"] = self.narrow_down


        def callback_window():
            global list_chk
            global get_callback_list
            global bln
            list_chk = []
            irow = 2
            irow0 = 2

            value = self.trace_node_combo.get()

            if value == "":
                get_callback_list = self.app.callback_names
                            
            else:
                node = self.app.get_node(value)
                get_callback_list = node.callback_names

            num_list = len(get_callback_list)
            if num_list < 9:
                canvas_height = 23 * num_list
            elif num_list >= 9:
                canvas_height = 200

            self.callback_window = tk.Toplevel()
            self.callback_window.geometry("530x270")
            self.callback_window.title("callback_Select")
            
            button_frame = tk.Frame(self.callback_window)
            button_frame.grid(row=0,column=0,sticky=tk.W)

            allSelectButton = tk.Button(button_frame, text="All_Select", command=allSelect_click)
            allSelectButton.grid(row=0, column=0,sticky=tk.W)

            alldeleteButton = tk.Button(button_frame, text="Select_Clear", command=allDelete_click)
            alldeleteButton.grid(row=0, column=1,sticky=tk.W)

            canvas = tk.Canvas(self.callback_window,width=500,height=canvas_height,bg='white')
            canvas.grid(row=1,column=0)

            ybar = tk.Scrollbar(self.callback_window,orient=tk.VERTICAL)
            ybar.grid(row=1,column=1,sticky=tk.N + tk.S + tk.W)
            ybar.config(command=canvas.yview)
            canvas.config(yscrollcommand=ybar.set)
            canvas_height = 23 * num_list
            canvas.config(scrollregion=(0, 0, 700, canvas_height))

            canvas_frame = tk.Frame(canvas,bg='white')

            canvas.create_window((0,0),window=canvas_frame,anchor=tk.NW,width=500)


            for callbacks in get_callback_list:
                if irow%2==0:
                    color='#d3cdff'
                else:
                    color='white'
                bln = tk.BooleanVar()
                bln.set(False)
                check_box = tk.Checkbutton(canvas_frame,variable = bln,width=5,text='',background=color)
                list_chk.append(bln)
                check_box.grid(row=irow,column=0,padx=0,pady=0,ipadx=0,ipady=0)
                #callback名
                a1 = callbacks
                b1 = tk.Label(canvas_frame,width=100,text=a1,anchor='w',background=color)
                b1.grid(row=irow,column=1,padx=0,pady=0,ipadx=0,ipady=0)

                irow += 1

        def allSelect_click():
            for i in range(len(list_chk)):
                list_chk[i].set(True)

        def allDelete_click():
            for i in range(len(list_chk)):
                list_chk[i].set(False)


        def visualization_callback():
            self.callbackname = ""
            i = 0
            for callback_status in get_callback_list:
                bln_status = list_chk[i].get()
                if bln_status == True:
                    self.callbackname += callback_status + ","
                i += 1
            self.callbackname = self.callbackname[:-1]
            self.now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") #時間を文字列に
            # export_path = os.getenv('LD_PRELOAD')
            # if os.getenv('LD_PRELOAD'):
            #     del os.environ['LD_PRELOAD']
            visualize_callback.visualize(self.callbackname, self.latency_bln.get(), self.frequency_bln.get(), self.period_bln.get(), self.app, datepath, self.now)
            # export_path_cmd = 'export LD_PRELOAD=$(readlink -f ' + export_path + ')'
            # env_result = subprocess.run(export_path_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print('Visualization')

        def search_paths():
            self.paths = []
            self.paths = self.arch.search_paths(self.source_node_combo.get(),self.end_node_combo.get())
            dict = {(i + 1): self.paths[i] for i in range(0, len(self.paths))}
            self.path_combo["values"] = list(dict.keys()) #値を渡す
            self.path_combo.current() 

        def print_paths():
            self.sub_win = tk.Toplevel()
            self.sub_win.geometry("700x700")
            self.textbox = tk.Text(self.sub_win, width= 50, height= 50)
            self.textbox.grid(row=0, column=0)
            number_path = int(self.path_combo.get())
            self.paths[number_path-1].summary.pprint()
            self.textbox.insert('1.0', self.paths[number_path-1].summary)

        def export_paths():
            number_path = int(self.path_combo.get())
            self.arch.add_path('target_path', self.paths[number_path-1])
            self.arch.export(self.arcitecturefile, force=True)
            self.arch = Architecture('yaml', self.arcitecturefile)
            self.app = Application(self.arch, self.lttng)

        def visualization_paths():
            self.now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") #時間を文字列に
            visualize_paths.visualize(self.message_flow_bln.get(), self.chain_latency_bln.get(), self.response_time_bln.get(), self.app, datepath, self.now)
      
        super().__init__(master)


        self.tracedata_name_label = tk.Label(self, text = "Tracedata_name")
        self.tracedata_name_label.grid(row=0, column=0, padx=2, pady=2)

        self.entry_tracedataname = StringVar()
        self.tracedata_name_entry = tk.Entry(self, textvariable=self.entry_tracedataname, width=50)
        self.tracedata_name_entry.grid(row=0, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.btn03 = ttk.Button(self, text="Trace", command=trace, width=10)
        self.btn03.grid(row=0, column=3, padx=2, pady=2)


        self.select_tracedata_label = tk.Label(self, text = "Select_tracedata")
        self.select_tracedata_label.grid(row=1, column=0, padx=2, pady=2)

        self.entry_selecttracedata = StringVar()
        self.select_tracedata_entry = tk.Entry(self, textvariable=self.entry_selecttracedata, width=50)
        self.select_tracedata_entry.grid(row=1, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.btn13 = ttk.Button(self, text="Search", command=dirdialog_select_tracedata_clicked, width=10)
        self.btn13.grid(row=1, column=3, padx=2, pady=2)

        self.btn14 = ttk.Button(self, text="Generate", command=generate_architecturefile, width=25)
        self.btn14.grid(row=1, column=4, padx=2, pady=2)

        #空間を開けるためのダミー
        self.run_node_label = tk.Label(self, text = "")
        self.run_node_label.grid(row=2, column=0, padx=2, pady=2)

        self.tracedata_label = tk.Label(self, text = "Select_tracedata")
        self.tracedata_label.grid(row=3, column=0, padx=2, pady=2)

        self.entry_tracedata = StringVar()
        self.tracedata_entry = tk.Entry(self, textvariable=self.entry_tracedata, width=50)
        self.tracedata_entry.grid(row=3, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.btn33 = ttk.Button(self, text="Search", command=dirdialog_tracedata_clicked, width=10)
        self.btn33.grid(row=3, column=3, padx=2, pady=2)


        self.architecturefile_label = tk.Label(self, text = "Select_architecturefile")
        self.architecturefile_label.grid(row=4, column=0, padx=2, pady=2)

        self.entry_architecturefile = StringVar()
        self.architecturefile_entry = tk.Entry(self, textvariable=self.entry_architecturefile, width=50)
        self.architecturefile_entry.grid(row=4, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.btn43 = ttk.Button(self, text="Search", command=filedialog_architecturefile_clicked, width=10)
        self.btn43.grid(row=4, column=3, padx=2, pady=2)

        self.btn_genarate_app = ttk.Button(self, text="OK", command=genarate_app, width=10)
        self.btn_genarate_app.grid(row=4, column=4, padx=2, pady=2)





        #空間を開けるためのダミー
        self.run_node_label = tk.Label(self, text = "")
        self.run_node_label.grid(row=5, column=0, padx=2, pady=2)

        self.trace_nodename = tk.StringVar()  #ウィジェット変数
        self.trace_nodename.trace_add("write", change_trace_node)  #ウィジェットに対する操作に対して自動的に特定の処理を実行させる

        self.trace_node_label = tk.Label(self, text = "Node")
        self.trace_node_label.grid(row=6, column=0, padx=2, pady=2)

        self.trace_node_combo = ttk.Combobox(self, state='normal', width=50, textvariable=self.trace_nodename)
        self.trace_node_combo.grid(row=6, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)


        self.btn_callback_list = ttk.Button(self, text="callback_list", command=callback_window, width=10)
        self.btn_callback_list.grid(row=6, column=3, padx=2, pady=2)


        self.latency_bln = tk.BooleanVar()
        self.latency_bln.set(True)

        self.latency_chk = tk.Checkbutton(self, variable=self.latency_bln, text='Latency')
        self.latency_chk.grid(row=7, column=0, padx=2, pady=2)

        self.frequency_bln = tk.BooleanVar()
        self.frequency_bln.set(False)

        self.frequency_chk = tk.Checkbutton(self, variable=self.frequency_bln, text='Frequency')
        self.frequency_chk.grid(row=7, column=1, padx=2, pady=2)

        self.period_bln = tk.BooleanVar()
        self.period_bln.set(False)

        self.period_chk = tk.Checkbutton(self, variable=self.period_bln, text='Period')
        self.period_chk.grid(row=7, column=2, padx=2, pady=2)

        self.btn_visualization_callback = ttk.Button(self, text="Visualize", command=visualization_callback, width=25)
        self.btn_visualization_callback.grid(row=7, column=4, padx=2, pady=2)

        self.btn_visualization_paths = ttk.Button(self, text="Visualize", command=visualization_paths, width=25)
        self.btn_visualization_paths.grid(row=12, column=4, padx=2, pady=2)


        self.source_nodename = tk.StringVar()  #ウィジェット変数
  
        self.source_node_label = tk.Label(self, text = "Source_Node")
        self.source_node_label.grid(row=9, column=0, padx=2, pady=2)

        self.source_node_combo = ttk.Combobox(self, state='normal', width=50, textvariable=self.source_nodename)
        self.source_node_combo.grid(row=9, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)
    

        self.end_nodename = tk.StringVar()  #ウィジェット変数
  
        self.end_node_label = tk.Label(self, text = "End_Node")
        self.end_node_label.grid(row=10, column=0, padx=2, pady=2)

        self.end_node_combo = ttk.Combobox(self, state='normal', width=50, textvariable=self.end_nodename)
        self.end_node_combo.grid(row=10, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)


        self.btn_search_paths = ttk.Button(self, text="Search_paths", command=search_paths, width=10)
        self.btn_search_paths.grid(row=10, column=3, padx=2, pady=2)


        self.path_name = tk.StringVar()  #ウィジェット変数
  
        self.path_label = tk.Label(self, text = "Path")
        self.path_label.grid(row=11, column=0, padx=2, pady=2)

        self.path_combo = ttk.Combobox(self, state='normal', width=50, textvariable=self.path_name)
        self.path_combo.grid(row=11, column=1, columnspan=2, padx=2, pady=2, sticky=tk.W + tk.E)

        self.btn_print_paths = ttk.Button(self, text="Print_paths", command=print_paths, width=10)
        self.btn_print_paths.grid(row=11, column=3, padx=2, pady=2)

        self.btn_export_paths = ttk.Button(self, text="Export_paths", command=export_paths, width=25)
        self.btn_export_paths.grid(row=11, column=4, padx=2, pady=2)

        self.message_flow_bln = tk.BooleanVar()
        self.message_flow_bln.set(True)

        self.message_flow_chk = tk.Checkbutton(self, variable=self.message_flow_bln, text='Message flow')
        self.message_flow_chk.grid(row=12, column=0, padx=2, pady=2)

        self.chain_latency_bln = tk.BooleanVar()
        self.chain_latency_bln.set(False)

        self.chain_latency_chk = tk.Checkbutton(self, variable=self.chain_latency_bln, text='Chain latency')
        self.chain_latency_chk.grid(row=12, column=1, padx=2, pady=2)

        self.response_time_bln = tk.BooleanVar()
        self.response_time_bln.set(False)

        self.response_time_chk = tk.Checkbutton(self, variable=self.response_time_bln, text='Response time')
        self.response_time_chk.grid(row=12, column=2, padx=2, pady=2)

        self.btn_visualization_paths = ttk.Button(self, text="Visualize", command=visualization_paths, width=25)
        self.btn_visualization_paths.grid(row=12, column=4, padx=2, pady=2)


        
class UpperFrame_tab_three(tk.Frame):
    def __init__(self, master=None):

        def filedialog_clicked():
            iDir = os.path.abspath(os.path.dirname(__file__)) #ディレクトリ名取得
            fld = filedialog.askdirectory(initialdir=iDir) 
            self.mapfld.set(fld)

        def pri():
            print(self.rdo_var.get())

        super().__init__(master)


        
        # チェック有無変数
        self.rdo_var = IntVar()
        # value=0のラジオボタンにチェックを入れる
        self.rdo_var.set(0)

        # ラジオボタン作成
        self.rdo1 = tk.Radiobutton(self, value=0, variable=self.rdo_var, text='autoware')
        self.rdo1.grid(row=0, column=0, padx=2, pady=2)

        self.rdo2 = tk.Radiobutton(self, value=1, variable=self.rdo_var, text='other')
        self.rdo2.grid(row=0, column=1, padx=2, pady=2)




        self.map_label = tk.Label(self, text = "SelectMap")
        self.map_label.grid(row=1, column=0, padx=2, pady=2)

        self.mapfld = StringVar()
        self.map_entry = tk.Entry(self, textvariable=self.mapfld, width=58)
        self.map_entry.grid(row=1, column=1, columnspan=3, padx=2, pady=2)

        self.btn0 = ttk.Button(self, text="Search", command=filedialog_clicked, width=10)
        self.btn0.grid(row=1, column=4, padx=2, pady=2)


        self.vehicle_label = tk.Label(self, text = "Selectvehiclemodel")
        self.vehicle_label.grid(row=2, column=0, padx=2, pady=2)

        self.vehiclename = StringVar()
        self.vehiclename.set('sample_vehicle')
        self.vehicle_entry = tk.Entry(self, textvariable=self.vehiclename, width=58)
        self.vehicle_entry.grid(row=2, column=1, columnspan=3, padx=2, pady=2)


        self.sensor_label = tk.Label(self, text = "Selectsensormodel")
        self.sensor_label.grid(row=3, column=0, padx=2, pady=2)

        self.sensorname = StringVar()
        self.sensorname.set('sample_sensor_kit')
        self.sensor_entry = tk.Entry(self, textvariable=self.sensorname, width=58)
        self.sensor_entry.grid(row=3, column=1, columnspan=3, padx=2, pady=2)



def click_close():
    print('exit')

    global i_click_close
    i_click_close = 1

    # ret1 = tk.messagebox.askyesno(
    #     title = "End Confirmation",
    #     message = "Do you really want to close it?")

    # if ret1 == True:

    # 終了確認のメッセージ表示
    ret2 = tk.messagebox.askyesno(
        title = "End Confirmation",
        message = "Save folder?")

    if ret2 == True:
        # 「yes」がクリックされたとき
        pass
    else:
        shutil.rmtree(datepath)

    root.destroy()



root = tk.Tk()
root.geometry("1000x700")

notebook = ttk.Notebook(root)

tab_one = tk.Frame(notebook)
tab_two = tk.Frame(notebook)
tab_three = tk.Frame(notebook)

notebook.add(tab_one, text="node & bag")
notebook.add(tab_two, text="trace")
notebook.add(tab_three, text="autoware")


notebook.pack(anchor="nw")



upper_frame_tab_one = UpperFrame_tab_one(tab_one)
upper_frame_tab_one.pack(padx=2, pady=2, anchor=tk.W)
upper_frame_tab_one.node_combo.selection_clear()


upper_frame_tab_two = UpperFrame_tab_two(tab_two)
upper_frame_tab_two.pack(padx=2, pady=2, anchor=tk.W)

upper_frame_tab_three = UpperFrame_tab_three(tab_three)
upper_frame_tab_three.pack(padx=2, pady=2, anchor=tk.W)



date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") #GUI起動時の時間を文字列に

dir = "output"
if not os.path.exists(dir): # ディレクトリoutputが存在するか確認
    os.makedirs(dir) # ディレクトリoutput作成

os.chdir(os.path.abspath(dir)) #outputへ移動

if not os.path.exists(date): # ディレクトリがdate存在するか確認
    os.makedirs(date) # ディレクトリdate作成
    datepath = os.path.abspath(date) #dateまでのpath取得

os.chdir("../") #ディレクトリをこのファイルに戻す

i_click_close = 0

root.protocol("WM_DELETE_WINDOW", click_close)


try:
    root.mainloop()

finally:
    # 終了確認のメッセージ表示
    if i_click_close == 0:
        print('exit')
        ret = tk.messagebox.askyesno(
            title = "End Confirmation",
            message = "Save folder?")

        if ret == True:
            # 「yes」がクリックされたとき
            pass
        else:
            shutil.rmtree(datepath)