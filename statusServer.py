#!/usr/bin/env python3

import socket

TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

running = True
data = "".encode()
while running:
	conn, addr = s.accept()
	print('Connection address:', addr)
	while 1:
		data = conn.recv(BUFFER_SIZE)
		if not data: break

		f = open("statusLog.txt", "a")
		data_str = data.decode()
		print(data_str)
		f.write(data_str+"\n")
		f.close
#		print('\n test \n')


	conn.close()
