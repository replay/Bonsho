import asyncio


class EventLoop:

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def add_reader(self, socket, handler):
        self.loop.add_reader(socket, handler)

    def run(self):
        self.loop.run_forever()
