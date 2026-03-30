import argparse
import math
from odps import ODPS
import networkx as nx
import pandas as pd
from odps.tunnel import TableTunnel

def main():
    access_id = 'nStFpOmyIJOZewTe'
    access_key = 'LHn6Meb5R02LLw5PuzeZUvgXJoHNGN'
    project = 'citybrain_prod'
    endpoint = 'http://service.cn-jswx-xuelang-d01.odps.res.cloud.wuxi-yqgcy.cn/api'
    o = ODPS(access_id, access_key, project, endpoint)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('left_lon', type=float)
    parser.add_argument('right_lon', type=float)
    parser.add_argument('down_lat', type=float)
    parser.add_argument('upper_lat', type=float)
    args = parser.parse_args()

    start_lon = args.left_lon
    end_lon = args.right_lon
    start_lat = args.down_lat
    end_lat = args.upper_lat
    
    # o.execute_sql('select count(1) from osm_node_roadnet;')
    o.execute_sql('drop table IF EXISTS node_tmp;')
    o.execute_sql('drop table IF EXISTS edge_tmp1;')
    o.execute_sql('drop table IF EXISTS edge_tmp2;')
    
    o.execute_sql('create table IF NOT EXISTS node_tmp(osmid BIGINT, x FLOAT, y FLOAT);')
    o.execute_sql('create table IF NOT EXISTS edge_tmp1(lsid BIGINT, osmid_start BIGINT, osmid_end BIGINT);')
    o.execute_sql('create table IF NOT EXISTS edge_tmp2(lsid BIGINT, highway STRING);')
    o.execute_sql(f'insert into node_tmp select osmid,x,y from osm_node_roadnet where x>{start_lon} and x<{end_lon} and y>{start_lat} and y<{end_lat};')
    o.execute_sql('insert into edge_tmp1 select lsid, osmid_start, osmid_end from osm_split_edge_roadnet where osmid_start in (select osmid from node_tmp) and osmid_end in (select osmid from node_tmp);')
    o.execute_sql('insert into edge_tmp2 select osmid, highway from osm_fulltag_edge_roadnet where osmid in (select lsid from edge_tmp1);')
    
    t = o.get_table('node_tmp')
    with t.open_reader() as reader:
        pd_df = reader.to_pandas()
        pd_df.to_csv('/root/osm_download/CityBrainLab-main/CBData/input_data_transformation/roadnet/input/node.csv', index=False)
        
    t = o.get_table('edge_tmp1')
    with t.open_reader() as reader:
        pd_df = reader.to_pandas()
        pd_df.to_csv('/root/osm_download/CityBrainLab-main/CBData/input_data_transformation/roadnet/input/edge1.csv', index=False)
    
    t = o.get_table('edge_tmp2')
    with t.open_reader() as reader:
        pd_df = reader.to_pandas()
        pd_df.to_csv('/root/osm_download/CityBrainLab-main/CBData/input_data_transformation/roadnet/input/edge2.csv', index=False)
    
    print("finished!")

if __name__ == "__main__":
    main()