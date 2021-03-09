# Spider Utils

爬虫辅助工具

### 1. get_db

获取数据库实例，在调试状态下默认使用sqlite，在当前目录下创建`db.sqlite`文件

### 2. ProxyManager

包装 `urllib3.ProxyManager`，在调试环境下转换为 `urllib3.PoolManager`。在生产环境下会使用 HTTP 代理网关。

### 3. submit

提交爬取结果，在调试环境下会检测提交结果的正确性，返回模拟结果。

在测试环境下可以通过

```python
result["_"].print()
```

来查看解析结果的细节情况。