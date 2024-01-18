from spaceone.core.manager import BaseManager


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

    def set_message_values(self, sender: str, template_id: str) -> None:
        self._message["chnId"] = sender
        self._message["tmplId"] = template_id

    def set_message_content(self, phone_numbers: list, link: str, tags: list) -> None:
        project_name, webhook_name = self._set_message_variables(tags)
        url_link = self._shorten_url(link) if link else "관리자에게 문의하세요"

        for phone_number in phone_numbers:
            receiver = {
                "mbnum": phone_number,
                "var1Vl": project_name,
                "var2Vl": webhook_name,
                "var3Vl": url_link,
            }
            self._message["messageReceiverList"].append(receiver)

    @staticmethod
    def _set_message_variables(tags: list) -> tuple:
        project_name = "내부"
        webhook_name = "내부 시스템"
        for tag in tags:
            if tag["key"] == "Project":
                project_name = tag["value"]
            if tag["key"] == "Triggered by":
                webhook_name = tag["value"]
        return project_name, webhook_name

    @staticmethod
    def _truncate_string(target_string: str, limit_length: int) -> str:
        if len(target_string) > limit_length:
            ceiling = limit_length - 4
            return target_string[:ceiling] + "..."
        return target_string

    @staticmethod
    def _shorten_url(link: str) -> str:
        split_link = link.split("/alert/")
        shortened_link = split_link[0] + "/alert"
        return shortened_link
