import struct


class StructUtils:
    @staticmethod
    def unpack_ip_layer(pdu_bytes):
        return struct.unpack('B' * 20, pdu_bytes)

    @staticmethod
    def unpack_tcp_layer(pdu_bytes):
        return struct.unpack('!HHIIHHHH', pdu_bytes)
