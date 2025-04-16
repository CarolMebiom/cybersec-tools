import socket

def discover_host(ip):
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDPLITE)
    sock.timeout(0.5)
    port = 40555
    port_sock = 30555
    try:
        sock.sendto("ping".encode(),(ip,port))
        sock.bind(ip, port_sock)
        received = sock.recvfrom(1024)
        print(received)
    
    except Exception as e:
        print(e)
