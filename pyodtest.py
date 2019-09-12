from pyod.models.knn import KNN   # imprt kNN分类器
from influxdb import InfluxDBClient
import matplotlib.pyplot as plt
import pandas as pd


# 访问influxdb
client = InfluxDBClient('', 8786, 'root',
                        'root', 'api_log_database')
# 查询数据
#timelimit = 'time > \'2019-08-26T00:00:00Z\' and time < \'2019-08-26T01:00:00Z\''
timelimit = 'time > now()-1d'
apiid = '5bd26bd8-cbd6-4b85-bcaf-45cb3a32f932'
# apiid='d037a3ee-224a-42e8-93a0-207f99d79f69'
result = client.query(
    'select Average, CallCount, ErrorRate from apis where ApiId = \''+apiid + '\' and ' + timelimit + ';')
# 把resultset格式的数据转换成list格式
apis_table = list(result.get_points(measurement='apis'))
# 把要处理的数据存成DataFrame
df = pd.DataFrame(data=apis_table)
# 数据处理一下
df['CallCount'] = df['CallCount']*1
df['Average'] = df['Average']*1
df['ErrorRate'] = df['ErrorRate']
# 去掉time，这一列不参与运算
x = df
x = x.drop("time", axis=1)
#x = x.drop("ErrorRate", axis=1)
x = x.values


# 训练一个kNN检测器
clf_name = 'kNN'
clf = KNN()  # 初始化检测器clf
clf.fit(x)  # 使用X_train训练检测器clf

'''# 返回训练数据X_train上的异常标签和异常分值
y_train_pred = clf.labels_  # 返回训练数据上的分类标签 (0: 正常值, 1: 异常值)
y_train_scores = clf.decision_scores_  # 返回训练数据上的异常值 (分值越大越异常)'''

df['score'] = clf.decision_scores_
#df['pred'] = clf.labels_
df = df.sort_values("score", ascending=False)
print(df.head(10))
print(df['CallCount'].max())
max_score = df.head(1)['score'].values
print(max_score)
df['prob']=df['score']/max_score
print(df.head(10))

'''
# 用训练好的clf来预测未知数据中的异常值
y_test_pred = clf.predict(X_test)  # 返回未知数据上的分类标签 (0: 正常值, 1: 异常值)
y_test_scores = clf.decision_function(X_test)  #  返回未知数据上的异常值 (分值越大越异常)'''

# 新数据预测
testdata = {"Average": 150, "CallCount": 130 ,'ErrorRate':100}
test = pd.DataFrame(data=testdata, index=[0])
print(test)
test_scores = clf.decision_function(test)
print(test_scores)


alert = pd.DataFrame(df.loc[df['score'] > 10])
# 数据展示
plt.title(timelimit)
plt.xlabel('Average')
plt.ylabel('CallCount')
plt.scatter('Average', 'CallCount', s=1, data=df)
plt.scatter('Average', 'CallCount', s=2, c='red', data=alert)
#plt.scatter('Average', 'CallCount', s=3, c='green', data=test)
plt.show()
