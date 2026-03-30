
from odps import ODPS
import sys
import os
import codecs
import csv
import subprocess
import time

o = ODPS('nStFpOmyIJOZewTe', 'LHn6Meb5R02LLw5PuzeZUvgXJoHNGN', 'citybrain_prod',
endpoint='http://service.cn-jswx-xuelang-d01.odps.res.cloud.wuxi-yqgcy.cn/api')

ODPSCMD = "/Users/nieo/Desktop/odps/bin/odpscmd -e 'tunnel upload "

SKIP = True

def saveCsvFile(fileName,datas):

    file_csv = codecs.open(fileName,'w','utf-8')
    print("Saving file: ",fileName)

    writer = csv.writer(file_csv, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)

    for i in range(datas.__len__()):
        data = datas[i]
        writer.writerow(data)

def waitInstanceFinish(instance):
    while 1:
        if instance.is_terminated():
            break
        time.sleep(0.1)
    return True

def getODPSTaskCost(instance,task_name='KDEmeanTest'):
    detail2= instance.get_task_detail2(task_name)
    # cost = detail2.get('mapReduce').get('summary').split('\n')[0].split(":")[1]
    cost = detail2.get('mapReduce').get('summary').split('\n')[0].split(":")[0]
    cpu= cost.split(",")[0]
    # mem= cost.split(",")[1]
    mem= cost.split(",")[0]
    return cpu + ',' + mem

#创建结果表
o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)')
o.execute_sql('truncate table osm_roadnet_kde_mean_test')

if not SKIP:
    #############################################################################
    # test osm_100000.csv，1/100000之一采样，19450记录条数，不用索引
    #############################################################################
    time1 = time.time()

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    'select /*+ mapjoin(center) */ ' + \
                                    '       center.x, center.y,kde(point.x,point.y,center.x,center.y,20) as kde ' + \
                                    'from (select x,y,1 as JOIN_ITEM from osm_roadnet_sampling100000) point,(select x,y, 1 as JOIN_ITEM from osm_roadnet_sampling100000) center ' + \
                                    'where point.JOIN_ITEM = center.JOIN_ITEM and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    'group by center.x,center.y ',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_100000 with windows index, time used:", time2 - time1, ' ,cost:',cost.lstrip())


    #############################################################################
    # test osm_10000.csv,1/10000之一采样，194500记录条数，不用索引
    #############################################################################
    time1 = time.time()

    #创建结果表
    #o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)')
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    'select /*+ mapjoin(center) */ ' + \
                                    '       center.x, center.y,kde(point.x,point.y,center.x,center.y,20) as kde ' + \
                                    'from (select x,y,1 as JOIN_ITEM from osm_roadnet_sampling100000) point,(select x,y, 1 as JOIN_ITEM from osm_roadnet_sampling100000) center ' + \
                                    'where point.JOIN_ITEM = center.JOIN_ITEM and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    'group by center.x,center.y ',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_10000 with windows index, time used:", time2 - time1, ' ,cost:',cost.lstrip())

if not SKIP:
    #############################################################################
    # test osm_10000.csv,1/10000之一采样，194500记录条数，不用索引
    #############################################################################
    time1 = time.time()

    #创建结果表
    #o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)')
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    'select /*+ mapjoin(center) */ ' + \
                                    '       center.x, center.y,kde(point.x,point.y,center.x,center.y,20) as kde ' + \
                                    'from (select x,y,1 as JOIN_ITEM from osm_roadnet_sampling100000) point,(select x,y, 1 as JOIN_ITEM from osm_roadnet_sampling100000) center ' + \
                                    'where point.JOIN_ITEM = center.JOIN_ITEM and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    'group by center.x,center.y ',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_10000 with windows index, time used:", time2 - time1, ' ,cost:',cost.lstrip())


#############################################################################
# test osm_10000.csv,1/1000之一采样，1945000记录条数，不用索引
#############################################################################

if not SKIP:
    time1 = time.time()

    #创建结果表
    #o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)')
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    'select /*+ mapjoin(center) */ ' + \
                                    '       center.x, center.y,kde(point.x,point.y,center.x,center.y,20) as kde ' + \
                                    'from (select x,y,1 as JOIN_ITEM from osm_roadnet_sampling1000) point,(select x,y, 1 as JOIN_ITEM from osm_roadnet_sampling1000) center ' + \
                                    'where point.JOIN_ITEM = center.JOIN_ITEM and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    'group by center.x,center.y ',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_1000 with windows index, time used:", time2 - time1, ' ,cost:',cost.lstrip())


