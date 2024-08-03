# Serverless-Discord-Bot

## 環境構築

このプロジェクトをローカル環境で動作させるために、以下の手順で環境構築を行います。

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
