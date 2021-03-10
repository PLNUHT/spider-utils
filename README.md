# Spider Utils

## 安装方法

```console
$ python setup.py install
```

## 说明

爬虫辅助工具

### 1. get_db

获取数据库实例，在调试状态下默认使用sqlite，在当前目录下创建`db.sqlite`文件。相关文档请参考 [docs](http://docs.peewee-orm.com/en/latest/peewee/quickstart.html)

### 2. ProxyManager

包装 `urllib3.ProxyManager`，在调试环境下转换为 `urllib3.PoolManager`。在生产环境下会使用 HTTP 代理网关。

### 3. submit

提交爬取结果，在调试环境下会检测提交结果的正确性，返回模拟结果。

在测试环境下可以通过

```python
result["_"].print()
```

来查看解析结果的细节情况。参考代码 `examples/submit.py`。

### 4. run(func, interval, on_shutdown = None)

定时任务运行程序，参数：
* func: 定时运行的函数
* interval: 函数func运行的时间间隔（单位为秒）
* on_shutdown: 在程序终止时调用的函数（通常在代码更新等情况下会终止程序，可以在此时进行数据保存等操作）

参考 `examples/run_interval.py`