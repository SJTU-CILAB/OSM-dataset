import os
import pandas as pd

def count_nodes_edges():
    current_folder = os.getcwd()
    city_stats = {}
    
    for city_folder in os.listdir(current_folder):
        city_path = os.path.join(current_folder, city_folder)
        if os.path.isdir(city_path):
            node_file = os.path.join(city_path, 'osm_node.csv')
            edge_file = os.path.join(city_path, 'osm_edge1.csv')
            
            if os.path.exists(node_file) and os.path.exists(edge_file):
                nodes = pd.read_csv(node_file, skiprows=1)
                edges = pd.read_csv(edge_file, skiprows=1)
                
                num_nodes = nodes.shape[0]
                num_edges = edges.shape[0]
                
                city_stats[city_folder] = {'nodes': num_nodes, 'edges': num_edges}
            else:
                missing_files = []
                if not os.path.exists(node_file):
                    missing_files.append('osm_node.csv')
                if not os.path.exists(edge_file):
                    missing_files.append('osm_edge1.csv')
                print(f"Skipping {city_folder} due to missing files: {', '.join(missing_files)}")
    
    return city_stats

stats = count_nodes_edges()

results = []
for city, count in stats.items():
    results.append([city, count['nodes'], count['edges']])
    print(f"City: {city}, Nodes: {count['nodes']}, Edges: {count['edges']}")

df = pd.DataFrame(results, columns=['City', 'Nodes', 'Edges'])
df.to_csv('num.csv', index=False)

