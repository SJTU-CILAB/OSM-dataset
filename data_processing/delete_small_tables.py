from odps import ODPS

o = ODPS('eCWJKNSgOAwj0Vr7', 'Jp3eplgHYOwKndLh4E9x6322QpzywW', 'nsodps_dev',
         endpoint='http://service.cn-hangzhou-yqgcy-d01.odps.res.cloud.yqgcy.cn:80/api')


for table in o.list_tables():
    table_name = str(table.name)
    if len(table_name) > 25 and table_name[:25] == 'osm_full_tag_node_machine':
        o.delete_table(table_name, if_exists=True)
        print('delete table:{}'.format(table_name))