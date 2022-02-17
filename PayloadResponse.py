from Payload import Payload


class PayloadResponse(Payload):

    def __init__(self, client_id, content=""):
        super().__init__(client_id, content);