if not SKIP:
    #############################################################################
    # test osm_100000.csv，1/100000之一采样，19450记录条数，带索引
    #############################################################################
    time1 = time.time()

    #创建结果表
    #o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)')
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    ' select x,y,sum(kde) ' + \
                                    ' from( ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100000 point, osm_roadnet_sampling100000 center ' + \
                                    '    where point.idx = center.idx and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100000 point, osm_roadnet_sampling100000 center ' + \
                                    '    where point.idx = center.idx + 1 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100000 point, osm_roadnet_sampling100000 center ' + \
                                    '    where point.idx = center.idx + 900 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100000 point, osm_roadnet_sampling100000 center ' + \
                                    '    where point.idx = center.idx + 901 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100000 point, osm_roadnet_sampling100000 center ' + \
                                    '    where point.idx = center.idx - 1  and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100000 point, osm_roadnet_sampling100000 center ' + \
                                    '    where point.idx = center.idx - 901 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100000 point, osm_roadnet_sampling100000 center ' + \
                                    '    where point.idx = center.idx - 900 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100000 point, osm_roadnet_sampling100000 center ' + \
                                    '    where point.idx = center.idx + 899 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100000 point, osm_roadnet_sampling100000 center ' + \
                                    '    where point.idx = center.idx - 899 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    ')                              ' + \
                                    'group by x,y',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_100000 with windows index, time used:", time2 - time1, ' ,cost:',cost.lstrip())

if not SKIP:
    #############################################################################
    # test osm_10000.csv，1/10000之一采样，194500记录条数，带索引
    #############################################################################
    time1 = time.time()

    #创建结果表
    #o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)')
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    ' select x,y,sum(kde) ' + \
                                    ' from( ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000 point, osm_roadnet_sampling10000 center ' + \
                                    '    where point.idx = center.idx and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000 point, osm_roadnet_sampling10000 center ' + \
                                    '    where point.idx = center.idx + 1 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000 point, osm_roadnet_sampling10000 center ' + \
                                    '    where point.idx = center.idx + 900 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000 point, osm_roadnet_sampling10000 center ' + \
                                    '    where point.idx = center.idx + 901 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000 point, osm_roadnet_sampling10000 center ' + \
                                    '    where point.idx = center.idx - 1  and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000 point, osm_roadnet_sampling10000 center ' + \
                                    '    where point.idx = center.idx - 901 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000 point, osm_roadnet_sampling10000 center ' + \
                                    '    where point.idx = center.idx - 900 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000 point, osm_roadnet_sampling10000 center ' + \
                                    '    where point.idx = center.idx + 899 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000 point, osm_roadnet_sampling10000 center ' + \
                                    '    where point.idx = center.idx - 899 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    ')                              ' + \
                                    'group by x,y',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_10000 with windows index, time used:", time2 - time1, ' ,cost:',cost.lstrip())

#############################################################################
# test osm_10000.csv，1/100000之一采样，19450记录条数，带索引，带整型对比
#############################################################################


time1 = time.time()

#创建结果表
#o.execute_sql('drop table osm_roadnet_kde_mean_test')
#o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)')
o.execute_sql('truncate table osm_roadnet_kde_mean_test')

#执行SQL
hints=dict({'odps.sql.mapper.split.size':1,
            'odps.sql.python.version':'cp37',
            'odps.sql.jobconf.odps2':'true',
            'odps.sql.cfile2.enable.read.write.index.flag':'true',
            'odps.use.legacy.fuxi.jobmaster':'true',
            'odps.sql.reshuffle.dynamicpt':'false',
            'odps.sql.mapper.cpu':600,
            'odps.sql.reducer.cpu':600,
            'odps.sql.mapper.memory':8192,
            'odps.sql.reducer.memory':8192})

instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                ' select x/120000-180,y/120000-90,sum(kde) ' + \
                                ' from( ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100000_hash_int point, osm_roadnet_sampling100000_hash_int center ' + \
                                '    where point.idx = center.idx and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y -24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100000_hash_int point, osm_roadnet_sampling100000_hash_int center ' + \
                                '    where point.idx = center.idx + 1 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100000_hash_int point, osm_roadnet_sampling100000_hash_int center ' + \
                                '    where point.idx = center.idx + 900 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100000_hash_int point, osm_roadnet_sampling100000_hash_int center ' + \
                                '    where point.idx = center.idx + 901 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100000_hash_int point, osm_roadnet_sampling100000_hash_int center ' + \
                                '    where point.idx = center.idx - 1  and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100000_hash_int point, osm_roadnet_sampling100000_hash_int center ' + \
                                '    where point.idx = center.idx - 901 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100000_hash_int point, osm_roadnet_sampling100000_hash_int center ' + \
                                '    where point.idx = center.idx - 900 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100000_hash_int point, osm_roadnet_sampling100000_hash_int center ' + \
                                '    where point.idx = center.idx + 899 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100000_hash_int point, osm_roadnet_sampling100000_hash_int center ' + \
                                '    where point.idx = center.idx - 899 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                ')                              ' + \
                                'group by x,y',
            hints=hints,async_=True,name='KDEmeanTest')

