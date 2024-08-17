import subprocess
import multiprocessing
import numpy as np
import os
import codecs

edge_fulltag_listdir = os.listdir('/workspace/edges_fulltag')
edge_split_listdir = os.listdir('/workspace/edges_split')
node_listdir = os.listdir('/workspace/nodes')

nodes_total_length = 0
edge_split_total_length = 0
edge_fulltag_total_length = 0
for i in range(len(node_listdir)):
    with codecs.open('/workspace/nodes/' + node_listdir[i], 'r', encoding='utf-8') as f:
        osm_list = f.readlines()
        nodes_total_length = nodes_total_length + len(osm_list)

print('nodes total length:', nodes_total_length)
print('nodes csv count:', len(node_listdir))
print('node merge csv length:', nodes_total_length - len(node_listdir) + 1)

for i in range(len(edge_split_listdir)):
    with codecs.open('/workspace/edges_split/' + edge_split_listdir[i], 'r', encoding='utf-8') as f:
        osm_list = f.readlines()
        edge_split_total_length = edge_split_total_length + len(osm_list)

print('edge split total length:', edge_split_total_length)
print('edge split csv count:', len(edge_split_listdir))
print('edge split merge csv length:', edge_split_total_length - len(edge_split_listdir) + 1)

for i in range(len(edge_fulltag_listdir)):
    with codecs.open('/workspace/edges_fulltag/' + edge_fulltag_listdir[i], 'r', encoding='utf-8') as f:
        osm_list = f.readlines()
        edge_fulltag_total_length = edge_fulltag_total_length + len(osm_list)

print('edge fulltag total length:', edge_fulltag_total_length)
print('edge fulltag csv count:', len(edge_fulltag_listdir))
print('edge fulltag merge csv length:', edge_fulltag_total_length - len(edge_fulltag_listdir) + 1)