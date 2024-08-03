import json
from discord_interactions import verify_key, InteractionType, InteractionResponseType
import os
import boto3

def lambda_handler(event, context):
    print(event)

    request_body = json.loads(event.get("body", "{}"))
    headers = event.get("headers", {})

    signature = headers.get("x-signature-ed25519")
    timestamp = headers.get("x-signature-timestamp")
    raw_body = event.get("body", "{}").encode()
    if signature is None or timestamp is None or \
        not verify_key(raw_body, signature, timestamp, os.environ.get("DISCORD_PUBLIC_KEY")):
        return {
            'statusCode': 401,
            'body': "Bad request signature"
        }

    # Handle request
    interaction_type = request_body.get("type")

    if interaction_type in [InteractionType.APPLICATION_COMMAND, InteractionType.MESSAGE_COMPONENT]:
        data = request_body.get("data", {})
        command_name = data.get("name")

        response_data = {
            "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
        }
        # Kick another Lambda async
        client = boto3.client("lambda")
        client.invoke(
            FunctionName=f"{os.environ.get('RESOURCE_NAME_PREFIX')}-{command_name}",
            InvocationType="Event",
            Payload=json.dumps(request_body)
        )

    else:
        response_data = {"type": InteractionResponseType.PONG}

    print(response_data)
    return {
        'statusCode': 200,
        'body': json.dumps(response_data)
    }
