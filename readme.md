# API调用数据实时异常检测算法

>  可以参考的文章：[实时异常检测最终汇报 ](https://confluence.newegg.org/pages/viewpage.action?pageId=55026518)

- KNN.py是图形化展示算法可行性的程序。
- alert.py包含一个每次调用能返回异常值分数的函数**api_alert**，并且每十秒调用他一次。

## 用到的Python库介绍：

### [pyod](https://pyod.readthedocs.io/en/latest/example.html#knn-example)：
- Python Outlier Detection（PyOD）是当下最流行的Python异常检测工具库(**详情见链接**)，其主要亮点包括：
- 包括近20种常见的异常检测算法，比如经典的ABOD以及最新的深度学习如对抗生成模型（GAN）和集成异常检测（outlier ensemble）
- 支持不同版本的Python：包括2.7和3.5+；支持多种操作系统：windows，macOS和Linux
- 简单易用且一致的API，只需要几行代码就可以完成异常检测，方便评估大量算法
- 使用JIT和并行化（parallelization）进行优化，加速算法运行及扩展性（scalability），可以处理大量数据

### InfluxDBClient：
- Python的influxdb处理模块

### [matplotlib-pyplot](https://www.matplotlib.org.cn/tutorials/introductory/pyplot.html)：
* matplotlib.pyplot 是命令样式函数的集合(**详情见链接**)，使matplotlib像MATLAB一样工作。
* 每个pyplot函数对图形进行一些更改：例如，创建图形，在图形中创建绘图区域，在绘图区域中绘制一些线条，用标签装饰图形等。
* 在matplotlib.pyplot中，各种状态在函数调用中保留，以便跟踪当前图形和绘图区域等内容，并且绘图函数指向当前轴

### [pandas](https://www.pypandas.cn/docs/getting_started/basics.html)：
- Pandas 是一个 Python 的包(**详情见链接**)，提供快速、灵活和富有表现力的数据结构，旨在使“关系”或“标记”数据的使用既简单又直观。
- 它的目标是成为用Python进行实际的、真实的数据分析的基础高级模块。
- 此外，它还有更宏远的目标，即成为超过任何语言的最强大，最灵活的开源数据分析/操作工具。

## 代码介绍：

> 代码注释写得很详细

### 函数定义
`def api_alert(influxdb_ip,
              influxdb_port,
              influxdb_user,
              influxdb_pwd,
              influxdb_database,
              influxdb_table,
              apiid):`
              
### 返回结果
<pre>
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
</pre>
