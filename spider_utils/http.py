import pkg_resources, random
import urllib3, os

class PoolWarpper:
    def __init__(self, pool : urllib3.PoolManager, clear_its=None):
        self.__pool = pool
        self.__uas = []
        self.__clear_its = clear_its
        self.__curr_cnt = 0
        for line in pkg_resources.resource_stream(__name__, "ualist.txt").readlines():
            self.__uas.append( line.strip() )

    
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
                ret = self.__pool.request(method, url, fields, headers, **urlopen_kw)
            except urllib3.exceptions.TimeoutError as e:
                err = e
                self.__pool.pools.clear()
            else:
                return ret
        self.__curr_cnt += 1
        if self.__clear_its is not None and self.__curr_cnt >= self.__clear_its:
            self.__pool.pools.clear()
        raise err
        
def ProxyManager(**kwargs) -> PoolWarpper:
    if  "PRODUCTION" in os.environ:
        urllib3.disable_warnings()
        return PoolWarpper(urllib3.ProxyManager("http://proxy.service/", cert_reqs="CERT_NONE", timeout=urllib3.Timeout(connect=None, read=None), **kwargs), clear_its=8)
    else:
        return PoolWarpper(urllib3.PoolManager(**kwargs))