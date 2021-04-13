FROM python:3.8-slim-buster AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.8-slim-buster
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY . /app

ENV PATH="/opt/venv/bin:$PATH"
