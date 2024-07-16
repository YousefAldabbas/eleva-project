from fastapi import Header


def message_locale(message: dict):
    def _message_locale(local: str = Header(default="en", alias="Accept-Language")):
        return message[local]

    return _message_locale
