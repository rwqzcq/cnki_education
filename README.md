## 爬取cnki官网中有关于教育类的论文
### 程序运行
```
python main.py
```
### 思路
1. 找到所有教育类C刊，并存储到json文件中
2. 先爬取所有2018年的论文存入csv文件
3. 读出csv文件，完善期刊的内容

### 文件夹解释
1. common
    - 程序公共模块，主要存放配置文件
2. config
    - 程序配置文件，比如期刊列表这些配置信息
3. dataset
    - 数据集文件，存放爬取的数据
4. init
    - 程序启动文件，存放期刊论文列表
5. log
    - 日志文件，存放爬取日志
6. paper
    - 与论文有关的程序
7. journal
    - 与期刊有关的程序
8. db
    - 与数据库有关的操作

### 主要要解决的问题
#### 1. 数据更新问题
将所有期刊的最新都存入到配置的json文件中
```
读取日志文件
批量查询是否更新
批量更新
    批量查询期刊存入期刊列表 串行还是并行？
```

### 使用的库
- yaml
- selenium

### 示例
关键词有 A;B;C
摘要有 XXX
content字段的内容是 
```
A;B;C XXX 
```
还是这种
```
关键词 A;B;C 摘要 XXX
```

