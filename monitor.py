import sys
import mmap
import struct
import win32event

buffer_ready = win32event.CreateEvent (
  None, 0, 0,
  "DBWIN_BUFFER_READY"
)
data_ready = win32event.CreateEvent (
  None, 0, 0, 
  "DBWIN_DATA_READY"
)
buffer = mmap.mmap (0, 4096, "DBWIN_BUFFER", mmap.ACCESS_WRITE)

while True:
  #
  # Signal that we're ready to accept debug output
  #
  win32event.SetEvent (buffer_ready)
  if win32event.WaitForSingleObject (data_ready, win32event.INFINITE) == win32event.WAIT_OBJECT_0:
    buffer.seek (0)
    #
    # The first DWORD is the process id which generated the output
    #
    process_id, = struct.unpack ("L", buffer.read (4))
    data = buffer.read (4092)
    if b"\0" in data:
      string = data[:data.index (b"\0")]
    else:
      string = data
    
    # print "Process %d: %s" % (process_id, string)
    print("Process %d: %s" % (process_id, string))