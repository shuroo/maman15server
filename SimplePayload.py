from Payload import Payload
"""
Class for proccessing and sending a simple response (like in code 9000 - general error)
"""
# Payload with no header param ( like in response 9000 ).
class SimplePayload(Payload):

    def __init__(self, content):
        super().__init__("", content);