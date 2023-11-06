from lib.packet_response_thread import PacketResponderThread
from lib.sniffer import Sniffer
from common.app_router import AppRouter


class Router(AppRouter):
    def __init__(self, port):
        super().__init__()
        self.responder = PacketResponderThread(self.routes)
        self.sniffer = Sniffer(port, self.responder)


    def run(self):
        self.responder.start()
        self.sniffer.start()

        self.responder.join()
        self.sniffer.join()

    def register_blueprint(self, blueprint):
        for key in blueprint.routes.keys():
            self.routes[key] = blueprint.routes[key]
