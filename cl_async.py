import asyncio
import sys

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        #print('1Data received: {!r}'.format(data.decode())) raw
        print(f'Data received: {data.decode()}')

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()

#message = 'Hello World!'
while True:
    #message = 'cmd.exe /C cd c:'

    message = input(">>")
    if message != "q":
        try:
            coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),'192.168.0.44', 8888)
            loop.run_until_complete(coro)
            loop.run_forever()
        except Exception as ex:
            print(ex)
    else:
        loop.close()
        sys.exit(0)