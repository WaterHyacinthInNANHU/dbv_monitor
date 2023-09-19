import sys
import os
import re
root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, root)
import socket
from time import sleep

from dbv_monitor import DbvLisener
# from stat_parser import is_recv_msg


def parse_report(msg):
	res = re.findall(r"\${1}(.+?)\${2}", msg)
	if len(res) != 4: return {}
	return {
		't_ms': int(res[0]),
		'name': res[2],
		'val': res[3],
	}

class VideoStatsReporter(object):
	def __init__(self, host: str, port: int) -> None:
		self.dbv_listener = DbvLisener()
		self.host, self.port = host, port
		self.connect()
		self.dbv_listener.start()
		self.seperator = 'a'*8

	def connect(self):
		self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		while self.skt.connect_ex((self.host, self.port)) != 0:
			print('Cannot connect to host, retry later...')
			sleep(3)
			self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print('Connected to {}:{}'.format(self.host, self.port))

	def serve_forever(self):
		while True:
			process_id, msg = self.dbv_listener.read(block=True)
			# timestamp, msg0, msg1 = parse(msg)
			# sleep(1)
			# msg = 'hello'
			# to_send = '{}{}'.format(self.seperator, msg).encode()
			# remove \n
			msg = msg.replace('\n', '')
			res = parse_report(msg)
			if res:
				t, name, val = res['t_ms'], res['name'], res['val']
				print(f"{t}: <{name}> {val}")				
				to_send = f'stat:{name},{val}:stat'.encode()
				try:
					self.skt.sendall(to_send)
				except (ConnectionAbortedError, ConnectionResetError):
					print('Connection aborted, reconnecting...')
					self.connect()
					continue
	
	
if __name__ == '__main__':

	# listener = DbvLisener()
	# listener.start()

	# features = ['VideoSendStream::Stats', '']

	# while True:
	# 	process, msg = listener.read()
	# 	res = parse(msg)
	# 	if res:
	# 		timestamp, msg0, msg1 = res
	# 		print('{} {}'.format(timestamp, msg1))

	# print(parse(sample))

	reporter = VideoStatsReporter('192.168.44.1', 1234)
	reporter.serve_forever()
