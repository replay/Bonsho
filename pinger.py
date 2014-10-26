import threading
import time
import queue


class QuitException(Exception):
    pass


class Pinger:
    interval = 20

    def __init__(self, *args, **kwargs):
        self.msg = kwargs['msg']
        self.connection = kwargs['connection']
        self.command_q = queue.Queue()
        self.worker = threading.Thread(
            name='Pinger for {0}'.format(kwargs['endpoint']),
            target=self.ping,
            daemon=False)
        self.worker.start()

    def queue_commands(self):
        try:
            while True:
                cmd = self.command_q.get(block=False)
                if cmd == 'quit':
                    raise QuitException()
        except queue.Empty:
            return

    def ping(self):
        run_count = 0
        try:
            while True:
                if run_count == self.interval:
                    run_count = 0
                    self.connection.send(self.msg)
                else:
                    self.queue_commands()
                    run_count += 1
                time.sleep(1)
        except QuitException:
            return

    def send_quit(self):
        self.command_q.put('quit')
        self.worker.join()
