import time
import pandas as pd

import json
import os
import codecs
import numpy as np
import multiprocessing

os.mkdir('/workspace/edges_split')
os.mkdir('/workspace/edges_fulltag')
edge_split_save_path = '/workspace/edges_split'
edge_full_tag_save_path = '/workspace/edges_fulltag'
file_dir = os.listdir('/workspace/edges')


def split_edge_csv(edge_file):
    csv_file_header = os.path.splitext(edge_file)[0]
    edge_delete_nodes_csv = []
    edge_stream_csv = ['osmid@osmid_start@osmid_end\n']
    with codecs.open('/workspace/edges/' + edge_file, encoding='utf-8-sig') as f:
        header_line = f.readline()
        header_line_list = header_line.split('@')
        header_line_list.remove('nodes')
        edge_delete_nodes_header = '@'.join(header_line_list)
        edge_delete_nodes_csv.append(edge_delete_nodes_header)
        line = f.readline()
        while line:
            line_list = line.split('@')
            edge_delete_nodes_line_list = line_list.copy()
            edge_delete_nodes_line_list.pop(1)
            edge_delete_nodes_line = '@'.join(edge_delete_nodes_line_list)
            edge_delete_nodes_csv.append(edge_delete_nodes_line)  # 逐行删掉nodes属性后加入edge_fulltag

            nodes_list = json.loads(line_list[1])
            for i in range(len(nodes_list) - 1):
                edge_stream_line_list = [str(line_list[0]), str(nodes_list[i]), str(nodes_list[i + 1]) + '\n']
                # print(edge_stream_line_list)
                edge_stream_line = '@'.join(edge_stream_line_list)
                edge_stream_csv.append(edge_stream_line)  # 将1行拆成多行，加入edge_split
            line = f.readline()

    with codecs.open(edge_split_save_path + '/' + csv_file_header + '_split.csv', 'w', encoding='utf-8-sig') as f1:
        f1.writelines(edge_stream_csv)
    print('save csv:{}'.format(csv_file_header + '_split.csv'))
    with codecs.open(edge_full_tag_save_path + '/' + csv_file_header + '_fulltag.csv', 'w', encoding='utf-8-sig') as f2:
        f2.writelines(edge_delete_nodes_csv)
    print('save csv:{}'.format(csv_file_header + '_fulltag.csv'))


time1 = time.time()
pool = multiprocessing.Pool(processes=44)
for file in file_dir:
    pool.apply_async(split_edge_csv, args=(file,))
pool.close()
pool.join()
time2 = time.time()
print('time:', time2 - time1)
print('finish all!')
