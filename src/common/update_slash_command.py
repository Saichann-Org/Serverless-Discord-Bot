import os
import requests as rq
from pathlib import Path
import inspect
import importlib.util

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APPLICATION_ID = os.environ.get("APPLICATION_ID")

def lambda_handler(event, context):
    base_url = "https://discord.com/api/v8"
    guilds_url = f"{base_url}/users/@me/guilds"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (private use) Python-urllib/3.11",
        "Authorization": f"Bot {BOT_TOKEN}",
    }

    # ギルドのリストを取得
    response = rq.get(guilds_url, headers=headers)

    commands_directory = Path("src/commands")
    command_list = []

    for command_file in commands_directory.glob("*.py"):
        module_name = command_file.stem
        spec = importlib.util.spec_from_file_location(module_name, command_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for _, obj in inspect.getmembers(module, inspect.isfunction):
            if hasattr(obj, 'name') and hasattr(obj, 'description') and hasattr(obj, 'options'):
                command_list.append({
                    "name": obj.name,
                    "description": obj.description,
                    "options": obj.options,
                })  

    print(f"command_list: {command_list}")

    if response.status_code == 200:
        guilds = response.json()
        for guild in guilds:
            guild_id = guild["id"]
            print(f"Processing guild: {guild_id}")

            # 既存のコマンドを取得
            commands_url = f"{base_url}/applications/{APPLICATION_ID}/guilds/{guild_id}/commands"
            existing_commands_response = rq.get(commands_url, headers=headers)
            if existing_commands_response.status_code == 200:
                existing_commands = existing_commands_response.json()
                for command in existing_commands:
                    command_id = command["id"]
                    delete_url = f"{commands_url}/{command_id}"
                    delete_response = rq.delete(delete_url, headers=headers)
                    if delete_response.status_code == 204:
                        print(f"Deleted command {command['name']} from guild {guild_id}")
                    else:
                        print(f"Failed to delete command {command['name']} from guild {guild_id}: {delete_response.text}")
            else:
                print(f"Failed to fetch existing commands for guild {guild_id}: {existing_commands_response.text}")

            # 新しいコマンドを登録
            for command in command_list:
                post_response = rq.post(commands_url, headers=headers, json=command)
                if post_response.status_code == 201:
                    print(f"Command {command['name']} successfully set for guild {guild_id}")
                else:
                    print(f"Error {post_response.status_code}: {post_response.text}")
    else:
        print(f"Error {response.status_code}: {response.text}")

lambda_handler("a","a")