FROM python:3.10-bullseye AS base
WORKDIR /project
COPY . .
ARG GITHUB_TOKEN
RUN pip3 install -r requirements.txt

FROM base AS test
CMD ["python3", "-m", "coverage", "run" ,"-m", "pytest", "tests"]

FROM base AS prod-server
CMD ["python3", "start_rabbit_mq.py"]

FROM base as prod-worker
CMD ["python3", "redis_worker.py"]