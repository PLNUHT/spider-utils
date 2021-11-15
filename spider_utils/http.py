import pkg_resources, random
import urllib3, os
import threading

local = threading.local()


class PoolWarpper:
    def __init__(self, pool : urllib3.ProxyManager, clear_its=None, **kwargs):
        self.__pool = pool
        self.__uas = []
        self.__clear_its = clear_its
        self.__curr_cnt = 0
        self.__kwargs = kwargs
        for line in pkg_resources.resource_stream(__name__, "ualist.txt").readlines():
            self.__uas.append( line.strip() )

    def clear(self):
        if self.__pool is None:
            local.pool.clear()
        else:
            self.__pool.clear()
    
    def request(self, method, url, fields=None, headers=None, **urlopen_kw):
        """
        Make a request using :meth:`urlopen` with the appropriate encoding of
        ``fields`` based on the ``method`` used.

        This is a convenience method that requires the least amount of manual
        effort. It can be used in most situations, while still having the
        option to drop down to more specific methods when necessary, such as
        :meth:`request_encode_url`, :meth:`request_encode_body`,
        or even the lowest level :meth:`urlopen`.
        """
        if self.__pool is None:
            if (not hasattr(local, "pool")) or (local.pool is None):
                local.pool = urllib3.ProxyManager("http://proxy.service/", cert_reqs="CERT_NONE", timeout=urllib3.Timeout(connect=None, read=None), **self.__kwargs)

        if headers is None:
            headers = {}
        hasUA = False
        for kw in headers.keys():
            if kw.lower() == "user-agent":
                hasUA = True
        if not hasUA:
            headers["User-Agent"] = random.choice(self.__uas)
        if "timeout" not in urlopen_kw:
            urlopen_kw["timeout"] = 5
        
        err = None
        for i in range(5):
            try:
                if self.__pool is None:
                    ret = local.pool.request(method, url, fields, headers, **urlopen_kw)
                else:
                    ret = self.__pool.request(method, url, fields, headers, **urlopen_kw)
                if ret.status == 407:
                    err = Exception("Proxy error")
                    if self.__pool is None:
                        local.pool.clear()
                    continue
            except (urllib3.exceptions.TimeoutError, urllib3.exceptions.MaxRetryError) as e:
                err = e
                if self.__pool is None:
                    local.pool.clear()
            else:
                self.__curr_cnt += 1
                if self.__clear_its is not None and self.__curr_cnt >= self.__clear_its:
                    if self.__pool is None:
                        local.pool.clear()
                    self.__curr_cnt = 0
                return ret

        raise err
        
def ProxyManager(clear_its=8, **kwargs) -> PoolWarpper:
    if  "PRODUCTION" in os.environ:
        urllib3.disable_warnings()
        return PoolWarpper(None, clear_its=clear_its)
    else:
        return PoolWarpper(urllib3.PoolManager(**kwargs))