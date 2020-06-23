import base64


def encode_str_base64(message: str) -> str:
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")
    return base64_message


def encode_bytes_as_base64(message_bytes: bytes) -> str:
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")
    return base64_message
