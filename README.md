# Serverless-Discord-Bot

## 環境構築

本BOTをローカル環境で開発するために、以下の手順で環境構築を行います。

### 前提条件

以下のライブラリおよびツールがローカルPCにインストールされている必要があります。

- **npm**: Node.jsのパッケージマネージャー
- **pyenv**: Pythonバージョン管理ツール
- **Poetry**: Pythonの依存関係管理ツール

### ServerlessFrameworkのセットアップ

1. プロジェクトディレクトリに移動します。

2. 依存関係をインストールします。

```bash
npm ci
```

### Pythonのセットアップ

プロジェクトに適したPythonバージョンを指定します。

```bash
poetry install
```
## 新規コマンド追加

本BOTに新規コマンドを追加する場合は以下の手順で追加を行います。

### 1. Pythonスクリプトの追加

`src/commands`配下に`{コマンド名}.py`のファイルを作成し、以下のコードをベースにロジックの作成を行ってください。

return部分の記述方法については公式ドキュメントや、[Qiita記事](https://qiita.com/Izuko/items/99550613e14025b2a894)を参考にしてみて下さい。

```python
from common.defer_command_execution import defer_command_execution

@defer_command_execution(name="{コマンド名}", description="{コマンドの説明}")
def lambda_handler(event, context):

    # ここにロジックを追加

    return {
        "content": "サンプル",
        "embeds": [
            {
                "description": "サンプル",
                "color": 0x32CD32,
                "image": {
                    "url": data["message"]
                }
            }
        ]
    }

```

### 2. サードパーティーライブラリの追加

poetryへのライブラリ追加は以下のコマンドで行えます。

```bash
poetry add {ライブラリ名}
```

### 3. 新コマンド用Lamdbaの追加

実装が完了したらコマンドを実行するLambdaを作成する必要があります。
そのため`serverless.yml`の`functions`スコープに下記例に則り追記してください。※波括弧部分は置換してください。
```yml
  {コマンド名}:
    name: ${param:resourceNamePrefix}-{コマンド名}
    image:
      name: core
      command:
        - src.commands.{コマンド名}.lambda_handler
```

### 4. デプロイ

GitHub Actionsの**CD**ワークフローを実行し、約3分ほどでAWS環境に展開されます。

※Discord上で`/{コマンド名}`でコマンドが実行できるようになるまで最大10分間かかります。

## 新規タスク追加

本BOTに新規タスク(定期実行)を追加する場合は以下の手順で追加を行います。

### 1. Pythonスクリプトの追加

`src/tasks`配下に`{タスク名}.py`のファイルを作成し、以下のコードをベースにロジックの作成を行ってください。

return部分の記述方法については公式ドキュメントや、[Qiita記事](https://qiita.com/Izuko/items/99550613e14025b2a894)を参考にしてみて下さい。

```python
from common.send_to_discord import send_to_discord

@send_to_discord(channel_ids=["{送信先チャンネルID}"])
def lambda_handler(event, context):

    # ここにロジックを追加

    return {
        "content": "サンプル",
        "embeds": [
            {
                "description": "サンプル",
                "color": 0x32CD32,
                "image": {
                    "url": data["message"]
                }
            }
        ]
    }

```

### 2. サードパーティーライブラリの追加

poetryへのライブラリ追加は以下のコマンドで行えます。

```bash
poetry add {ライブラリ名}
```

### 3. 新コマンド用Lamdbaの追加

実装が完了したらタスクを実行するLambdaを作成する必要があります。
そのため`serverless.yml`の`functions`スコープに下記例に則り追記してください。※波括弧部分は置換してください。
```yml
  {タスク名}:
    name: ${param:resourceNamePrefix}-{タスク名}
    image:
      name: core
      command:
        - src.tasks.{タスク名}.lambda_handler
    events:
      - schedule:
          rate: cron(0 0 ? * * *) or rate(10 minutes)
          enabled: true
```

### 4. デプロイ

GitHub Actionsの**CD**ワークフローを実行し、約3分ほどでAWS環境に展開されます。
