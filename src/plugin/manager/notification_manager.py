import logging
from dateutil.parser import parse
from spaceone.core.manager import BaseManager

from plugin.connector.kakao_biz_connector import KakaoBizConnector
from plugin.manager.message_manager import MessageManager

_LOGGER = logging.getLogger("spaceone")


class NotificationManager(BaseManager):
    def dispatch(
        self,
        phone_numbers: list,
        access_key: str,
        message: dict,
        notification_type: str,
    ) -> None:
        message_manager = MessageManager()

        title = message["title"]
        description = message.get("description")
        image_url = message.get("image_url")
        tags = message.get("tags", [])
        self.parse_occurred_at(message, tags)
        message_manager.set_receivers(
            phone_numbers, title, notification_type, description, image_url, tags
        )

        headers = {
            "Authorization": access_key,
            "Content-Type": "application/json",
        }

        kakao_biz_connector = KakaoBizConnector()
        print(message_manager.message)
        kakao_biz_connector.send_message(message_manager.message, headers)

    @staticmethod
    def parse_occurred_at(message: dict, tags: list) -> None:
        if occurred_at := message.get("occurred_at"):
            occurred_dt = parse(occurred_at)
            tags.append(
                {
                    "key": "Date",
                    "value": occurred_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "options": None,
                }
            )
