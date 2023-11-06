import socket
from copy import deepcopy
from threading import Thread


from enums.pdu_enum import PduOptions
from lib.network import Network
from lib.parser import Parser


class Sniffer(Thread):
    MTU = 65535

    def __init__(self, port, responder):

        self.parser = Parser()
        self.s = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.port = port
        self.s.bind(("0.0.0.0", self.port))
        # Starting listener sniffer(self), and the responder thread
        super().__init__(target=self.listening_socket, daemon=True)
        self.responder = responder

    def listening_socket(self):
        print('Listen..')
        while True:
            pdu, address = self.s.recvfrom(Sniffer.MTU)

            pdu_options_sign = self.parser.parse_pdu(pdu)

            if self.parser.tcp.dst_port != self.port:
                print("Port not match.")
                ip_rst_ack, tcp_rst_ack = self.parser.parse_to_rst_ack()
                Network.send_tcp_rst(ip_rst_ack, tcp_rst_ack)

            elif pdu_options_sign == PduOptions.WAS_SYN:
                ip_syn_ack, tcp_syn_ack = self.parser.parse_to_syn_ack()
                Network.send_syn_ack(ip_syn_ack, tcp_syn_ack)

            elif pdu_options_sign == PduOptions.WAS_HTTP_REQUEST:
                self.responder.work_on_response(deepcopy(self.parser))



