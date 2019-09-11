from pyod.models.knn import KNN   # imprt kNN分类器
from influxdb import InfluxDBClient
import matplotlib.pyplot as plt
import pandas as pd

# 访问influxdb
client = InfluxDBClient('10.16.78.70', 8786, 'root',
                        'root', 'api_log_database')
# 查询数据
#timelimit = 'time > \'2019-09-08T00:00:00Z\' and time < \'2019-09-09T00:00:00Z\''
timelimit = 'time > now()-1d'
#apiid = '5bd26bd8-cbd6-4b85-bcaf-45cb3a32f932'
apiid='d037a3ee-224a-42e8-93a0-207f99d79f69'
result = client.query(
    'select Average, CallCount, ErrorRate from apis where ApiId = \''+apiid + '\' and ' + timelimit + ';')
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

x_last = x.tail(1)
print(x_last)
df_last = df.tail(1)

x = x.drop(x.index[-1])
df = df.drop(df.index[-1])

x = x.values


# 训练一个kNN检测器
clf_name = 'kNN'
clf = KNN()  # 初始化检测器clf
clf.fit(x)  # 使用X_train训练检测器clf

'''# 返回训练数据X_train上的异常标签和异常分值
y_train_pred = clf.labels_  # 返回训练数据上的分类标签 (0: 正常值, 1: 异常值)
y_train_scores = clf.decision_scores_  # 返回训练数据上的异常值 (分值越大越异常)'''

# 给df添加一列显示宜昌分数
df['score'] = clf.decision_scores_
#df['pred'] = clf.labels_

# 排序分数
df = df.sort_values("score", ascending=False)
print(df.tail(20))

'''#分数->映射到[0,1] 转换为概率表示
max_score=df.head(1)['score'].values
df['prob']=df['score']/max_score
print(df.head(10))'''

'''
# 用训练好的clf来预测未知数据中的异常值
y_test_pred = clf.predict(X_test)  # 返回未知数据上的分类标签 (0: 正常值, 1: 异常值)
y_test_scores = clf.decision_function(X_test)  #  返回未知数据上的异常值 (分值越大越异常)'''

# 新数据预测

test_data = x_last
# print(test_data)
test_scores = clf.decision_function(test_data)
print(df_last)
print(test_scores)

rate = 0.05
alert = pd.DataFrame(df.loc[df['score'] > rate])
# 数据展示
title = timelimit + '|Rate=' + str(rate)
plt.title(title)
plt.xlabel('Average')
plt.ylabel('CallCount')
plt.scatter('Average', 'CallCount', s=1, data=df)
plt.scatter('Average', 'CallCount', s=2, c='red', data=alert)
# 展示测试数据点
if (test_scores >= 0.05):
    plt.scatter('Average', 'CallCount', s=3, c='purple', data=df_last)
else:
    plt.scatter('Average', 'CallCount', s=3, c='yellow', data=df_last)
plt.show()