waitInstanceFinish(instance1)
time2 = time.time()
#删除中间表
#o.execute_sql('drop table osm_roadnet_kde_mean_test')

#计算用时,计算cost,KDEmeanTest
cost = getODPSTaskCost(instance1)
print("ODPS,osm_100000 with windows index and integer compare, time used:", time2 - time1, ' ,cost:',cost.lstrip())


#############################################################################
# test osm_10000.csv，1/10000之一采样，194500记录条数，带索引，带整型对比
#############################################################################

if not SKIP:
    time1 = time.time()

    #创建结果表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')
    #o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)')
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    ' select x/120000-180,y/120000-90,sum(kde) ' + \
                                    ' from( ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000_hash_int point, osm_roadnet_sampling10000_hash_int center ' + \
                                    '    where point.idx = center.idx and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y -24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000_hash_int point, osm_roadnet_sampling10000_hash_int center ' + \
                                    '    where point.idx = center.idx + 1 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000_hash_int point, osm_roadnet_sampling10000_hash_int center ' + \
                                    '    where point.idx = center.idx + 900 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000_hash_int point, osm_roadnet_sampling10000_hash_int center ' + \
                                    '    where point.idx = center.idx + 901 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000_hash_int point, osm_roadnet_sampling10000_hash_int center ' + \
                                    '    where point.idx = center.idx - 1  and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000_hash_int point, osm_roadnet_sampling10000_hash_int center ' + \
                                    '    where point.idx = center.idx - 901 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000_hash_int point, osm_roadnet_sampling10000_hash_int center ' + \
                                    '    where point.idx = center.idx - 900 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000_hash_int point, osm_roadnet_sampling10000_hash_int center ' + \
                                    '    where point.idx = center.idx + 899 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling10000_hash_int point, osm_roadnet_sampling10000_hash_int center ' + \
                                    '    where point.idx = center.idx - 899 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    ')                              ' + \
                                    'group by x,y',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_10000 with windows index and integer compare, time used:", time2 - time1, ' ,cost:',cost.lstrip())

if not SKIP:
    #############################################################################
    # test osm_1000.csv，1/1000之一采样，1945000记录条数，带索引
    #############################################################################
    time1 = time.time()

    #创建结果表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')
    #o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)  CLUSTERED BY (idx ASC) SORTED BY (idx ASC) INTO 1024 BUCKETS')
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    ' select x,y,sum(kde) ' + \
                                    ' from( ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash point, osm_roadnet_sampling1000_hash center ' + \
                                    '    where point.idx = center.idx and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash point, osm_roadnet_sampling1000_hash center ' + \
                                    '    where point.idx = center.idx + 1 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash point, osm_roadnet_sampling1000_hash center ' + \
                                    '    where point.idx = center.idx + 900 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash point, osm_roadnet_sampling1000_hash center ' + \
                                    '    where point.idx = center.idx + 901 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash point, osm_roadnet_sampling1000_hash center ' + \
                                    '    where point.idx = center.idx - 1  and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash point, osm_roadnet_sampling1000_hash center ' + \
                                    '    where point.idx = center.idx - 901 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash point, osm_roadnet_sampling1000_hash center ' + \
                                    '    where point.idx = center.idx - 900 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash point, osm_roadnet_sampling1000_hash center ' + \
                                    '    where point.idx = center.idx + 899 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash point, osm_roadnet_sampling1000_hash center ' + \
                                    '    where point.idx = center.idx - 899 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    ')                              ' + \
                                    'group by x,y',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_1000 with windows index, time used:", time2 - time1, ' ,cost:',cost.lstrip())


#############################################################################
# test osm_10000.csv，1/1000之一采样，1945000记录条数，带索引，带整型对比
#############################################################################
time1 = time.time()

