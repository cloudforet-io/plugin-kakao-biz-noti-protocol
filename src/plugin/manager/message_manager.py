from spaceone.core.manager import BaseManager

NOTIFICATION_TYPE_MAP = {
    "INFO": "#43BEFF",
    "ERROR": "#FF6A6A",
    "SUCCESS": "#60B731",
    "WARNING": "#FFCE02",
    "DEFAULT": "#858895",
}

HEADER_ICON_URL = "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/spaceone-logo.png"


class MessageManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        template for 알림톡
        """
        # self._message = {
        #     "chnId": "@spaceone",
        #     "tmplId": "TKA0000621",
        #     "subTxtUseYn": "N",
        #     "messageReceiverList": [],
        #     "var1Vl": "제목",
        #     "var2Vl": "알림타입",
        #     "var3Vl": "본문내용",
        #     "var4Vl": "태그내용",
        # }

        """
        template for 친구톡
        """
        self._message = {
            "chnId": "@spaceone",
            "msgCotn": "SpaceONE Alert Manager에서 \n생성된 Alert 내용을 알려드립니다.\n\n[#{2}] #{1}\n\n#{3}\n\n{4}\n\n세부내용은 버튼을 눌러 확인하세요.",
            "subTxtEntprNm": "메가버드",
            "subTxtUseYn": "N",
            "messageReceiverList": [],
        }

    @property
    def message(self) -> dict:
        return self._message

    def set_receivers(
        self,
        phone_numbers: list,
        title,
        notification_type,
        description,
        image_url,
        tags,
    ) -> None:
        msg_body = (
            f"Image URL: {image_url}\n\n {description}" if image_url else description
        )
        tags_list = []
        for tag in tags:
            tags_list.append(f"{tag['key']}: {tag['value']}")
        tag_body = "\n".join(tags_list)
        for phone_number in phone_numbers:
            receiver = {
                "mbnum": phone_number,
                "var1Vl": title,
                "var2Vl": notification_type,
                "var3Vl": msg_body,
                "var4Vl": tag_body,
            }
            self._message["messageReceiverList"].append(receiver)
