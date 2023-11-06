from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1, send

from protocols.ip import Ip
from protocols.tcp import Tcp


class Network:

    @staticmethod
    def send_syn_ack(ip_syn_ack, tcp_syn_ack):
        ip_packet = IP(
            src=ip_syn_ack.src_ip, dst=ip_syn_ack.dst_ip)
        tcp_packet = TCP(
            sport=tcp_syn_ack.src_port, dport=tcp_syn_ack.dst_port, flags='SA',
            ack=tcp_syn_ack.ack_num)

        scapy_syn_ack_pack = ip_packet / tcp_packet

        pkt_ack = sr1(scapy_syn_ack_pack)
        if pkt_ack['TCP'].flags != 'A':
            # Todo: Retransmit syn_ack
            pass

    @staticmethod
    def send_http_responses(parser, res, status, err_msg="", content_type='application/json'):
        ip = IP(src=parser.ip.dst_ip, dst=parser.ip.src_ip)
        tcp_ack = TCP(sport=parser.tcp.dst_port, dport=parser.tcp.src_port, flags="A",
                      seq=parser.tcp.ack_num, ack=parser.tcp.seq_num + parser.http.len)

        send(ip / tcp_ack)

        tcp_http_res = TCP(sport=parser.tcp.dst_port, dport=parser.tcp.src_port,
                           flags="PA", seq=parser.tcp.ack_num, ack=parser.tcp.seq_num + parser.http.len)

        http = parser.http.get_scapy_layer(
            str(res), err_msg, status, content_type)

        send_pack = ip / tcp_http_res / http

        send(send_pack)

    @staticmethod
    def send_tcp_rst(ip_response: Ip, tcp_response: Tcp):
        rst_pack = IP(src=ip_response.src_ip, dst=ip_response.dst_ip) / TCP(sport=tcp_response.src_port,
                                                                            dport=tcp_response.dst_port, flags="RA", seq=tcp_response.seq_num, ack=tcp_response.ack_num)
        send(rst_pack)
