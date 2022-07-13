import re
import json

### parser ###

"""
sample = r'(video_send_stream_impl.cc:674): VideoSendStream::Stats: VideoSendStream stats: 1038143402, {qp: 56, input_fps: 30, encode_fps: 29, encode_ms: 7, encode_usage_perc: 25, target_bps: 1454155, media_bps: 662048, suspended: false, bw_adapted_res: false, cpu_adapted_res: false, bw_adapted_fps: false, cpu_adapted_fps: false, #cpu_adaptations: 0, #quality_adaptations: 26} {ssrc: 3600624451, type: media, width: 640, height: 480, key: 37, delta: 43852, total_bps: 815568, retransmit_bps: 0, avg_delay_ms: 158, max_delay_ms: 298, cum_loss: 0, max_ext_seq: 163370, nack: 0, fir: 0, pli: 0}'
parsed to:
(1038143402, 
{'qp': '56', 'input_fps': '30', 'encode_fps': '29', 'encode_ms': '7', 'encode_usage_perc': '25', 'target_bps': '1454155', 'media_bps': '662048', 'suspended': 'false', 'bw_adapted_res': 'false', 'cpu_adapted_res': 'false', 'bw_adapted_fps': 'false', 'cpu_adapted_fps': 'false', '#cpu_adaptations': '0', '#quality_adaptations': '26'}, {'ssrc': '3600624451', 'type': 'media', 'width': '640', 'height': '480', 'key': '37', 'delta': '43852', 'total_bps': '815568', 'retransmit_bps': '0', 'avg_delay_ms': '158', 'max_delay_ms': '298', 'cum_loss': '0', 'max_ext_seq': '163370', 'nack': '0', 'fir': '0', 'pli': '0'}
)
"""

escape_pat_key = re.compile(r'((, )|{)(.*?):')
escape_pat_value = re.compile(r': (.*?)(,|})')
parse_send_pat = re.compile(r'VideoSendStream stats: (.*?), ({.*?}) ({.*?})')
parse_recv_pat = re.compile(r'VideoReceiveStream stats: (.*?), ({.*?}) ({.*?})')

def msg2dict(msg: str)-> dict:
	keys = re.findall(escape_pat_key, msg)
	keys = [i[-1] for i in keys]
	values = re.findall(escape_pat_value, msg)
	values = [i[0] for i in values]
	assert len(keys) == len(values), '\nmsg: {}, \nkeys: {}, \nvalues: {}'.format(msg, keys, values)
	res = {}
	for key, value in zip(keys, values):
		res[key] = value
	return res

def parse_send_stat(msg: str)-> tuple:
	m = re.search(parse_send_pat, msg) 
	if m is None:
		return None
	m = m.groups()
	timestamp = int(m[0])
	msg0 = msg2dict(m[1])
	msg1 = msg2dict(m[2])
	return timestamp, msg0, msg1

def parse_recv_stat(msg: str)-> tuple:
	m = re.search(parse_recv_pat, msg) 
	if m is None:
		return None
	m = m.groups()
	timestamp = int(m[0])
	msg = msg2dict(m[1])
	return timestamp, msg

def is_send_msg(msg: str):
	return re.search(parse_send_pat, msg) is not None 

def is_recv_msg(msg: str):
	return re.search(parse_send_pat, msg) is not None 

###