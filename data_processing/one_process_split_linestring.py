import time
import pandas as pd

import json
import os
import codecs
import numpy as np
import multiprocessing
import osmnx as ox

# os.mkdir('/workspace/edges_split')
# os.mkdir('/workspace/edges_fulltag')
edge_split_save_path = '/workspace/edges_split'
edge_full_tag_save_path = '/workspace/edges_fulltag'
temp_osm_save_path = '/workspace/temp_osm'
file_dir = os.listdir('/workspace/edges')
edge_split_file_list = os.listdir('/workspace/edges_split')
edge_fulltag_file_list = os.listdir('/workspace/edges_fulltag')


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
            # print(len(line_list))
            edge_delete_nodes_line_list = line_list.copy()
            # print(edge_delete_nodes_line_list)
            edge_delete_nodes_line_list.pop(1)
            edge_delete_nodes_line = '@'.join(edge_delete_nodes_line_list)
            edge_delete_nodes_csv.append(edge_delete_nodes_line)  # 逐行删掉nodes属性后加入edge_fulltag
            # print(line_list[1])
            try:
                nodes_list = json.loads(line_list[1])
            except Exception as e:
                print(str(line_list[1]), len(line_list[1]), len(line_list))
                os._exit(0)
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
# pool = multiprocessing.Pool(processes=44)
for file in file_dir:
    if os.path.splitext(file)[0] + '_split.csv' not in edge_split_file_list:
        osm_name = os.path.basename(file).rsplit('_', 1)[0] + '.osm'
        print(osm_name)
        with codecs.open(temp_osm_save_path + '/' + osm_name, 'r', encoding='utf-8') as f:
            osm_list = f.readlines()
            new_osmlist = [line_string.replace('&#x', '').replace('\u2029', '') for line_string in osm_list]

        with codecs.open(temp_osm_save_path + '/' + osm_name, 'w', encoding='utf-8') as f:
            f.writelines(new_osmlist)

        node_dict, edge_dict = ox.graph_from_xml(temp_osm_save_path + '/' + osm_name, simplify=False, retain_all=True)
        continent_name = osm_name.rsplit('_', 1)[0]
        if len(edge_dict) != 0:
            edge_value_list = list(edge_dict.values())
            edge_dataframe = pd.DataFrame(edge_value_list,
                                          columns=["osmid", "nodes", "continent", "name", "aerialway", "aeroway",
                                                   "amenity", "barrier", "boundary", "admin_level", "building",
                                                   "entrance", "craft", "emergency", "geological", "healthcare",
                                                   "highway", "footway", "sidewalk", "cycleway", "abutters", "bus_bay",
                                                   "junction", "lanes", "lit", "motorroad", "oneway", "overtaking",
                                                   "priority_road", "service", "smoothness", "surface", "turn",
                                                   "historic", "landuse", "leisure", "man_made", "military", "natural",
                                                   "office", "place", "population", "is_in", "power",
                                                   "public_transport", "railway", "usage", "route", "shop", "sport",
                                                   "telecom", "tourism", "water", "waterway", "area", "bridge",
                                                   "access", "est_width", "maxwidth", "maxaxleload", "maxheight",
                                                   "maxlength", "maxstay", "maxweight", "maxspeed", "minspeed"])
            edge_dataframe['continent'] = continent_name
            edge_dataframe.to_csv('/workspace/edges/' + file, index=False, encoding='utf-8-sig', sep='@')
            print(os.path.basename(file))
        if len(node_dict) != 0:
            print('{} have nodes!'.format(osm_name))
        edge_dataframe = pd.read_csv('/workspace/edges/' + file, sep='@', low_memory=False)
        split_dataframe = pd.DataFrame(columns=['osmid', 'osmid_start', 'osmid_end'])
        full_tag_dataframe = edge_dataframe.copy()
        column_list = edge_dataframe.columns.to_list()
        print(column_list)

        print(new_dataframe)
        for i in range(len()):
            record = edge_dataframe.loc[i].copy()
            # print(line_string)
            # print(type(line_string))
            nodes_list = json.loads(record['nodes'])
            start_end_list = []
            for j in range(len(nodes_list) - 1):
                start_end_list.append([nodes_list[j], nodes_list[j + 1]])
                start_end_dataframe = pd.DataFrame(data=start_end_list, columns=['start', 'end'])
                repeat_record_dataframe = pd.DataFrame(np.repeat(record, len(nodes_list) - 1), columns=column_list)
                new_dataframe = pd.concat([repeat_record_dataframe, start_end_dataframe])
                # print(len(new_dataframe))
        time2 = time.time()
        new_dataframe = new_dataframe.drop(labels='nodes', axis=1)
        new_dataframe.to_csv('new_aus.csv', index=False, encoding='utf-8-sig', sep='@')

        print(time2 - time1)
print('finish')
