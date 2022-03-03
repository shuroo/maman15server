from Payload import Payload


class PayloadResponse(Payload):

    def __init__(self, header_param, content=""):
        super().__init__(header_param, content);