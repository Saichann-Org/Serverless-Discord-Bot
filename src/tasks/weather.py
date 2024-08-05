import random
from common.send_to_discord import send_to_discord

@send_to_discord(channel_ids=["1248782266721898566"])
def lambda_handler(event, context):

    dice_list = ["お", "ち", "ん", "ま", "う", "こ"]

    word = ""
    for i in range(5):
        word += random.choice(dice_list)

    return {
        "embeds": [
            {
                "description": word,
                "color": 0x32CD32,
            }
        ]
    }
