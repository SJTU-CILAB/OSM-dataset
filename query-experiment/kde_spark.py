from __future__ import print_function

import sys
import numpy as np
import math
import time
from pyspark import SparkContext

sdata = []
window_check = True

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

    eu_dis = math.sqrt((lon2 - lon1) ** 2+(lat2 - lat1) ** 2)
    alpha = alpha_dict[abs(int(lat1))]
    return alpha * eu_dis

def gaussian_kernel(distance, bandwidth):

    logStandardDeviationPlusHalfLog2Pi = math.log(bandwidth) + 0.5 * math.log(2 * math.pi)
    gaussian_value = math.exp( (-1/2)  *  (distance/ bandwidth) *  (distance/ bandwidth) - logStandardDeviationPlusHalfLog2Pi)
    return gaussian_value

def kdemean(p0,p1,w, centers,window_check=True,bandwith=20):
    kde = 0.0

    filter_points = []
    if window_check:
        ws=centers[:,2]
        filter_points.extend( centers[  (ws == w) ^ (ws + 1 == w) ^ (ws + 900 == w) ^ (ws + 901 == w) ^ (ws + 899 == w) ^ (ws -1  == w) ^ (ws - 900 == w) ^ (ws - 901 == w) ^ (ws - 899 == w)  ])
        #filter_points.extend( centers[ ws  ==  w])
        #filter_points.extend( centers[ ws + 1 == w ])
        #filter_points.extend( centers[ ws + 900 == w ])
        #filter_points.extend( centers[ ws + 901 == w ])
        #filter_points.extend( centers[ ws - 1  == w ])
        #filter_points.extend( centers[ ws - 900 == w ])
        #filter_points.extend( centers[ ws - 901 == w ])
        #filter_points.extend( centers[ ws - 899 == w ])
        #filter_points.extend( centers[ ws + 899 == w ])
    else:
        filter_points = centers

    for i in range(len(filter_points)):

        dis = distance2(p0,p1,filter_points[i][0], filter_points[i][1])
        if dis < bandwith:
            kde += gaussian_kernel(dis,bandwith)

    return kde

def partitionFunction(pDatas):

   results = []
   for item in pDatas:
       kdes = kdemean(item[0],item[1],item[2],sdata,window_check)
       temp=(item[0],item[1],kdes)
       results.append(temp)

   return results

def mapFunction(pData):

   lst = pData.split(',')
   return (float(lst[0]),float(lst[1]),int(lst[2]))

def saveFile(fileName,datas):

    file_csv = open(fileName,'w')
    print("Saving file: ",fileName)

    for item in datas:
        file_csv.writelines(str(item[0]) + ',' + str(item[1]) + ',' + str(item[2]) + '\n')
    file_csv.close()

if __name__ == "__main__":

    if len(sys.argv) != 4 or (sys.argv[2] !='1' and sys.argv[2] !='0') :
        print("Usage: kde <file> <check_window(1 or 0)> <partition_count", file=sys.stderr)
        exit(-1)

    time1 = time.time()
    sc = SparkContext(appName="PythonKDE")
    #data = np.loadtxt(sys.argv[1],
    #        dtype={'names': ('lon', 'lat', 'window'),
    #        'formats': ('f4', 'f4', 'i')},delimiter=',')
    #data = sc.textFile(sys.argv[1],6).map(
    #    lambda p: ( float(p.split(',')[0]),float(p.split(',')[1]),int(p.split(',')[2]) )
    #).cache()
    data = sc.textFile(sys.argv[1],int(sys.argv[3])).map(mapFunction).cache()
    #kPoints = data.take(data.count())
    sdata = np.asarray(data.take(data.count()))
    #############################################################################
    # without window
    #############################################################################
    print("########################################################")
    print("########################################################")

    window_check = bool(int(sys.argv[2]))
    #kdes = sc.parallelize(data,6).map(
    #        lambda p: (p[0],p[1],kdemean(p[0],p[1],p[2],data,check_window))).collect()
    #kdes = sc.parallelize(data,6).mapPartitions(partitionFunction).collect()
    kdes = data.mapPartitions(partitionFunction).collect()
    saveFile('./spark_result.csv',kdes)
    time2 = time.time()
    #for p in kdes:
    #    #if p[2] > 0.0:
    #     print(str(p))
    print("########################################################")
    if window_check:
        print("spark multi core, " + sys.argv[1] + " with window check, " + str(time2-time1))
    else:
        print("spark multi core, " + sys.argv[1] +" without window check, "+ str(time2-time1))
    #print("########################################################")

    #end spark
    sc.stop()