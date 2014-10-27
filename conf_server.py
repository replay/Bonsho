import asyncio


class ConfServer(asyncio.Protocol):

    TIMEOUT = 5.0

    def timeout(self):
        print('connection timeout, closing.')
        self.transport.close()

    def connection_made(self, transport):
        print('connection made')
        self.transport = transport

        # start 5 seconds timeout timer
        self.h_timeout = asyncio.get_event_loop().call_later(
            self.TIMEOUT, self.timeout)

    def data_received(self, data):
        print('data received: ', data.decode())
        self.transport.write(b'Re: ' + data)

        # restart timeout timer
        self.h_timeout.cancel()
        self.h_timeout = asyncio.get_event_loop().call_later(
            self.TIMEOUT, self.timeout)

    def eof_received(self):
        pass

    def connection_lost(self, exc):
        print('connection lost:', exc)
        self.h_timeout.cancel()
