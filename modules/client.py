import socket,os,hashlib






# client=socket.socket()
# client.connect(("127.0.0.1",8888))
# comm=input("input:").strip()
# filename = comm.split()[1]
# client.send(comm.encode())
# total_size=int(client.recv(1024).decode())
# print("total size:",total_size)
# client.send("recvd size".encode())#send ack
# recv_size=0
# m5=hashlib.md5()
# f= open(filename+".new","wb")
# while recv_size < int(total_size):
#         size = total_size - recv_size
#         if size > 1024: # must recv more once
#             data = client.recv(1024)# avoid sticky packets
#         else:
#             data = client.recv(size)#last time
#         m5.update(data)
#         f.write(data)
#         recv_size += len(data)
#
# else:
#     print("total size:%s\nrecvsize:%s"%(total_size,recv_size))
#     print("recv finished!md5:\n",m5.hexdigest())
#     server_m5=client.recv(1024).decode()
#     print("server md5:",server_m5)