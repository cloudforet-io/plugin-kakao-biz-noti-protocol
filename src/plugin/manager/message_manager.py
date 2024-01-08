from spaceone.core.manager import BaseManager

# NOTIFICATION_TYPE_MAP = {
#     "INFO": "#43BEFF",
#     "ERROR": "#FF6A6A",
#     "SUCCESS": "#60B731",
#     "WARNING": "#FFCE02",
#     "DEFAULT": "#858895",
# }

MAIN_MAX_LENGTH = 1000
DESCRIPTION_MAX_LENGTH = 600


class MessageManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        template for 알림톡
        """
        self._message = {
            "chnId": "",
            "tmplId": "",
            "subTxtUseYn": "N",
            "messageReceiverList": [],
            "var1Vl": "프로젝트명",
            "var2Vl": "웹훅명",
            "var3Vl": "링크",
        }

        # """
        # template for 친구톡
        # """
        # self._message = {
        #     "chnId": "@spaceone",
        #     "msgCotn": "",
        #     "subTxtEntprNm": "메가버드",
        #     "subTxtUseYn": "N",
        #     "messageReceiverList": [],
        # }

    @property
    def message(self) -> dict:
        return self._message

    def set_message_values(self, sender, template_id) -> None:
        self._message["chnId"] = sender
        self._message["tmplId"] = template_id

    def set_receivers(self, phone_numbers: list, link: str, tags: list) -> None:
        project_name, webhook_name = self._process_tags(tags)
        for phone_number in phone_numbers:
            receiver = {
                "mbnum": phone_number,
                "var1Vl": project_name,
                "var2Vl": webhook_name,
                "var3Vl": link,
            }
            self._message["messageReceiverList"].append(receiver)

    @staticmethod
    def _process_tags(tags):
        project_name = ""
        webhook_name = ""
        webhook_exists = False
        for tag in tags:
            if tag["key"] == "Project":
                project_name = tag["value"]
            if tag["key"] == "Triggered by":
                webhook_exists = True
                webhook_name = tag["value"]
        if not webhook_exists:
            webhook_name = "내부 시스템"
        return project_name, webhook_name

    # def _set_link(self, link):
    #     link_content = f"{LINK_CONTENT}: {link}"
    #     if len(link_content) > VAR_MAX_LENGTH:
    #         link_content = ""
    #     return link_content

    @staticmethod
    def _truncate_string(target_string: str, limit_length: int) -> str:
        if len(target_string) > limit_length:
            ceiling = limit_length - 4
            return target_string[:ceiling] + "..."
        return target_string
