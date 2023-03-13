import os
import glob
import subprocess
import shutil
import re
from distutils.dir_util import copy_tree
import sqlite3
import sys

args = sys.argv

currentdir = os.getcwd()

os.chdir(args[2]) #ディレクトリをバグを生成する場所へ

info_list = ''
sub_topic_list = []
pub_topic_list = []

#ros2 node listで各ノードの情報を取得
node_list_exec = subprocess.run(['ros2', 'node', 'list'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) 
node_list = node_list_exec.stdout.strip().split('\n')

#ros2 node infoの結果から、各ノードのpub、subトピック名の配列を生成
for data in node_list:
    get_info = subprocess.run(['ros2', 'node', 'info', data], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) 
    node_info = get_info.stdout
    info_list += get_info.stdout #複数ノードの情報を合わせたもの、txtに記入される
    txt_lines = node_info.strip().split('\n')
    txt_lines = [data.strip() for data in txt_lines] #各要素の空白文字削除
    # print(txt_lines)
    for i, value in enumerate(txt_lines):
        if i > txt_lines.index('Subscribers:') and i < txt_lines.index('Publishers:'): #subトピック名の取得
            # print(i,value)
            sub_topic_list.append(re.sub(':.*', '', value))
        if i > txt_lines.index('Publishers:') and i < txt_lines.index('Service Servers:'): #pubトピック名の取得
            # print(i,value)
            pub_topic_list.append(re.sub(':.*', '', value))
  

create_nodoinfo = open('node_info.txt', mode = 'w')
create_nodoinfo.writelines(info_list)
create_nodoinfo.close()

#絶対パス取得
filepath = os.path.abspath("node_info.txt")

# リスト内の重複している要素を削除
list(set(sub_topic_list))
list(set(pub_topic_list))


#リスト内の/rosoutと/parameter_eventsの削除
sub_topic_list = [data for data in sub_topic_list if data != '/rosout' and data != '/parameter_events']
pub_topic_list = [data for data in pub_topic_list if data != '/rosout' and data != '/parameter_events']



#subとpubリストを比較、subかつpubで取得したトピック名をsubリストから削除
match_topic_list = []

for elem in sub_topic_list:  #pubリストにあって、subリストにある要素を取得
    if elem in pub_topic_list:
        match_topic_list.append(elem)
# print('subかつpubリスト:', match_topic_list)

for value in match_topic_list:
    sub_topic_list.remove(value)


copy_tree(args[1], "./rosbag2_bag")

# bagファイルのフォルダ内の.bd3拡張子がついているファイルを検索
for file in os.listdir("./rosbag2_bag"):
    base, ext = os.path.splitext(file) #拡張子とそれ以外で分割
    if ext == '.db3':
        db3_name = file
        
db = sqlite3.connect("./rosbag2_bag/" + db3_name, isolation_level=None)


sql = "DELETE FROM topics WHERE"
i = 1
for topic in sub_topic_list:
    sql += " (name != '" + topic + "')"
    if len(sub_topic_list) > i:
      sql += " AND"
      i+=1
    else:
      break

db.execute(sql)

sql = "DELETE FROM messages WHERE topic_id NOT IN  (SELECT id FROM topics)"
db.execute(sql)
db.execute('vacuum;')
db.close()

print('Generate bagfile')

os.chdir(currentdir)

