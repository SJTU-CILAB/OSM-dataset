import time
import pandas as pd
import osmnx as ox
import datetime
import json
import os
import codecs
import numpy as np
import codecs
import multiprocessing

os.mkdir('/workspace/nodes')
os.mkdir('/workspace/edges')
os.mkdir('/workspace/temp_osm')
loadpath = '/workspace/osm'
osm_savepath = '/workspace/temp_osm'
node_csv_savepath = '/workspace/nodes'
edge_csv_savepath = '/workspace/edges'


def get_header(path, file):
    header = []
    start_line = 0
    f = codecs.open(path + '/' + file, 'r', encoding='utf-8')
    for line in f:
        # print(line)
        if line.startswith('  <node id=') or line.startswith('  <way id=') or line.startswith('  <relation id='):
            f.close()
            return header, start_line
        else:
            header.append(line)
            start_line += 1


def osm_to_csv(header, linelist, file, block_id):
    time1 = time.time()
    continent_name = file.rsplit('-', 1)[0].replace('-', '_')
    temp_osm_name = continent_name + '_{}.osm'.format(block_id)

    new_linelist = [line_string.replace('@', 'at').replace('&#x', '').replace('\u2029', '').replace('\u2028', '') for line_string in linelist]  # replace all '@' and line seperator in osm file
    sum_list = header + new_linelist
    sum_list.append('</osm>')
    temp_file = codecs.open(osm_savepath + '/' + temp_osm_name, 'w', encoding='utf-8')
    temp_file.writelines(sum_list)
    temp_file.close()
    node_dict, edge_dict = ox.graph_from_xml(osm_savepath + '/' + temp_osm_name, simplify=False, retain_all=True)
    time2 = time.time()
    print('generate {} dict:'.format(continent_name), ', time:', time2 - time1, ', node:', len(node_dict), ', edge:', len(edge_dict))

    if len(node_dict) != 0:
        node_value_list = list(node_dict.values())
        node_dataframe = pd.DataFrame(node_value_list, columns=["osmid", "x", "y", "continent", "name", "aerialway", "aeroway", "amenity", "barrier", "boundary", "admin_level", "building", "entrance", "height", "craft", "emergency", "geological", "healthcare", "highway", "ford", "lit", "historic", "landuse", "leisure", "man_made", "military", "natural", "office", "place", "population", "is_in", "power", "public_transport", "railway", "shop", "sport", "telecom", "tourism", "water", "waterway", "crossing"])
        node_dataframe['continent'] = continent_name
        time3 = time.time()
        print('generate dataframe:{}, time:{}'.format(continent_name + '_edge' + str(block_id), time3 - time2))
        node_dataframe.to_csv(node_csv_savepath + '/' + continent_name + '_{}_node.csv'.format(block_id),
                              index=False, encoding='utf-8-sig', sep='@')
        time4 = time.time()
        print('save csv:{}, time:{}'.format(continent_name + '_node' + str(block_id) + '.csv', time4 - time3))

    time5 = time.time()
    if len(edge_dict) != 0:
        edge_value_list = list(edge_dict.values())
        edge_dataframe = pd.DataFrame(edge_value_list, columns=["osmid", "nodes", "continent", "name", "aerialway", "aeroway", "amenity", "barrier", "boundary", "admin_level", "building", "entrance", "craft", "emergency", "geological", "healthcare", "highway", "footway", "sidewalk", "cycleway", "abutters", "bus_bay", "junction", "lanes", "lit", "motorroad", "oneway", "overtaking", "priority_road", "service", "smoothness", "surface", "turn", "historic", "landuse", "leisure", "man_made", "military", "natural", "office", "place", "population", "is_in", "power", "public_transport", "railway", "usage", "route", "shop", "sport", "telecom", "tourism", "water", "waterway", "area", "bridge", "access", "est_width", "maxwidth", "maxaxleload", "maxheight", "maxlength", "maxstay", "maxweight", "maxspeed", "minspeed"])
        edge_dataframe['continent'] = continent_name
        time6 = time.time()
        print('generate dataframe:{}, time:{}'.format(continent_name + '_edge' + str(block_id), time6 - time5))
        edge_dataframe.to_csv(edge_csv_savepath + '/' + continent_name + '_{}_edge.csv'.format(block_id),
                              index=False, encoding='utf-8-sig', sep='@')
        time7 = time.time()
        print('save csv:{}, time:{}'.format(continent_name + '_edge' + str(block_id) + '.csv', time7 - time6))


time_start = datetime.datetime.now()
for path, dir_list, file_list in os.walk(loadpath):
    pool = multiprocessing.Pool(processes=44)
    for file in file_list:
        with codecs.open(path + '/' + file, 'r', encoding='utf-8') as f:
            header, startline = get_header(path, os.path.basename(file))
            line_number = 0
            line_list = []
            block_id = 0
            for i in range(startline):
                line = f.readline()
                line_number += 1
                # print(line)
            while line:
                line_list.append(line)
                line = f.readline()  # 这里是已经读了下一行了
                line_number += 1
                if line.startswith('  <relation id='):  # 后面的部分都是relation,和点、边无关
                    pool.apply_async(osm_to_csv, args=(header, line_list, os.path.basename(file), block_id))
                    line_list = []
                    block_id = 0
                    break
                if line_number % 400000 == 0:
                    if line.startswith('    <tag k=') or line.startswith('    <nd ref='):
                        while line.startswith('    <tag k=') or line.startswith(
                                '    <nd ref='):  # 下一行如果是以tag或ref开始，就表示节点或边没读完
                            line_list.append(line)
                            line = f.readline()
                            line_number += 1
                        line_list.append(line)
                        line = f.readline()  # 继续读下一行 把node或way的结束符也读进来
                    elif line.startswith('  </node>') or line.startswith('  </way>'):
                        line_list.append(line)
                        line = f.readline()
                    # print(line_list)
                    pool.apply_async(osm_to_csv, args=(header, line_list, os.path.basename(file), block_id))
                    block_id += 1
                    line_list = []  # 清空line_list 供后续使用
        print('finish add all process to pool!:{}'.format(os.path.basename(file)))
    pool.close()
    pool.join()
print('finish all')
time_end = datetime.datetime.now()
print('total time:', time_end - time_start)
