# import threading
import socket
from time import sleep

class RecieverClient(object):
	""" Reciever for connecting to server and
		recieves string as message.
	"""
	def __init__(self):
		# threading.Thread.__init__(self)
		self.recived_message = ''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('192.168.1.247', 8888)
		self.sock.connect(server_address)
		print('connected to {}'.format(server_address))

		self.connect_target()
		
	def connect_target(self):
		self.target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		target_address = ('192.168.1.123', 1234)
		while self.target.connect_ex(target_address) != 0:
			print('Cannot connect to host, retry later...')
			sleep(3)
			self.target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print('connected to {}'.format(target_address))

	def run(self):
		while True:
			data = self.sock.recv(1000)
			# self.recived_message += data
			print(data, end='')
			try:
				self.target.sendall(data)
			except socket.error as e:
				# The connection to target end is dead / socket has closed
				self.target.close() #closing sender socket
				print ("Unable to send data %s" % e)
				print ('Reconnecting...')
				self.connect_target()

if __name__ == '__main__':
	reciever = RecieverClient()
	reciever.run()