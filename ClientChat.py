import socket, select, string, sys


def prompt() :
	sys.stdout.write('<You> : ')
	sys.stdout.flush()

def registrate() :
	sys.stdout.write('Masukkan username anda : ')
	username = sys.stdin.readline().rstrip('\n')
	
	if username :
		s.send(username) 
		respons = s.recv(LIMIT)
		if str(respons) == 'false' and respons != None and respons != None :
			print ' Username tersebut sudah terdaftar !'
		if str(respons) == 'true' and respons != None  and respons != False :
			print ' Username anda adalah '+ username
			return True
	else :
		print 'Username harus terisi !'
	
#main function
if __name__ == "__main__" :
	
	if(len(sys.argv) < 3):
		print ' Cara menggunakan : python clients.py <hostname> <port>'
		sys.exit()
		
		
	host = sys.argv[1]
	port = int (sys.argv[2])
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.settimeout(2)
	
	try :
		s.connect((host, port))
	except :
		print 'Gagal konek ke server'
		sys.exit()
		
	LIMIT = 4096
	
	
	print 'Koneksi ke server sukses!\nSilahkan Login'
	Flag = False
	Flag = registrate()
	
	while Flag!=True:
		Flag=registrate()
	
	prompt()
	
	while True:
		list_socket = [sys.stdin, s]
		read_sockets, write_sockets, error_sockets = select.select(list_socket, [], [])
		
		for sock in read_sockets :
			if sock == s : #ada pesan masuk dari server
				data = s.recv(LIMIT)
				if data != None and data != False:
					#print data
					sys.stdout.write(data)
					prompt()
				
			else : #user memasukkan pesan
				msg = sys.stdin.readline().rstrip('\n')
				
				if str(msg) =='keluar' :
					s.send(msg)
					sys.stdout.write('Memutuskan sambungan ke server...\n')
					sys.exit()
				else :
					s.send(msg) 
					prompt() #user mengirim pesan
					
	sys.exit()
