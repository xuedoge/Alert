from influxdb import InfluxDBClient
from sksos import SOS
import pandas as pd

'''
points = result.get_points()

#枚举，取出某一列的值
for item in points:
    print(item['Average'])
'''
iris = pd.read_csv("Iris.csv")