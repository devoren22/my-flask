import json
from copy import deepcopy

from enums.flags_enum import Flags
from enums.pdu_enum import PduOptions
from enums.protocols_enum import Protocols

from  common.singelton_decorator import singleton

from protocols.http import Http
from protocols.ip import Ip
from protocols.tcp import Tcp

from utils.general_utils import Utils
from utils.struct_utils import StructUtils

# Struct rules: B = 1, H = 2, I = 4
@singleton
class Parser:
    def __init__(self):
        self.ip = None
        self.tcp = None
        self.http = None

    def parse_ip_packet(self, pdu):
        '''
            version + header length = [:1]
            type of service = [1:2]
            total length = [2:4]
            identification = [4:6]
            flags + fragmentOffest = [6:8]
            time to live = [8: 9]
            protocol = [9:10]
            header checksum = [11: 12]
            srcIp = [12: 16]
            destIp = [16:20]
        '''

        # Get the ip unpacked values
        ip_unpacked = StructUtils.unpack_ip_layer(pdu[0:20])

        helper_total_len = ip_unpacked[2:4]
        total_len = (helper_total_len[0] << 8) + helper_total_len[1]

        version_and_header_len_fields = ip_unpacked[:1][0]
        ip_version, header_len = Utils.parse_byte_to_4_bits_tuple(
            version_and_header_len_fields)
        # print(ip_unpacked)
        # total_len = ip_unpacked[3]

        time_to_live = ip_unpacked[8:9][0]

        protocol = ip_unpacked[9:10][0]

        header_checksum = ip_unpacked[11:12][0]

        src_ip_octets_list = list(ip_unpacked[12:16])
        src_ip = '.'.join(
            Utils.convert_all_list_to_str(src_ip_octets_list))

        dst_ip_octets_list = list(ip_unpacked[16:20])
        dst_ip = '.'.join(
            Utils.convert_all_list_to_str(dst_ip_octets_list))

        self.ip = Ip(ip_version, header_len, time_to_live,
                     protocol, header_checksum, src_ip, dst_ip, total_len)

    def parse_tcp_packet(self, pdu):
        '''
            source port = [0] (16 bits) (H)
            destination port = [1] (16 bits) (H)
            sequence number = [2] (32 bits) (I)
            ack number = [3] (32 bits) (I)
            data offset = [4] (left) (4 bits) (H) oooo rrrr rrff ffff
            reserved (6 bits)
            flags (6 bits)
            window = [5] (16 bits) (H)
            checksum = [6] (16 bits) (H)
            urgent pointer = [7] (16 bits) (H)
        '''
        # Get tcp unpacked values

        tcp_unpacked = StructUtils.unpack_tcp_layer(pdu[20:40])

        source_port = tcp_unpacked[0]
        dst_port = tcp_unpacked[1]
        seq_num = tcp_unpacked[2]
        ack_num = tcp_unpacked[3]
        offset_reversed_flags = tcp_unpacked[4]
        offset = (offset_reversed_flags >> 12) * 4
        flags = offset_reversed_flags & 0b0000000000111111
        window = tcp_unpacked[5]
        checksum = tcp_unpacked[6]
        urgent_pointer = tcp_unpacked[7]

        self.tcp = Tcp(source_port, dst_port, seq_num, ack_num,
                       offset, flags, window, checksum, urgent_pointer)

    def parse_to_syn_ack(self):
        ip_syn_ack = deepcopy(self.ip)
        tcp_syn_ack = deepcopy(self.tcp)

        # Tcp manipulations
        tcp_syn_ack.flags = 0x12 # Flags to syn-ack
        tcp_syn_ack.src_port, tcp_syn_ack.dst_port = tcp_syn_ack.dst_port, tcp_syn_ack.src_port # Switch ports
        tcp_syn_ack.ack_num = tcp_syn_ack.seq_num + 1 # ack is the seq plus 1 of the syn packet

        # Parse layer 3 ips
        ip_syn_ack.src_ip, ip_syn_ack.dst_ip = ip_syn_ack.dst_ip, ip_syn_ack.src_ip

        # tcp && ip.addr==108.156.2.2
        return ip_syn_ack, tcp_syn_ack

    def parse_to_rst_ack(self):
        ip_rst_ack = deepcopy(self.ip)
        tcp_rst_ack = deepcopy(self.tcp)

        tcp_rst_ack.src_port, tcp_rst_ack.dst_port = tcp_rst_ack.dst_port, tcp_rst_ack.src_port  # Switch ports
        tcp_rst_ack.ack_num = tcp_rst_ack.seq_num + 1
        tcp_rst_ack.seq_num = 1


        ip_rst_ack.src_ip, ip_rst_ack.dst_ip = ip_rst_ack.dst_ip, ip_rst_ack.src_ip

        return ip_rst_ack, tcp_rst_ack

    def parse_http_packet(self, pdu):

        offset = self.tcp.offset
        raw_data = pdu[20 + offset:]
        if not raw_data:
            print("No http")
            return

        try:
            data = raw_data.decode().split('\r\n')

            is_http_packet = 'HTTP' in data[0]
            if is_http_packet:
                self.http = Http(data)
                return True
        except:
            print("Error in parsing http data")
        # If it's not http request return False.
        return False

    def parse_pdu(self, pdu):
        self.parse_ip_packet(pdu)

        if self.ip.protocol != Protocols.TCP:
            return

        # We parse only TCP
        self.parse_tcp_packet(pdu)

        # When get tcp pdu syn, we need to return syn_ack packet to establish connection(before getting http)
        if self.tcp.flags == Flags.SYN:
            return PduOptions.WAS_SYN


        is_http_req = self.parse_http_packet(pdu)
        if is_http_req:
            return PduOptions.WAS_HTTP_REQUEST