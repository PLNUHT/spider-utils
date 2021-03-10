import os
import json
import time

from .sanitize import sanitize_attributes

__submit_pool = None

def get_db():
    import peewee
    if  "PRODUCTION" in os.environ:
        DB_NAME = os.environ["DB_NAME"]
        DB_USER = os.environ["DB_USER"]
        DB_PASSWORD = os.environ["DB_PASSWORD"]
        DB_HOST = os.environ["DB_HOST"]
        DB_PORT = int(os.environ["DB_PORT"])
        return peewee.PostgresqlDatabase(
            DB_NAME, user=DB_USER, password=DB_PASSWORD,
            host=DB_HOST, port=DB_PORT
        )
    else:
        return peewee.SqliteDatabase(
            "./db.sqlite3", pragmas={
                'journal_mode': 'wal',
                'cache_size': -1024 * 64
            }
        )

def ProxyManager(**kwargs):
    import urllib3
    if  "PRODUCTION" in os.environ:
        urllib3.disable_warnings()
        return urllib3.ProxyManager("http://proxy.service/", cert_reqs="CERT_NONE", timeout=urllib3.Timeout(connect=None, read=None), **kwargs)
    else:
        return urllib3.PoolManager(**kwargs)

def submit(data):
    global __submit_pool
    if  "PRODUCTION" in os.environ:
        if __submit_pool is None:
            import urllib3
            __submit_pool = urllib3.PoolManager()
        
        res = None
        while True:
            try:
                v = __submit_pool.request("POST", "http://gather.service", body=json.dumps(data, ensure_ascii=False).encode("utf-8"), headers={'Content-Type': 'application/json'})
                str_data = v.data.decode("utf-8")
                res = json.loads(str_data)
            except UnicodeDecodeError as e:
                print(res.data, e, "decode error retry after 5 seconds")
                time.sleep(5)
                continue
            except json.JSONDecodeError as e:
                print( str_data, e, "json decode error retry after 5 seconds")
                time.sleep(5)
                continue
            except urllib3.exceptions.MaxRetryError as e:
                print(e, "retry after 5 seconds")
                time.sleep(5)
                continue
            break
        return res
    else:
        from .checker import checkHTML
        for kw in ["lang", "src", "cat", "subcat", "body", "meta"]:
            if kw not in data:
                return {
                    "code": 2,
                    "msg": "failed to parse json",
                    "_": "required key `%s`" % kw
                }
        if data["lang"] not in ["zh", "en"]:
            return {
                "code": -1,
                "msg": "invalid language",
                "_": data["lang"]
            }
        v = checkHTML(data["body"])
        if v.ok:
            return {
                "code": 0,
                "msg": "ok",
                "_": v
            }
        else:
            return {
                "code": 3,
                "msg": "Invalid html format",
                "_": v
            }

from .cron import run
