from spaceone.core.error import ERROR_REQUIRED_PARAMETER
from spaceone.notification.plugin.protocol.lib.server import ProtocolPluginServer

from plugin.manager.notification_manager import NotificationManager
from plugin.manager.protocol_manager import ProtocolManager

app = ProtocolPluginServer()


@app.route("Protocol.init")
def protocol_init(params: dict) -> dict:
    """init plugin by options

    Args:
        params (ProtocolInitRequest): {
            'options': 'dict',    # Required
            'domain_id': 'str'
        }

    Returns:
        PluginResponse: {
            'metadata': 'dict'
        }
    """
    protocol_manager = ProtocolManager()
    return protocol_manager.get_metadata()


@app.route("Protocol.verify")
def protocol_verify(params: dict) -> None:
    """Verifying protocol plugin

    Args:
        params (ProtocolVerifyRequest): {
            'options': 'dict',      # Required
            'secret_data': 'dict',  # Required
            'domain_id': 'str'
        }

    Returns:
        None
    """
    pass


@app.route("Notification.dispatch")
def notification_dispatch(params: dict) -> None:
    """dispatch notification

    Args:
        params (NotificationDispatchRequest): {
            'options': 'dict',              # Required
            'secret_data': 'dict',          # Required
            'channel_data': 'dict',         # Required
            'message': 'dict',              # Required
            'notification_type': 'str',     # Required
        }

    Returns:
        None
    """
    channel_data = params["channel_data"]
    secret_data = params["secret_data"]
    if not (phone_number := channel_data.get("phone_number")):
        raise ERROR_REQUIRED_PARAMETER(key="channel_data.phone_number")

    phone_numbers = phone_number.replace(" ", "").split(",")
    phone_numbers = [phone_number for ph in phone_numbers if ph != ""]
    message = params["message"]
    notification_type = params["notification_type"]
    access_key = secret_data.get("access_key")

    notification_manager = NotificationManager()

    notification_manager.dispatch(phone_numbers, access_key, message, notification_type)
