import random
from common.defer_command_execution import defer_command_execution

@defer_command_execution(name="ncodice", description="うこダイス")
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
