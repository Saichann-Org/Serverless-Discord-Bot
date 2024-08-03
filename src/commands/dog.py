import time
from common.defer_command_execution import defer_command_execution

@defer_command_execution
def lambda_handler(event, context, url, headers):
    time.sleep(10)

    return {
        "content": f"Dog"
    }
