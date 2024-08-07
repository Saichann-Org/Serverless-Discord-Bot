import os
import json
import requests as rq
from functools import wraps

def defer_command_execution(name: str, description: str, options: "list[str]" = []):
    def decorator(func):
        @wraps(func)
        def wrapper(event, context, *args, **kwargs):
            interaction_token = event.get("token", "")

            url = f"https://discord.com/api/v10/webhooks/{os.getenv('APPLICATION_ID')}/{interaction_token}"

            headers = {
                'Content-Type': 'application/json',
                "User-Agent": "DiscordBot (private use) Python-requests/2.x"
            }

            # コマンド実行
            payload = func(event, context, *args, **kwargs)

            # Discordへのリクエスト送信
            response = rq.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # エラーが発生した場合、例外がスローされる

            # 成功時のステータスコードとレスポンスボディ
            return {
                'statusCode': response.status_code,
                'body': response.text
            }

        # コマンド名と説明を関数属性として設定
        wrapper.name = name
        wrapper.description = description
        wrapper.options = options

        return wrapper
    return decorator
