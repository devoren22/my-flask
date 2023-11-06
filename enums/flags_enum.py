from enum import Enum


class Flags(int, Enum):
    SYN = 2,
    ACK = 16,
    SYN_ACK = 18
    FIN_ACK = 17
    RST_ACK = 20
    PSH_ACK = 24
    FIN_PSH_ACK = 25
    CONGESTION = 194
