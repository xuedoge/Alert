from influxdb import InfluxDBClient
from sksos import SOS
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

client = InfluxDBClient('', 8786, 'root',
                        'root', 'api_log_database')
result = client.query(
    'select Average,ErrorRate,S1000CallCount,S100CallCount,S3000CallCount,S5000CallCount,SLongCallCount from apis where ApiId = \'5bd26bd8-cbd6-4b85-bcaf-45cb3a32f932\' and time > now()-1h;')
apis_table = list(result.get_points(measurement='apis'))
#print (apis_table)

df = pd.DataFrame(data=apis_table)
x = df.drop("time", axis=1).values
# print(x)
# print(df)
detector = SOS()
df["score"] = detector.predict(x)
df
print(df.sort_values("score", ascending=False))

alert = pd.DataFrame(df.loc[df["score"] > 0.9])
#print(alert)

# 数据展示
plt.xlabel('S100CallCount')
plt.ylabel('Average')
plt.scatter('S100CallCount', 'Average', s=1, data=df)
plt.scatter('S100CallCount', 'Average', s=2, c='red', data=alert)
plt.show()
