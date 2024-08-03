FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11-arm64

# Lambda Insights
# RUN curl -O https://lambda-insights-extension-arm64.s3-ap-northeast-1.amazonaws.com/amazon_linux/lambda-insights-extension-arm64.rpm && \
#     rpm -U lambda-insights-extension-arm64.rpm && \
#     rm -f lambda-insights-extension-arm64.rpm

COPY src ${LAMBDA_TASK_ROOT}

# RUN pip install -r requirements.txt

# CMD [ "lambda_function.handler" ]