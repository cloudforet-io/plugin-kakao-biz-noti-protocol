from spaceone.core.error import *


class ERROR_CLIENT_REQUEST_FAILED(ERROR_INVALID_ARGUMENT):
    _message = (
        "The server cannot perform the client request. More details provided. (status_code={status_code}, "
        "reason={reason})"
    )


class ERROR_SERVER_FAILED(ERROR_UNKNOWN):
    _message = "A problem occurred on the server. More details provided. (status_code={status_code}, reason={reason})"
