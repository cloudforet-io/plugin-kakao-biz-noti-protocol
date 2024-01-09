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

    @property
    def message(self) -> dict:
        return self._message

    def set_message_values(self, sender, template_id) -> None:
        self._message["chnId"] = sender
        self._message["tmplId"] = template_id

    def set_message_content(self, phone_numbers: list, link: str, tags: list) -> None:
        project_name, webhook_name, url_link = self._set_message_variables(tags, link)

        for phone_number in phone_numbers:
            receiver = {
                "mbnum": phone_number,
                "var1Vl": project_name,
                "var2Vl": webhook_name,
                "var3Vl": url_link,
            }
            self._message["messageReceiverList"].append(receiver)

    @staticmethod
    def _set_message_variables(tags, link):
        project_name = "내부"
        webhook_name = "내부 시스템"
        link = link if link else "관리자에게 문의하세요"
        for tag in tags:
            if tag["key"] == "Project":
                project_name = tag["value"]
            if tag["key"] == "Triggered by":
                webhook_name = tag["value"]
        return project_name, webhook_name, link

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
