from influxdb import InfluxDBClient
from sksos import SOS
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
#访问influxdb
client = InfluxDBClient('10.16.78.70', 8786, 'root',
                        'root', 'api_log_database')
#查询数据
result = client.query(
    'select  Average , CallCount from apis where ApiId = \'5bd26bd8-cbd6-4b85-bcaf-45cb3a32f932\' and time > now()-1h;')
#把resultset格式的数据转换成list格式
apis_table = list(result.get_points(measurement='apis'))
#把要处理的数据存成DataFrame
df = pd.DataFrame(data=apis_table)
#去掉time，这一列不参与运算
x = df.drop("time", axis=1).values
#定义SOS
detector = SOS()
#给df新添加一列存分数
df["score"] = detector.predict(x)
#查看df按照分数排序后的结果
print(df.sort_values("score", ascending=False))
#把df中分数大于0.9的数据提取出来存成alert中
alert = pd.DataFrame(df.loc[df["score"] > 0.9])
print(alert)

# 数据展示
plt.xlabel('CallCount')
plt.ylabel('Average')
plt.scatter('CallCount','Average', s=1, data=df)
plt.scatter('CallCount','Average', s=2, c='red', data=alert)
plt.show()
