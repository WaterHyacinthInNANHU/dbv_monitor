import sys
import mmap
import struct
import win32event
from multiprocessing import Process, Queue


class DbvMonitor(object):
	def __init__(self) -> None:
		self.buffer_ready = win32event.CreateEvent (
		None, 0, 0,
		"DBWIN_BUFFER_READY"
		)
		self.data_ready = win32event.CreateEvent (
		None, 0, 0, 
		"DBWIN_DATA_READY"
		)
		self.buffer = mmap.mmap (0, 4096, "DBWIN_BUFFER", mmap.ACCESS_WRITE)
		pass

	def read_one_msg(self):
		# Signal that we're ready to accept debug output
		win32event.SetEvent(self.buffer_ready)
		if win32event.WaitForSingleObject(self.data_ready, win32event.INFINITE) == win32event.WAIT_OBJECT_0:
			self.buffer.seek(0)
			# The first DWORD is the process id which generated the output
			process_id, = struct.unpack ("L", self.buffer.read (4))
			data = self.buffer.read(4092)
			if b"\0" in data:
				string = data[:data.index (b"\0")]
			else:
				string = data
			# print "Process %d: %s" % (process_id, string)
		try:
			return (process_id, string.decode())
		except UnicodeDecodeError:
			return (process_id, '')



def service(out_queue: Queue):
	monitor = DbvMonitor()
	while True:
		msg = monitor.read_one_msg()
		out_queue.put(msg)

class DbvLisener(object):
	def __init__(self, queue_size=100000) -> None:
		self.queue_size = queue_size
		self.p_listener = None
		self.msg_queue = None

	def reset(self):
		if self.p_listener is not None:
			self.p_listener.close()
		self.msg_queue = Queue(self.queue_size)
		self.p_listener = Process(target=service, args=(self.msg_queue,), )

	def start(self):
		self.reset()
		self.p_listener.start()

	def read(self, block=True):
		assert self.msg_queue is not None, 'listener never starts'
		if not block:
			if self.msg_queue.empty():
				return None
		msg = self.msg_queue.get()
		return msg
