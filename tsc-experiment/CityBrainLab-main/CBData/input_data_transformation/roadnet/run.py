from src.roadnet_simplify import Roadnet_simplify
from src.data_transform import Data_transform
from src.rm_signal import RemoveSignal


# modify here--------------------------------------------------------------------------------------
node_path = './input/node.csv' # path of input node.csv
edge_from_to_path = './input/edge1.csv' # path of input edge_from_to.csv
edge_level_path = './input/edge2.csv' # path of input edge_level.csv
# reserved_edge_level_set = {'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential', 'unclassified',
#                             'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link'} # reserved road levels
reserved_edge_level_set = {
    'service', 'footway', 'residential', 'pedestrian', 'steps', 'secondary', 'living_street',
    'tertiary', 'primary', 'motorway', 'track', 'motorway_link', 'path', 'unclassified',
    'cycleway', 'secondary_link', 'primary_link', 'trunk', 'construction', 'proposed',
    'tertiary_link', 'trunk_link', 'corridor', 'elevator', 'planned', 'services',
    'bus_stop', 'raceway', 'platform'
}

# --------------------------------------------------------------------------------------------------

output_path = './output' # full path of simplified node.csv and edge.csv and CBEngine roadnet file

# simplify roadnet
roadnet = Roadnet_simplify(node_path = node_path,
                           edge_from_to_path = edge_from_to_path,
                           edge_level_path= edge_level_path,
                           output_path = output_path,
                           reserved_edge_level_set = reserved_edge_level_set,
                           has_columns = False)
roadnet.simplify_roadnet()

# transform data to CBEngine format
CBEngine_roadnet = Data_transform(node_path=output_path + '/node.csv',
                                    edge_path=output_path + '/edge.csv',
                                    directed=False)
CBEngine_roadnet.CBEngine_data_transform(output_path=output_path)
CBEngine_roadnet.Output_roadnet_dict(output_path=output_path)

# 删去所有二叉路口和一叉路口的信号
rm = RemoveSignal(input_path="./output/raw_roadnet.txt", output_path="./output/roadnet.txt")
rm.rm_signal()
