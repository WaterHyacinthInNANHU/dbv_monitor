import sys
import os
import re
root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, root)
import socket
from time import sleep, time
import subprocess

class ProcessWatcher(object):
	def __init__(self, cmd, cwd):
		self.cmd = cmd
		self.cwd = cwd
		self.proc = None

	def _is_running(self):
		status = (self.proc is not None) and (self.proc.poll() is None)
		return status

	def keep_alive(self):
		if not self._is_running():
			self.proc = subprocess.Popen(self.cmd, cwd=self.cwd)

	
if __name__ == '__main__':
	# octopus
	# watchdog = ProcessWatcher(cmd=r'F:\mingxuan\projects\Octopus\AlphaRTC\out\test\peerconnection_serverless_octopus.exe F:\mingxuan\projects\Octopus\AlphaRTC\runtime\sender_pyinfer_i9.json', cwd=r'F:\mingxuan\projects\Octopus\AlphaRTC\runtime')
	# onrl-old
	watchdog = ProcessWatcher(cmd=r'F:\mingxuan\projects\Octopus\AlphaRTC\out\test\peerconnection_serverless_rlbwe.exe F:\mingxuan\projects\Octopus\AlphaRTC\runtime\sender_pyinfer_i9.json', cwd=r'F:\mingxuan\projects\Octopus\AlphaRTC\runtime')
	while True:
		sleep(1)
		watchdog.keep_alive()

# r'F:\mingxuan\projects\Octopus\AlphaRTC\out\test\peerconnection_serverless_octopus.exe F:\mingxuan\projects\Octopus\AlphaRTC\runtime\sender_pyinfer_i9.json'
