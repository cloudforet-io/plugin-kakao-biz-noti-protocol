from spaceone.core.manager import BaseManager


class ProtocolManager(BaseManager):
    def get_metadata(self) -> dict:
        return {
            "metadata": {
                "data_type": "PLAIN_TEXT",
                "data": {"schema": self._get_json_schema()},
            }
        }

    @staticmethod
    def _get_json_schema() -> dict:
        return {
            "properties": {
                "phone_number": {
                    "description": "The phone number to receive alerts from KakaoTalk. Must insert the cell phone numbers format without special characters.",
                    "minLength": 10,
                    "title": "Phone Number",
                    "type": "string",
                    "pattern": "^(01([0|1|6|7|8|9]?)\d{7,8}(, |,|$))*$",
                    "examples": ["0104445566, 01077778888"],
                }
            },
            "required": ["phone_number"],
            "type": "object",
        }
