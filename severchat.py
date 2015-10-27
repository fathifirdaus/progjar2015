import socket
import string
import select
import sys

def namebysocket(socket):
	indeks = Sockets.index(socket)
	senderName = Clients[indeks]
	return str(senderName)

def socketbyname(name):
	indeks = Clients.index(name)
	socket = Sockets[indeks]
	return socket

def broadcast (sock, msg):	#sock : socket si pengirim data
	senderName = namebysocket(sock)
	message = '\r' + senderName + ': ' + msg + '\n'
	for socket in Sockets :
		if socket != sock_server and socket!= sock :
			socket.send(message)

def sendto(sockFrom, nameTo, msg):
	senderName = namebysocket(sockFrom)
	if nameTo in Clients :
		message = '<' + senderName + '> : ' + msg + '\n'
		sockTo = socketbyname(nameTo)
		sockTo.send(message)
	else :
		sockFrom.send('\r Username yang dituju belum terdaftar\n')

def storeNewClientData ( newClient_socket, newClient_name ):
	Clients.append(newClient_name)
	Sockets.append(newClient_socket)
	#notifikiasi di server
	print newClient_name +' sekarang terhubung '
	
	broadcast (sockfd,newClient_name + ' sekarang terhubung ke server.')
	
	
def client_isOffline ( off_socket ):
	off_name = namebysocket(off_socket)
	Sockets.remove(off_socket)
	print off_name +' terputus dari server.'
	broadcast (sockfd, off_name + ' terputus dari server.')
	Clients.remove(off_name)
	

def listClients( sockRequested ):
	print namebysocket(sockRequested) +' list user online.'
	sockRequested.send('\r    List User Online')
	for client in Clients :
			if client == 'Server':
				print 'ok'
			else :
				sockRequested.send('\r    Online : ' + client + '\n')

		

if __name__ == "__main__" :
	
	Clients = [] #array of clients name
	Sockets = [] #array of sockets
	
	LIMIT = 4096
	HOST = "0.0.0.0"
	PORT = 5000
	sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse address
	sock_server.bind((HOST, PORT))
	sock_server.listen(10)
	
	Clients.append('Server')
	Sockets.append(sock_server)
	print "\nServer terhubung ke jaringan ! Port server : " + str(PORT)
	
	while True:
		read_sockets, write_sockets, error_sockets = select.select(Sockets,[],[])
			
		for sock in read_sockets:
			if sock == sock_server : 
				sockfd, addr = sock_server.accept()
				
				tanda = False
				while tanda!=True :
					uname = sockfd.recv(LIMIT)
					if uname!=None and uname!=False :
						if uname in Clients :
							sockfd.send('false')
						else :
							sockfd.send('true')
							storeNewClientData(sockfd, uname)
							tanda=True
							
			else :
				msg = sock.recv(LIMIT)
				if msg :
					if msg =='keluar' :
						client_isOffline(sock) #kirim data socket client yang exiting
					else :
						arrayMsg = msg.split(' ',2)
						if arrayMsg[0]=='sendto' :
							nameTo = arrayMsg[1]
							sendto(sock, nameTo, arrayMsg[2] )
						elif arrayMsg[0]=='list' :
							listClients(sock)
							print '\n'
						else :
							broadcast (sock, msg)
	sock_server.close()
	sys.exit()
