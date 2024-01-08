import logging
from dateutil.parser import parse
from spaceone.core.manager import BaseManager

from plugin.connector.kakao_biz_connector import KakaoBizConnector
from plugin.manager.message_manager import MessageManager

_LOGGER = logging.getLogger("spaceone")


class NotificationManager(BaseManager):
    def dispatch(
        self,
        sender: str,
        phone_numbers: list,
        access_key: str,
        message: dict,
        template_id: str,
    ) -> None:
        link = message.get("link", "")
        tags = message.get("tags", [])

        message_manager = MessageManager()
        message_manager.set_message_values(sender, template_id)

        self.parse_occurred_at(message, tags)
        message_manager.set_receivers(phone_numbers, link, tags)

        headers = {
            "Authorization": access_key,
            "Content-Type": "application/json",
        }
        kakao_biz_connector = KakaoBizConnector()
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
