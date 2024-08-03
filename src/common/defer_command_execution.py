import os
import time
from functools import wraps

def defer_command_execution(func):
    @wraps(func)
    def wrapper(event, context, *args, **kwargs):
        # デバッグ用
        # print(event)

        interaction_token = event.get("token", "")

        url = f"https://discord.com/api/v10/webhooks/{os.getenv('APPLICATION_ID')}/{interaction_token}"

        headers = {
            'Content-Type': 'application/json',
            "User-Agent": "DiscordBot (private use) Python-requests/2.x"
        }

        # 関数に共通データを渡す
        return func(event, context, url, headers, *args, **kwargs)

    return wrapper
