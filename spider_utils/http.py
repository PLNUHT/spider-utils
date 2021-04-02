import pkg_resources, random
import urllib3, os

class PoolWarpper:
    def __init__(self, pool : urllib3.PoolManager):
        self.__pool = pool
        self.__uas = []
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
            else:
                return ret
        raise err
        
def ProxyManager(**kwargs) -> PoolWarpper:
    if  "PRODUCTION" in os.environ:
        urllib3.disable_warnings()
        return PoolWarpper(urllib3.ProxyManager("http://proxy.service/", cert_reqs="CERT_NONE", timeout=urllib3.Timeout(connect=None, read=None), **kwargs))
    else:
        return PoolWarpper(urllib3.PoolManager(**kwargs))