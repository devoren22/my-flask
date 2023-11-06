import json
from common.request import Request


class Http:
    def __init__(self, raw_data_after_parsed):
        #  example: ['GET /stam?firstName=oren HTTP/1.1', 'User-Agent: PostmanRuntime/7.29.2', 'Accept: */*', 'Cache-Control: no-cache', 'Postman-Token: be94891c-f571-4bc1-9c2a-52caf3416dae', 'Host: 192.168.1.108:132', 'Accept-Encoding: gzip, deflate, br', 'Connection: keep-alive', '', '']
        request = raw_data_after_parsed[0].split(' ')
        self.method = request[0]
        self.path = request[1]
        self.protocol = request[2]
        self.len = len('\r\n'.join(raw_data_after_parsed))
        self.body = {}

        if raw_data_after_parsed[-1] != "":
            self.body = json.loads(raw_data_after_parsed[-1])

    def __str__(self):
        return json.dumps({"method": self.method, 'path': self.path, 'protocol': self.protocol, 'len': self.len, 'body': self.body})

    def get_scapy_layer(self, content, err_msg, status, content_type):
        http_content = '\r\n'.join([f"{self.protocol} {status} {err_msg}", f"Content-Type: {content_type}",
                                   f"Content-Length:{len(content.encode('utf-8'))}", ""])
        http_content += "\r\n"
        http_content += content
        return http_content

    def extract_request(self, registered_routes):
        # { 'query': { 'firstName': 'oren' }  }
        req = Request()

        def validate_path_and_parse_params():
            params_res = {}

            # router_path: "/stam/:id/:anotherId?firstName=oren"
            # got: /stam/3/5?firstName=oren&lastName=kaizer
            is_valid_right_now = True
            for router_path in registered_routes.keys():
                is_valid_right_now = True
                params_res.clear()

                if registered_routes[router_path]['method'] != self.method:
                    continue

                router_path_sections = router_path.split(
                    "/")[1:]  # ["stam", ":id", ":anotherId"]
                curr_got_path_without_query = "".join(self.path.split("?")[0])
                curr_got_path_without_query_sections = curr_got_path_without_query.split(
                    "/")[1:]  # ["stam", "3", "5"]

                is_match_path = len(router_path_sections) == len(
                    curr_got_path_without_query_sections)
                if not is_match_path:
                    is_valid_right_now = False
                    continue

                for idx, (router_section, got_section) in enumerate(zip(router_path_sections, curr_got_path_without_query_sections)):
                    if router_section.find(":") == -1:
                        # If we didnt get the params yet ["/stam", ":id", ":anotherId"]
                        # Sections must be match(the base path)
                        if router_section != got_section:
                            is_valid_right_now = False
                            break
                    else:

                        clean_param_key = router_section[1:]  # :id => id

                        # Check for the last section ["/5?firstName=oren"]
                        if got_section.find("?"):
                            got_section = got_section.split("?")[0]

                        params_res[clean_param_key] = got_section

                if is_valid_right_now:
                    return params_res, router_path

            # Remove query
            return None, None

        def parse_query():
            # got: /stam/3/5?firstName=oren&lastName=kaizer
            query_res = {}

            res = self.path.split("?")
            is_found_question_mark = len(res) > 1
            if not is_found_question_mark:
                return

            list_queries_str = res[1].split("&")

            for query_param in list_queries_str:
                key, val = query_param.split('=')
                query_res[key] = val

            return query_res

        params_res, register_path = validate_path_and_parse_params()

        if not register_path:
            return None, None

        query_res = parse_query()

        req.body, req.params, req.query = self.body, params_res, query_res
        return req, register_path
