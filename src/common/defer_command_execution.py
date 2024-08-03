import os
import json
import requests as rq
from functools import wraps

def defer_command_execution(func):
    @wraps(func)
    def wrapper(event, context, *args, **kwargs):
        interaction_token = event.get("token", "")

        url = f"https://discord.com/api/v10/webhooks/{os.getenv('APPLICATION_ID')}/{interaction_token}"

        headers = {
            'Content-Type': 'application/json',
            "User-Agent": "DiscordBot (private use) Python-requests/2.x"
        }

        # コマンド実行
        payload = func(event, context)

        # Discordへのリクエスト送信
        response = rq.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # エラーが発生した場合、例外がスローされる

        # 成功時のステータスコードとレスポンスボディ
        return {
            'statusCode': response.status_code,
            'body': response.text
        }

    return wrapper
