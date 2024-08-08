import os
import requests as rq
from pathlib import Path
import inspect
import importlib.util

BOT_TOKEN = os.getenv("BOT_TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")

BASE_URL = "https://discord.com/api/v8"
GUILDS_URL = f"{BASE_URL}/users/@me/guilds"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "DiscordBot (private use) Python-urllib/3.11",
    "Authorization": f"Bot {BOT_TOKEN}",
}

def get_guilds():
    response = rq.get(GUILDS_URL, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def load_commands(commands_directory="src/commands"):
    commands = []
    for command_file in Path(commands_directory).glob("*.py"):
        module_name = command_file.stem
        spec = importlib.util.spec_from_file_location(module_name, command_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        commands.extend(
            {
                "name": func.name,
                "description": func.description,
                "options": func.options,
            }
            for _, func in inspect.getmembers(module, inspect.isfunction)
            if all(hasattr(func, attr) for attr in ("name", "description", "options"))
        )
    return commands

def sync_commands(guild_id, commands):
    commands_url = f"{BASE_URL}/applications/{APPLICATION_ID}/guilds/{guild_id}/commands"
    existing_commands = rq.get(commands_url, headers=HEADERS).json()

    existing_names = {cmd["name"] for cmd in existing_commands}
    new_names = {cmd["name"] for cmd in commands}

    # 更新・追加
    for command in commands:
        if command["name"] in existing_names:
            existing_cmd = next(cmd for cmd in existing_commands if cmd["name"] == command["name"])
            if command["description"] != existing_cmd["description"] or command["options"] != existing_cmd["options"]:
                rq.patch(f"{commands_url}/{existing_cmd['id']}", headers=HEADERS, json=command).raise_for_status()
        else:
            rq.post(commands_url, headers=HEADERS, json=command).raise_for_status()

    # 削除
    for command in existing_commands:
        if command["name"] not in new_names:
            rq.delete(f"{commands_url}/{command['id']}", headers=HEADERS).raise_for_status()

def lambda_handler(event, context):
    commands = load_commands()
    guilds = get_guilds()

    for guild in guilds:
        print(f"Processing guild: {guild['id']}")
        sync_commands(guild["id"], commands)
