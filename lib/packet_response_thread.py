import json
from threading import Thread

from common.response import Response
from errors.http_internal_server_error import HttpInternalServerError
from errors.http_not_found_error import HttpNotFoundError
from lib.network import Network


class PacketResponderThread(Thread):
    def __init__(self, routes):
        super().__init__(target=self.response_handler)
        self.registered_routes = routes
        self.buffered_parser_request = []

    def response_handler(self):
        while True:
            for parser in self.buffered_parser_request:
                self.handle_http_response(parser)
            self.buffered_parser_request.clear()

    def work_on_response(self, parser_picture):
        self.buffered_parser_request.append(parser_picture)

    def handle_http_response(self, parser):
        if parser.http is None:
            return

            # Handle http response flow
        '''
        STEPS:
            1) find any match of registred routes.
            2) get the req object(body, query, params)
            3) if no register path matched, return Not valid path
            4) else, handle the request and respond with http response packet
        '''

        req, register_match_path = parser.http.extract_request(
            self.registered_routes)

        if register_match_path is None:
            Network.send_http_responses(parser, "Not valid path", 500, "")

        else:
            handler = self.registered_routes[register_match_path]['handler']
            success_status = self.registered_routes[register_match_path]['status']
            try:
                res = Response(success_status)
                handler(req, res)  # Can throw an exception
                data, status = res.data, res.status_code

                Network.send_http_responses(parser, data, status)
            except (HttpInternalServerError, HttpNotFoundError) as err:
                Network.send_http_responses(parser, json.dumps(
                    {'error': err.message, 'status': err.status}), err.status)
            except Exception:
                Network.send_http_responses(parser, json.dumps({'error': "Server has error", 'status': 500}),
                                            500)