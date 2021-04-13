import threading
from .logger import getLogger

logger = getLogger("Thread pool")

class ThreadPool:
    def __init__(self, max_workers) -> None:
        self.threads = threading.Semaphore(max_workers)
        self.sigterm = False
        self.cnt = 0
    
    def _run_wrapper(self, target, args):
        try:
            target(self.cnt, *args)
        except KeyboardInterrupt:
            logger.info("SIGTERM received")
            self.sigterm = True
        except Exception as e:
            logger.error(e)
        finally:
            self.threads.release()
            self.cnt -= 1


    def run(self, target, args):
        self.threads.acquire()
        self.cnt += 1
        if self.sigterm:
            raise KeyboardInterrupt()
        threading.Thread(target=self._run_wrapper, args=(target, args)).start()
            