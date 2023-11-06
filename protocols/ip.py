import json


class Ip:
    def __init__(self, ip_version, header_len, ttl, protocol, checksum, src_ip, dst_ip, total_len):
        self.ip_version = ip_version
        self.header_len = header_len
        self.ttl = ttl
        self.protocol = protocol
        self.checksum = checksum
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.total_len = total_len

    def __str__(self):
        return json.dumps({'version': self.ip_version, 'header_len': self.header_len, 'ttl': self.ttl,
              'protocol': self.protocol, 'checksum': self.checksum, 'src_ip': self.src_ip, 'dst_ip': self.dst_ip, 'total_len': self.total_len})
