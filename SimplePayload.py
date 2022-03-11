from Payload import Payload

# Payload with no header param ( like in response 9000 ).
class SimplePayload(Payload):

    def __init__(self, content):
        super().__init__("", content);