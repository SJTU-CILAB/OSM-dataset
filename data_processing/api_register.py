from flask import Flask
from odps import ODPS

app = Flask(__name__)


@app.route('/')
def osm_node_Select():
    o = ODPS('eCWJKNSgOAwj0Vr7', 'Jp3eplgHYOwKndLh4E9x6322QpzywW', 'nsodps_dev',
             endpoint='http://service.cn-hangzhou-yqgcy-d01.odps.res.cloud.yqgcy.cn:80/api')

    with o.execute_sql("select count(1) as cnt from osm_junction_highway").open_reader(tunnel=True) as reader:
        for record in reader:
            a = record['cnt']
            return a
