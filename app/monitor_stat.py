import sys
import os
import re
from time import localtime, strftime
root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, root)
import socket
from time import sleep

from torch.utils.tensorboard import SummaryWriter

from dbv_monitor import DbvLisener
from stat_parser import is_send_msg

"""
(pacing_controller.cc:457): $$$1681379691837$$$stat_report$$$pacer_queue_size$$$0$$$
(send_statistics_proxy.cc:1020): $$$1681379691839$$$stat_report$$$encoded_image.size()$$$19736$$$
"""

def parse_report(msg):
	res = re.findall(r"\${1}(.+?)\${2}", msg)
	if len(res) != 4: return {}
	return {
		't_ms': int(res[0]),
		'name': res[2],
		'val': res[3],
	}

def get_time_str(format: str = "%Y-%m-%d~%H.%M.%S") -> str:
	s = strftime(format, localtime())
	return s
 
class RelativeTime():
	def __init__(self) -> None:
		self.init_time = None
	
	def __call__(self, t):
		if self.init_time is None: self.init_time = t
		return t - self.init_time
 
if __name__ == '__main__':

	listener = DbvLisener()
	listener.start()
 
 
	layout = {
		"ABCDE": {
			"main": ["Multiline", ["queue size", "frame size", "target rate bps"]],
		},
	}

	# writer = SummaryWriter()
	writer = SummaryWriter(log_dir=f'log/dbv_monitor/stat_monitor/{get_time_str()}')
	writer.add_custom_scalars(layout)
 
	relatime = RelativeTime()
	print('ready')
	while True:
		process, msg = listener.read()
		res = parse_report(msg)
		if res:
			t, name, val = relatime(res['t_ms']), res['name'], res['val']
			print(f"{t}: <{name}> {val}")
			if name == 'pacer_queue_size':
				writer.add_scalar("queue size", int(val), t)
			elif name == 'encoded_image.size()':
				writer.add_scalar("frame size", int(val), t)
			elif name == 'rl_bwe_params.target_encode_rate_bps':
				writer.add_scalar("traget rate bps", int(val), t)
			else:
				pass
	# print(parse_report(r'(pacing_controller.cc:457): $1681382219797$$$stat_report$$$pacer_queue_size$$$2786864$$$'))
