import math
import numpy as np
import codecs
import csv
import time
from tqdm import tqdm

bandwidth = 20.0

def saveFile(fileName,datas):

    file_csv = open(fileName,'w+')
    print("Saving file: ",fileName)

    for item in datas:
        file_csv.writelines(str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + '\n')
    file_csv.close()

alpha_dict = {0: 111.1949, 1: 111.178, 2: 111.1272, 3: 111.0425, 4: 110.9241, 5: 110.7718, 6: 110.5858, 7: 110.3661,
            8: 110.1128, 9: 109.8259, 10: 109.5056, 11: 109.1519, 12: 108.765, 13: 108.3449, 14: 107.8919,
            15: 107.406, 16: 106.8873, 17: 106.3361, 18: 105.7525, 19: 105.1367, 20: 104.4889, 21: 103.8092,
            22: 103.098, 23: 102.3553, 24: 101.5814, 25: 100.7766, 26: 99.9411, 27: 99.0751, 28: 98.179,
            29: 97.253, 30: 96.2973, 31: 95.3123, 32: 94.2983, 33: 93.2556, 34: 92.1844, 35: 91.0852, 36: 89.9582,
            37: 88.8038, 38: 87.6224, 39: 86.4143, 40: 85.1798, 41: 83.9194, 42: 82.6335, 43: 81.3223,
            44: 79.9864, 45: 78.6262, 46: 77.242, 47: 75.8342, 48: 74.4034, 49: 72.9499, 50: 71.4742, 51: 69.9767,
            52: 68.4579, 53: 66.9182, 54: 65.3582, 55: 63.7782, 56: 62.1789, 57: 60.5606, 58: 58.9238,
            59: 57.2691, 60: 55.5969, 61: 53.9078, 62: 52.2023, 63: 50.4809, 64: 48.7441, 65: 46.9925,
            66: 45.2266, 67: 43.4469, 68: 41.6539, 69: 39.8483, 70: 38.0305, 71: 36.2011, 72: 34.3607,
            73: 32.5099, 74: 30.6491, 75: 28.779, 76: 26.9002, 77: 25.0131, 78: 23.1184, 79: 21.2167, 80: 19.3086,
            81: 17.3945, 82: 15.4752, 83: 13.5511, 84: 11.6229, 85: 9.6912, 86: 7.7565, 87: 5.8194, 88: 3.8806,
            89: 1.9406, 90: 0.0}

def distance2(lon1, lat1, lon2, lat2):

    eu_dis = math.sqrt((((lon2 - lon1)) ** 2) + (((lat2 - lat1)) ** 2))
    alpha = alpha_dict[abs(int(lat1))]
    return alpha * eu_dis

def gaussian_kernel(distance, bandwidth):
    logStandardDeviationPlusHalfLog2Pi = math.log(bandwidth) + 0.5 * math.log(2 * math.pi)
    gaussian_value = np.exp( (-1/2)  *  (distance/ bandwidth) *  (distance/ bandwidth) - logStandardDeviationPlusHalfLog2Pi)
    return gaussian_value

def run(points,outfile,check_window = False):
    outdata = []

    xs=points[:,0]
    ys=points[:,1]
    ws=points[:,2]

    for i in tqdm(range(len(xs))):
        x = xs[i]
        y = ys[i]
        w = ws[i]
        kdemean = 0.0

        filter_points = []
        if check_window:

            filter_points.extend( points[ (ws == w) ^ (ws + 1 == w) ^ (ws + 900 == w) ^ (ws + 901 == w) ^ (ws + 899 == w) ^ (ws -1  == w) ^ (ws - 900 == w) ^ (ws - 901 == w) ^ (ws - 899 == w) ])
            #filter_points.extend( points[ ws  ==  w])
            #filter_points.extend( points[ ws + 1 == w ])
            #filter_points.extend( points[ ws + 900 == w ])
            #filter_points.extend( points[ ws + 901 == w ])
            #filter_points.extend( points[ ws - 1  == w ])
            #filter_points.extend( points[ ws - 900 == w ])
            #filter_points.extend( points[ ws - 901 == w ])
            #filter_points.extend( points[ ws - 899 == w ])
            #filter_points.extend( points[ ws + 899 == w ])
        else:
            filter_points = points

        for j in range(len(filter_points)):
            cx = filter_points[j][0]
            cy = filter_points[j][1]  

            dis = distance2(cx, cy, x, y)
            if dis < bandwidth: 
                kdemean += gaussian_kernel(dis,bandwidth)

        point = (x,y,kdemean)
        outdata.append(point)    
    #out file 
    saveFile(outfile,outdata)

#############################################################################
# load osm_100000.csv
#############################################################################
points = np.loadtxt('osm_100000.csv', delimiter=',')
outfile= 'single_core_'

time1 = time.time()
run(points,outfile + 'without_window_' + 'osm_100000.csv',False)
time2 = time.time()
print("Single core,osm_100000 without windows index, time used: ", time2 - time1)

time1 = time.time()
run(points,outfile + 'with_window_' + 'osm_100000.csv',True)
time2 = time.time()
print("Single core,osm_100000 with windows index, time used: ", time2 - time1)

#############################################################################
# load osm_10000.csv
#############################################################################
points = np.loadtxt('osm_10000.csv', delimiter=',')
outfile= 'single_core_'

time1 = time.time()
run(points,outfile + 'without_window_' + 'osm_10000.csv',False)
time2 = time.time()
print("Single core,osm_10000 without windows index, time used: ", time2 - time1)

time1 = time.time()
run(points,outfile + 'with_window_' + 'osm_10000.csv',True)
time2 = time.time()
print("Single core,osm_10000 with windows index, time used: ", time2 - time1)

#############################################################################
# load osm_1000.csv
#############################################################################
points = np.loadtxt('osm_1000.csv', delimiter=',')
outfile= 'single_core_'

time1 = time.time()
run(points,outfile + 'with_window_' + 'osm_10000.csv',True)
time2 = time.time()
print("Single core,osm_1000 with windows index, time used: ", time2 - time1)
