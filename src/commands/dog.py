import json
import requests as rq
from common.defer_command_execution import defer_command_execution

@defer_command_execution
def lambda_handler(event, context):
    dog_url = "https://dog.ceo/api/breeds/image/random"
    res = rq.get(dog_url)
    res.raise_for_status()
    data = res.json()

    return {
        # "content": "aa",
        "embeds": [
            {
                "description": "いぬ",
                "color": 0x32CD32,
                "image": {
                    "url": data["message"]
                }
            }
        ]
    }
