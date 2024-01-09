import os
import logging
import time
import datetime

from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json, to_json
from google.protobuf.json_format import MessageToDict

_LOGGER = logging.getLogger(__name__)

TOKEN = os.environ.get("MEGABIRD_TOKEN", None)

if TOKEN == None:
    print(
        """
##################################################
# ERROR
#
# Configure your Slack Token first for test
##################################################
example)

export SLACK_TOKEN=<YOUR_SLACK_TOKEN>

"""
    )
    exit


class TestNaverWorksNotification(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    endpoints = config.get("ENDPOINTS", {})
    secret_data = {"access_key": TOKEN}
    channel_data = {"phone_number": "01095117872"}

    def test_init(self):
        import yaml

        print(os.environ)
        input_dict = {
            "options": {},
            "message": {
                "title": "This is sample notification",
                "link": "https://spaceone.console.doodle.spaceone.dev/monitoring/alert-manager/escalation-policy",
                "image_url": "https://picsum.photos/200/300",
                "description": "Thresholds Crossed: 1 out of the last 1 datapoints [0.524033991396324 (29/06/21 "
                "05:06:00)] was less than the lower thresholds [0.6043306920412774] or greater than "
                "the upper thresholds [0.6544568893755576] (minimum 1 datapoint for OK -> ALARM "
                "transition).",
                "tags": [
                    {
                        "key": "project_id",
                        "value": "project-xxxxx",
                        "options": {"short": True},
                    },
                    {
                        "key": "project_name",
                        "value": "스페이스원 웹서버",
                        "options": {"short": True},
                    },
                    {
                        "key": "resource_id",
                        "value": "Resource [Asia Pacific (Seoul)]:[AWS/NetworkELB]: net/af83f347171a044af96459ebb37c8225/743a23562a96c595",
                    },
                ],
                "callbacks": [
                    {
                        "label": "Acknowledge SpaceONE Alerts",
                        "url": "https://monitoring-webhook.dev.spaceone.dev/monitoring/v1/alert/alert-61afa17a25bf/4186dacf2d69a689ca4dbed965ef6e2d/ACKNOWLEDGED",
                    }
                ],
                "occurred_at": datetime.datetime.utcnow().isoformat(),
            },
            "notification_type": "ERROR",
            "secret_data": self.secret_data,
            "channel_data": self.channel_data,
        }
        with open("./test.yaml", "w") as f:
            yaml.dump(input_dict, f)
        v_info = self.notification.Protocol.init({"options": {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.notification.Protocol.verify(
            {"options": options, "secret_data": self.secret_data}
        )

    def test_dispatch(self):
        options = {}
        params = {
            "options": options,
            "message": {
                "title": "This is sample notification",
                "link": "https://spaceone.console.doodle.spaceone.dev/monitoring/alert-manager/escalation-policy",
                "image_url": "https://picsum.photos/200/300",
                "description": "Thresholds Crossed: 1 out of the last 1 datapoints [0.524033991396324 (29/06/21 05:06:00)] was less than the lower thresholds [0.6043306920412774] or greater than the upper thresholds [0.6544568893755576] (minimum 1 datapoint for OK -> ALARM transition).",
                "tags": [
                    {
                        "key": "project_id",
                        "value": "project-xxxxx",
                        "options": {"short": True},
                    },
                    {
                        "key": "project_name",
                        "value": "스페이스원 웹서버",
                        "options": {"short": True},
                    },
                    {
                        "key": "resource_id",
                        "value": "Resource [Asia Pacific (Seoul)]:[AWS/NetworkELB]: net/af83f347171a044af96459ebb37c8225/743a23562a96c595",
                    },
                ],
                "callbacks": [
                    {
                        "label": "Acknowledge SpaceONE Alerts",
                        "url": "https://monitoring-webhook.dev.spaceone.dev/monitoring/v1/alert/alert-61afa17a25bf/4186dacf2d69a689ca4dbed965ef6e2d/ACKNOWLEDGED",
                    }
                ],
                "occurred_at": datetime.datetime.utcnow().isoformat(),
            },
            "notification_type": "ERROR",
            "secret_data": self.secret_data,
            "channel_data": self.channel_data,
        }
        self.notification.Notification.dispatch(params)
