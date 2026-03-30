
from odps import ODPS
import time

o = ODPS('HBqKYJJvPhAUedfP', 'j9JiW91K78Q7J48tpfz3Jzrjn7s4XK', 'nsodps_wuxi',
endpoint='http://service.cn-jswx-xuelang-d01.odps.res.cloud.wuxi-yqgcy.cn:80/api')

def waitInstanceFinish(instance):
    while 1:
        if instance.is_terminated():
            break
        time.sleep(2)
    return True

def getODPSTaskCost(instance,task_name='KDEmeanTest'):
    detail2= instance.get_task_detail2(task_name)
    cost = detail2.get('mapReduce').get('summary').split('\n')[0].split(":")[1]
    cpu= cost.split(",")[0]
    mem= cost.split(",")[1]
    return cpu + ',' + mem


#############################################################################
# test osm_10.csv，1/10之一采样，带索引
#############################################################################


# insert into kde_result
# select x/120000-180,y/120000-90,sum(kde)
# from(
#     select x1 x,y1 y,sum(density) as kde
#     from osm_density
#     group by x1,y1
#     distribute by x,y
#     sort by x,y

#     union all 
#     select x2 x,y2 y,sum(density) as kde
#     from osm_density
#     group by x2,y2
#     distribute by x,y
#     sort by x,y 
# ) group by x,y


#创建结果表
#o.execute_sql('drop table osm_roadnet_kde_mean_test')
o.execute_sql('CREATE TABLE IF NOT EXISTS osm_density(x1 INT,y1 INT,x2 INT,y2 INT,density FLOAT)')
o.execute_sql('truncate table osm_density')

def run_part_1_5(j):

    #执行SQL
    hints=dict({'odps.sql.mapper.split.size':1,
                'odps.sql.python.version':'cp37',
                'odps.sql.jobconf.odps2':'true',
                'odps.sql.cfile2.enable.read.write.index.flag':'true',
                'odps.use.legacy.fuxi.jobmaster':'true',
                'odps.sql.reshuffle.dynamicpt':'false',
                'odps.sql.mapper.cpu':200,
                'odps.sql.reducer.cpu':100,
                'odps.sql.mapper.memory':8192,
                'odps.sql.mapjoin.memory.max':4096,
                'odps.sql.reducer.memory':4096})

    #time1 = time.time()
    #osm_roadnet_level_distance_opt_t
    sql= 'insert into   osm_density ' + \
                                ' select x1,y1,x2,y2,density ' + \
                                ' from( ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 <= 24000 and y % 48000 <= 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx and point.id > center.id and   ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 <= 24000 and y % 48000 <= 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx - 1 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 <= 24000 and y % 48000 <= 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx - 900 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '   from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 <= 24000 and y % 48000 <= 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx - 899 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 >= 24000 and y % 48000 >= 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx and point.id > center.id and   ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 >= 24000 and y % 48000 >= 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx + 1 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 >= 24000 and y % 48000 >= 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx + 900 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '   from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 >= 24000 and y % 48000 >= 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx + 901 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                ') where density > 1e-6                              '

    sql=sql.replace("##",str(j))
    instance1 =  o.execute_sql(sql,hints=hints,async_=True,name='KDEmeanTest')
    waitInstanceFinish(instance1)

    sql= 'insert  into osm_density   ' + \
                                ' select x1,y1,x2,y2,density' + \
                                ' from( ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 > 24000 and y % 48000 < 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx and point.id > center.id and   ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 > 24000 and y % 48000 < 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx + 1 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 > 24000 and y % 48000 < 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx - 900 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '   from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 > 24000 and y % 48000 < 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx - 901 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 < 24000 and y % 48000 > 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx and point.id > center.id and   ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 < 24000 and y % 48000 > 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx - 1 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '    from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 < 24000 and y % 48000 > 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx + 900 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                '                               ' + \
                                '    union all ' + \
                                '                               ' + \
                                '    select /*+ mapjoin(center) */ ' + \
                                '        center.x as x1, center.y as y1,point.x as x2,point.y as y2, kdensity(point.x,point.y,center.x,center.y,20.0) as density  ' + \
                                '   from (select * from osm_roadnet_level_distance_opt_t where idx % 6 = ## and   x %  48000 < 24000 and y % 48000 > 24000 ) center, osm_roadnet_level_distance_opt_t point ' + \
                                '    where point.idx = center.idx + 899 and point.id > center.id and  ' + \
                                '        point.x < center.x + 24000 and point.x > center.x - 24000 and point.y < center.y + 24000 and point.y > center.y - 24000  ' + \
                                ') where density > 1e-6                              '
    sql=sql.replace("##",str(j))
    instance1 =  o.execute_sql(sql,hints=hints,async_=True,name='KDEmeanTest')
    waitInstanceFinish(instance1)


for i in range(6):
    run_part_1_5(i)
