import signal
import sys, time
import traceback

class Handlers:
    def __init__(self, on_shutdown):
        self.__on_shutdown = on_shutdown
    
    def on_shutdown(self, *args):
        sys.stdout.write("Get sigterm signal:\n")
        if self.__on_shutdown is not None:
            self.__on_shutdown()
        sys.exit(0)
    

def run(func, interval, on_shutdown=None):
    handlers = Handlers(on_shutdown)
    
    signal.signal(signal.SIGTERM, handlers.on_shutdown)

    while True:
        start_time = time.time()
        try:
            func()
        except KeyboardInterrupt:
            sys.stdout.write("Keyboard Interrupted\n")
            traceback.print_exc(file=sys.stdout)
            sys.stdout.flush()
            handlers.on_shutdown()
            break
        except Exception as e:
            sys.stdout.write("Exception:\n")
            traceback.print_exc(file=sys.stdout)
            sys.stdout.flush()
        end_time = time.time()

        time_used = end_time - start_time
        time_sleep = interval - time_used

        if time_sleep > 0:
            try:
                time.sleep(time_sleep)
            except KeyboardInterrupt:
                sys.stdout.write("Keyboard Interrupted\n")
                handlers.on_shutdown()
                break
