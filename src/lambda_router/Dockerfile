FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11-arm64

# Lambda Insights
# RUN curl -O https://lambda-insights-extension-arm64.s3-ap-northeast-1.amazonaws.com/amazon_linux/lambda-insights-extension-arm64.rpm && \
#     rpm -U lambda-insights-extension-arm64.rpm && \
#     rm -f lambda-insights-extension-arm64.rpm

# Poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python3 -

# 環境変数の設定
ENV PATH="/root/.local/bin:${PATH}"

# ソースコードをコピー
COPY src ${LAMBDA_TASK_ROOT}

# Poetryで依存関係をインストール
WORKDIR ${LAMBDA_TASK_ROOT}
RUN poetry install --no-dev
