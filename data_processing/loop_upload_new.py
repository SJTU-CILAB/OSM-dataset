import subprocess
import sys
import os
import datetime

sep = '"@"'

edge_fulltag_listdir = os.listdir('/workspace/edge_fulltag_merge')
edge_split_listdir = os.listdir('/workspace/edge_split_merge')
node_listdir = os.listdir('/workspace/node_merge')
time1 = datetime.datetime.now()

# for file in edge_fulltag_listdir:
#     upload_cmd = "/usr/local/odps/bin/odpscmd -e " + "'tunnel upload -h true /workspace/edge_fulltag_merge/" + file + " nsodps_dev.osm_fulltag_edge -fd " + sep + "'"
#     try:
#         ret = subprocess.call(upload_cmd, shell=True)
#     except Exception as e:
#         print(e)
#     if ret != 0:
#         sys.exit(0)
#     print('success upload:', file)
# time2 = datetime.datetime.now()
# for file in edge_split_listdir:
#     upload_cmd = "/usr/local/odps/bin/odpscmd -e " + "'tunnel upload -h true /workspace/edge_split_merge/" + file + " nsodps_dev.osm_split_edge -fd " + sep + "'"
#     try:
#         ret = subprocess.call(upload_cmd, shell=True)
#     except Exception as e:
#         print(e)
#     if ret != 0:
#         sys.exit(0)
#     print('success upload:', file)
time3 = datetime.datetime.now()
for file in node_listdir:
    upload_cmd = "/usr/local/odps/bin/odpscmd -e " + "'tunnel upload -h true " + "/workspace/node_merge/" + file + " nsodps_dev.osm_node -fd " + sep + "'"
    try:
        ret = subprocess.call(upload_cmd, shell=True)
    except Exception as e:
        print(e)
    if ret != 0:
        sys.exit(0)
    print('success upload:', file)
time4 = datetime.datetime.now()

print('upload node time:', time4 - time3)