import threading
from .logger import getLogger
from .http import local as http_local
import time

logger = getLogger("Thread pool")

class ThreadPool:
    def __init__(self, max_workers) -> None:
        self.threads = threading.Semaphore(max_workers)
        self.sigterm = False
        self.lock = threading.Lock()
        self.max_workers = max_workers
        self._thread_ids = [i for i in range(max_workers)]
        self._connections = [None for _ in range(max_workers)]

    def _run_wrapper(self, thd_id, target, args):
        try:
            http_local.pool = self._connections[thd_id]
            target(thd_id, *args)
        except KeyboardInterrupt:
            logger.info("SIGTERM received")
            self.sigterm = True
        except InterruptedError:
            logger.info("SIGTERM received")
            self.sigterm = True
        except Exception as e:
            logger.exception(e)
        finally:
            if hasattr(http_local, "pool"):
                self._connections[thd_id] = http_local.pool
            self.threads.release()
            with self.lock:
                self._thread_ids.append(thd_id)


    def run(self, target, args):
        self.threads.acquire()
        with self.lock:
            thd = self._thread_ids[-1]
            self._thread_ids = self._thread_ids[:-1]
        if self.sigterm:
            raise InterruptedError()
        threading.Thread(target=self._run_wrapper, args=(thd, target, args)).start()

    def join(self):
        while True:
            with self.lock:
                if len(self._thread_ids) == self.max_workers:
                    break
            time.sleep(0.1)