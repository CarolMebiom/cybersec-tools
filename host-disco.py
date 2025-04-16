import socket

def send_arp():
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    try:
        sock.bind(("eth0",0))
        sock.send(packet)
        print(sock.recv(1024))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    send_arp()