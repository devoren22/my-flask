from enum import Enum

class PduOptions(str, Enum):
    WAS_HTTP_REQUEST = 'http_request'
    WAS_SYN = 'was_syn'
