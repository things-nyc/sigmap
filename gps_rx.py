import socket
import time

UDP_IP = "104.236.29.160"
UDP_PORT = 11123

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

with open('gps_rx.data','a') as f:
  while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    now = time.time()
    datastr = "%d %s"%(now,data)
    print datastr
    f.write(datastr)
    f.flush()

