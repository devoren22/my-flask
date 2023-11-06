import json


class Tcp:
    def __init__(self, src_port, dst_port, seq_num, ack_num, offset, flags, window, checksum, urgent_pointer):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.offset = offset
        self.flags = flags
        self.window = window
        self.checksum = checksum
        self.urgent_pointer = urgent_pointer

    def __str__(self):
        return json.dumps({'src_port': self.src_port,
               'dst_port': self.dst_port,
              'seq_num': self.seq_num,
               'ack_num': self.ack_num,
               'offset': self.offset,
               'flags': self.flags,
               'window': self.window,
               'checksum': self.checksum,
               'urgent_pointer': self.urgent_pointer})
