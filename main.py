import socket

def discover_host(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(10)
    port = 40555
    try:
        sock.sendto("ping".encode(),(ip,port))
        received = sock.recvmsg(1024, ["MSG_DONTWAIT"])
        received = received.decode("utf-8")
        print(received)
    
    except Exception as e:
        print(e)
    
    finally:
        sock.close()
if __name__ == "main":
    discover_host("192.168.67.19")