#创建结果表
#o.execute_sql('drop table osm_roadnet_kde_mean_test')
#o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x INT,y INT, kde DOUBLE)')

if not SKIP:
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    ' select x/120000-180,y/120000-90,sum(kde) ' + \
                                    ' from( ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash_int point, osm_roadnet_sampling1000_hash_int center ' + \
                                    '    where point.idx = center.idx and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y -24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash_int point, osm_roadnet_sampling1000_hash_int center ' + \
                                    '    where point.idx = center.idx + 1 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash_int point, osm_roadnet_sampling1000_hash_int center ' + \
                                    '    where point.idx = center.idx + 900 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash_int point, osm_roadnet_sampling1000_hash_int center ' + \
                                    '    where point.idx = center.idx + 901 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash_int point, osm_roadnet_sampling1000_hash_int center ' + \
                                    '    where point.idx = center.idx - 1  and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash_int point, osm_roadnet_sampling1000_hash_int center ' + \
                                    '    where point.idx = center.idx - 901 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash_int point, osm_roadnet_sampling1000_hash_int center ' + \
                                    '    where point.idx = center.idx - 900 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash_int point, osm_roadnet_sampling1000_hash_int center ' + \
                                    '    where point.idx = center.idx + 899 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling1000_hash_int point, osm_roadnet_sampling1000_hash_int center ' + \
                                    '    where point.idx = center.idx - 899 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    ')                              ' + \
                                    'group by x,y',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_1000 with windows index and integer compare, time used:", time2 - time1, ' ,cost:',cost.lstrip())

if not SKIP:
    #############################################################################
    # test osm_100.csv，1/100之一采样，19458614记录条数，带索引
    #############################################################################
    time1 = time.time()

    #创建结果表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')
    #o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x DOUBLE,y DOUBLE, kde DOUBLE)  CLUSTERED BY (idx ASC) SORTED BY (idx ASC) INTO 1024 BUCKETS')
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':600,
                'odps.sql.reducer.cpu':600,
                'odps.sql.mapper.memory':8192,
                'odps.sql.reducer.memory':8192})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    ' select x,y,sum(kde) ' + \
                                    ' from( ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100 point, osm_roadnet_sampling100 center ' + \
                                    '    where point.idx = center.idx and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100 point, osm_roadnet_sampling100 center ' + \
                                    '    where point.idx = center.idx + 1 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100 point, osm_roadnet_sampling100 center ' + \
                                    '    where point.idx = center.idx + 900 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100 point, osm_roadnet_sampling100 center ' + \
                                    '    where point.idx = center.idx + 901 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100 point, osm_roadnet_sampling100 center ' + \
                                    '    where point.idx = center.idx - 1  and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100 point, osm_roadnet_sampling100 center ' + \
                                    '    where point.idx = center.idx - 901 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100 point, osm_roadnet_sampling100 center ' + \
                                    '    where point.idx = center.idx - 900 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100 point, osm_roadnet_sampling100 center ' + \
                                    '    where point.idx = center.idx + 899 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100 point, osm_roadnet_sampling100 center ' + \
                                    '    where point.idx = center.idx - 899 and  ' + \
                                    '        point.x < center.x + 0.2 and point.x > center.x - 0.2 and point.y < center.y + 0.2 and point.y > center.y - 0.2  ' + \
                                    '    group by center.x,center.y ' + \
                                    ')                              ' + \
                                    'group by x,y',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    #o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_100 with windows index, time used:", time2 - time1, ' ,cost:',cost.lstrip())

#############################################################################
# test osm_100.csv，1/100之一采样，1945万记录条数，带索引，带整型对比
#############################################################################

