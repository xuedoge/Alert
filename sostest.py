from influxdb import InfluxDBClient
from sksos import SOS
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

client = InfluxDBClient('', 8786, 'root',
                        'root', 'api_log_database')
#timelimit = 'time > \'2019-08-26T00:00:00Z\' and time < \'2019-08-26T01:00:00Z\''
timelimit = 'time > now()-60m'
apiid='5bd26bd8-cbd6-4b85-bcaf-45cb3a32f932'
#apiid='d037a3ee-224a-42e8-93a0-207f99d79f69'
result = client.query(
    'select Average, CallCount from apis where ApiId = \''+apiid +'\' and '+ timelimit +';')
apis_table = list(result.get_points(measurement='apis'))

df = pd.DataFrame(data=apis_table)

detector = SOS()
df['CallCount']=df['CallCount']*1
df['Average']=df['Average']*10
#df['ErrorRate']=df['ErrorRate']*100+1

x = df.drop("time", axis=1).values
#x = x.drop("Average", axis=1).values
df["score"] = detector.predict(x)

print(df.sort_values("score", ascending=False).head(10))

alert = pd.DataFrame(df.loc[df["score"] > 0.9])
#print(alert)

# 数据展示
plt.title(timelimit)
plt.xlabel('Average')
plt.ylabel('CallCount')
plt.scatter('Average', 'CallCount', s=1, data=df)
plt.scatter('Average', 'CallCount', s=2, c='red', data=alert)
plt.show()

