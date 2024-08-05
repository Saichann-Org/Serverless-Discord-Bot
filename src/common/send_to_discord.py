import os
import json
import requests as rq
from functools import wraps
from typing import Callable, Any, List

def send_to_discord(channel_ids: List[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            headers = {
                "Authorization": f"Bot {os.environ.get('BOT_TOKEN')}",
                "Content-Type": "application/json"
            }
            
            payload = func(*args, **kwargs)
            
            for channel_id in channel_ids:
                url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
                response = rq.post(url, headers=headers, data=json.dumps(payload))
                
                response.raise_for_status()  # エラーが発生した場合、例外がスローされる

            # 成功時のステータスコードとレスポンスボディ
            return {
                'statusCode': response.status_code,
                'body': response.text
            }

        return wrapper

    return decorator