if not SKIP:
    time1 = time.time()

    #创建结果表
    #o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x INT,y INT, kde DOUBLE)')
    o.execute_sql('truncate table osm_roadnet_kde_mean_test')

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':450,
                'odps.sql.reducer.cpu':450,
                'odps.sql.mapper.memory':10240,
                'odps.sql.reducer.memory':10240})

    instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                    ' select x/120000-180,y/120000-90,sum(kde) ' + \
                                    ' from( ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100_hash_int point, osm_roadnet_sampling100_hash_int center ' + \
                                    '    where point.idx = center.idx and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100_hash_int point, osm_roadnet_sampling100_hash_int center ' + \
                                    '    where point.idx = center.idx + 1 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100_hash_int point, osm_roadnet_sampling100_hash_int center ' + \
                                    '    where point.idx = center.idx + 900 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x -24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100_hash_int point, osm_roadnet_sampling100_hash_int center ' + \
                                    '    where point.idx = center.idx + 901 and  ' + \
                                    '        point.x < center.x +24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100_hash_int point, osm_roadnet_sampling100_hash_int center ' + \
                                    '    where point.idx = center.idx - 1  and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y +24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100_hash_int point, osm_roadnet_sampling100_hash_int center ' + \
                                    '    where point.idx = center.idx - 901 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100_hash_int point, osm_roadnet_sampling100_hash_int center ' + \
                                    '    where point.idx = center.idx - 900 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100_hash_int point, osm_roadnet_sampling100_hash_int center ' + \
                                    '    where point.idx = center.idx + 899 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    '                               ' + \
                                    '    union all ' + \
                                    '                               ' + \
                                    '    select /*+ mapjoin(center) */ ' + \
                                    '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                    '    from osm_roadnet_sampling100_hash_int point, osm_roadnet_sampling100_hash_int center ' + \
                                    '    where point.idx = center.idx - 899 and  ' + \
                                    '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                    '    group by center.x,center.y ' + \
                                    ')                              ' + \
                                    'group by x,y',
                hints=hints,async_=True,name='KDEmeanTest')

    waitInstanceFinish(instance1)
    time2 = time.time()
    #删除中间表
    o.execute_sql('drop table osm_roadnet_kde_mean_test')

    #计算用时,计算cost,KDEmeanTest
    cost = getODPSTaskCost(instance1)
    print("ODPS,osm_100 with windows index and integer compare, time used:", time2 - time1, ' ,cost:',cost.lstrip())

#############################################################################
# test osm_100.csv，1/100之一采样，19450万记录条数，带索引，带整型对比
#############################################################################

#==========================================================================================================
#创建结果表
time1 = time.time()
#o.execute_sql('CREATE TABLE IF NOT EXISTS citybrain_prod.osm_roadnet_kde_mean_test(x INT,y INT, kde DOUBLE)')
o.execute_sql('truncate table osm_roadnet_kde_mean_test')

#执行SQL
hints=dict({'odps.sql.mapper.split.size':1,
            'odps.sql.python.version':'cp37',
            'odps.sql.jobconf.odps2':'true',
            'odps.sql.cfile2.enable.read.write.index.flag':'true',
            'odps.use.legacy.fuxi.jobmaster':'true',
            'odps.sql.reshuffle.dynamicpt':'false',
            'odps.sql.mapper.cpu':200,
            'odps.sql.reducer.cpu':200,
            'odps.sql.mapper.memory':8196,
            'odps.sql.reducer.memory':8196})

instance1 =  o.execute_sql(sql= 'insert into table osm_roadnet_kde_mean_test ' + \
                                ' select x/120000-180,y/120000-90,sum(kde) ' + \
                                ' from( ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100_hash_int center, osm_roadnet_int point ' + \
                                '    where point.idx = center.idx and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100_hash_int center, osm_roadnet_int point ' + \
                                '    where point.idx = center.idx + 1 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100_hash_int center, osm_roadnet_int point ' + \
                                '    where point.idx = center.idx + 900 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x -24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100_hash_int center, osm_roadnet_int point ' + \
                                '    where point.idx = center.idx + 901 and  ' + \
                                '        point.x < center.x +24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100_hash_int center, osm_roadnet_int point ' + \
                                '    where point.idx = center.idx - 1  and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y +24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100_hash_int center, osm_roadnet_int point ' + \
                                '    where point.idx = center.idx - 901 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '   from osm_roadnet_sampling100_hash_int center, osm_roadnet_int point ' + \
                                '    where point.idx = center.idx - 900 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100_hash_int center, osm_roadnet_int point ' + \
                                '    where point.idx = center.idx + 899 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        kde2(point.x,point.y,center.x,center.y,20) as kde, center.x as x, center.y as y  ' + \
                                '    from osm_roadnet_sampling100_hash_int center, osm_roadnet_int point ' + \
                                '    where point.idx = center.idx - 899 and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    group by center.x,center.y ' + \
                                ')                              ' + \
                                'group by x,y',
            hints=hints,async_=True,name='KDEmeanTest')

waitInstanceFinish(instance1)
time2 = time.time()
#删除中间表
o.execute_sql('drop table osm_roadnet_kde_mean_test')

#计算用时,计算cost,KDEmeanTest
cost = getODPSTaskCost(instance1)
print("ODPS,osm_100 with windows index and integer compare, time used:", time2 - time1, ' ,cost:',cost.lstrip())

