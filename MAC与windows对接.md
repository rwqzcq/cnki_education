# 1. 对接流程

## 1.1 config.yaml
git pull下来后主要修改的就是**db**的配置以及**chrome_webdriver_path**配置

## 1.2 tests.test_log.py
由于日志模块的重构，因此需要将现在的日志文件转化为新的日志文件，所以的话需要在正式爬取之前存储的json文件做一次转化，此部分的代码会写在单元测试中，vs code中需要安装unittest插件以及unittest库
> 为了确保测试框架能够通过，可以先测试test_common.py中的函数

## 1.3 定期运行main.py文件
> 点击运行work.bat文件即可

