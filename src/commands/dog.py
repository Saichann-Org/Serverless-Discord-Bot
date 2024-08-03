import json
import time
import requests
from common.defer_command_execution import defer_command_execution

@defer_command_execution
def lambda_handler(event, context, url, headers):
    time.sleep(10)

    payload = {
        "content": f"Dog"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        status_code = response.status_code
        response_body = response.text
    except requests.exceptions.RequestException as e:
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    print(status_code, response_body)

    return {
        'statusCode': status_code,
        'body': response_body
    }
