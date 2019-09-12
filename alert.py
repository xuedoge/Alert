import time
from pyod.models.knn import KNN   # imprt kNN分类器
from influxdb import InfluxDBClient
import matplotlib.pyplot as plt
import pandas as pd

# 查询数据
#timelimit = 'time > \'2019-09-08T00:00:00Z\' and time < \'2019-09-09T00:00:00Z\''
apiid='d037a3ee-224a-42e8-93a0-207f99d79f69'
influxdb_ip = ''
influxdb_port = 8786
influxdb_user = 'root'
influxdb_pwd = 'root'
influxdb_database = 'api_log_database'
influxdb_table = 'apis'
#apiid = '5bd26bd8-cbd6-4b85-bcaf-45cb3a32f932'


def api_alert(influxdb_ip,
              influxdb_port,
              influxdb_user,
              influxdb_pwd,
              influxdb_database,
              influxdb_table,
              apiid):

    timelimit = 'time > now()-1d'
    # 访问influxdb
    client = InfluxDBClient(influxdb_ip, influxdb_port, influxdb_user,
                            influxdb_pwd, influxdb_database)
    # 获取当前API一天前的数据
    result = client.query(
        'select Average, CallCount, ErrorRate from ' + influxdb_table + ' where ApiId = \''+apiid + '\' and ' + timelimit + ';')
    # 把resultset格式的数据转换成list格式
    apis_table = list(result.get_points(measurement='apis'))
    # 把要处理的数据存成DataFrame
    df = pd.DataFrame(data=apis_table)
    # 去掉不参与运算的列，取训练集x
    x = df
    x = x.drop("time", axis=1)
    # 数据处理一下，归一化，映射到[0,1]
    x['CallCount'] = (x['CallCount']-x['CallCount'].min()) / \
        (x['CallCount'].max()-x['CallCount'].min())
    x['Average'] = (x['Average']-x['Average'].min()) / \
        (x['Average'].max()-x['Average'].min())
    x['ErrorRate'] = x['ErrorRate']/100
    # 取最后十秒的数据点作为测试点
    x_last = x.tail(1)
    #df_last = df.tail(1)
    x = x.drop(x.index[-1])
    df = df.drop(df.index[-1])
    # 转换成numpy格式准备计算
    x = x.values

    # 训练一个kNN检测器
    clf_name = 'kNN'
    clf = KNN()  # 初始化检测器clf
    clf.fit(x)  # 使用X_train训练检测器clf

    # 给df添加一列显示异常分数
    df['score'] = clf.decision_scores_

    # 排序分数
    df = df.sort_values("score", ascending=False)
    #print(df.head(20))

    # 新数据预测
    test_data = x_last
    test_scores = clf.decision_function(test_data)

    if(test_scores > 0.8):
        print('数据点异常程度4，必须报警')
    elif(test_scores > 0.5):
        print('数据点异常程度3，需要报警')
    elif(test_scores > 0.1):
        print('数据点异常程度2，建议报警')
    elif(test_scores > 0.05):
        print('数据点异常程度1，可以报警')
        #这个分级是根据KNN.py的图像分析出来的，0.05以上的很明显是异常点，0.1以上已经出现了离群现象，0.5以上就距离数据点很远了。
        #这个值根据训练用的时间相关，一天的数据0.05比较合适。
    return test_scores


def sleeptime(hour, min, sec):
    return hour*3600 + min*60 + sec


second = sleeptime(0, 0, 10)
while 1 == 1:
    time.sleep(second)
    result = api_alert(influxdb_ip,
                       influxdb_port,
                       influxdb_user,
                       influxdb_pwd,
                       influxdb_database,
                       influxdb_table,
                       apiid)
    print(result)
