import subprocess
import os

def generate_tracedata(tracedata_name, datepath):

	print(tracedata_name)
	my_env = os.environ.copy()
	my_env["ROS_TRACE_DIR"] = datepath #環境変数の設定、subprocessでこの設定を引き継げる

	# str(export_path)
	# print(export_path)

	# export_path_cmd = '$(readlink -f ' + export_path + ')'
	# my_env = os.environ.copy()
	# my_env["LD_PRELOAD"] = export_path_cmd
	
	tracecmd = 'ros2 caret record -s ' + tracedata_name
	subprocess.Popen(tracecmd, shell=True, env=my_env)