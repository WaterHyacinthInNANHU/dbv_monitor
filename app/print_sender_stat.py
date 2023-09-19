import sys
import os
root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, root)
import socket
from time import sleep

from dbv_monitor import DbvLisener
from stat_parser import is_send_msg

"""
(video_send_stream_impl.cc:674): VideoSendStream::Stats: VideoSendStream stats: 343267170, {qp: 55, input_fps: 30, encode_fps: 30, encode_ms: 9, encode_usage_perc: 23, target_bps: 494170, media_bps: 532144, suspended: false, bw_adapted_res: false, cpu_adapted_res: false, bw_adapted_fps: false, cpu_adapted_fps: false, #cpu_adaptations: 0, #quality_adaptations: 8} {ssrc: 133811868, type: media, width: 640, height: 480, key: 59, delta: 148680, total_bps: 445528, retransmit_bps: 0, 
avg_delay_ms: 474, max_delay_ms: 604, cum_loss: 0, max_ext_seq: 588816, nack: 0, fir: 0, pli: 2}
"""
	
	
if __name__ == '__main__':

	listener = DbvLisener()
	listener.start()

	while True:
		process, msg = listener.read()
		if is_send_msg(msg):
			print(msg)
